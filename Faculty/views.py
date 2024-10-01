from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from Faculty.models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages  # To display error messages

# Create your views here.

# faculty login
msg_delete={}
def factLogin(request):
    if request.method == 'POST':
        zprn = request.POST['zprn']
        pwd = request.POST['pass']
        data = {}
        try:
            # Try to get a single FacultyLogin object
            factInfo = FacultyLogin.objects.get(ZPRN=zprn)
            # Now check the ZPRN and password
            if factInfo.ZPRN == zprn and factInfo.password == pwd: # Ideally, compare hashed passwords
                    request.session['ZPRN'] = factInfo.ZPRN
                    return redirect('/faculty/home/')
            else:
                data = {'error': 'Invalid ZPRN or password please try again'}
        except FacultyLogin.DoesNotExist:
            # Handle the case when the faculty login is not found
            data = {'error': "Your account Does Not Exist. First create account"}
        # Render the form with the error
        return render(request, 'faculty/index.html', data)
    return render(request, 'faculty/index.html')

def home(request):
    try:
        if request.session['ZPRN'] is None :
            return redirect('faculty/')
    except:
        return redirect('/faculty/')
    
    zprn = request.session['ZPRN']  
    dict={ 'zprn': zprn}
    return render(request, 'faculty/HomeFaculty.html', dict)


def addExamCategory(request):
    zprn = request.session.get('ZPRN')          # Check if the session variable exists
    if zprn is None:
        return redirect('faculty/')  # Adjust the redirect as needed
    context = { 'zprn': zprn }
    try:
        sub = Exam_sub.objects.all()  # Use `objects` instead of `object`
        context['subdata'] = sub  # Add subdata to context
    except Exam_sub.DoesNotExist:
        context['msg'] = 'No data found'
    context['msg_delete']= msg_delete
    
    if request.method == 'POST':
        try:
            sub = request.POST['sub']
            time = request.POST['time']
            Exam_sub.objects.create(Subject= sub, exam_time_min= time)
            context['alert']= {
                'cls': 'success', 'mg': 'Sucessfully', 'desc': 'Add subject sucessfully'
            }
            sub = Exam_sub.objects.all()  # Use `objects` instead of `object`
            context['subdata'] = sub
        except Exception as e :
            context['alert']= {
                'cls': 'danger', 'mg': 'ERROR', 'desc': 'Subject is already Added'
            }
    return render(request, 'faculty/Add_exam_category.html', context)  # Pass a single context dictionary

# delete subject
def deleteSub(request, sub_id):
    if request.method == 'POST':
        try:
            row = Exam_sub.objects.get(id=sub_id)
            name = row.Subject
            row.delete()
            messages.success(request, f'{name} has been deleted successfully.')
        except :
            pass
    return HttpResponseRedirect('/faculty/add-exam-category/')

# Edit the subject
def editSub(request, sub_id):
    zprn = request.session.get('ZPRN')          # Check if the session variable exists
    if zprn is None:
        return redirect('faculty/')  # Adjust the redirect as needed
    context = { 'zprn': zprn }
    if request.method == 'GET':
        row = Exam_sub.objects.get(id=sub_id)
        return render(request, 'faculty/editSub.html', {'row': row, 'zprn': zprn})
    else:
        sn = request.POST.get('sb')
        tm = request.POST.get('time')
        row = Exam_sub.objects.get(id=sub_id)
        try:
            if sn and tm:
                row.Subject = sn
                row.exam_time_min = tm
                row.save()
                alert={
                'mg': 'Subject is Updated Sucessfully',
                'cls' :'success',
                'st': 'Updated'
                }
        except:
            alert={     'mg': 'Subject not Updated, Subject is already exit, Something is wrong ',                'cls' :'danger',                'st': 'ERROR'                }

        return render(request, 'faculty/editSub.html', {'row': row, 'zprn': zprn, 'msg': alert})

# select the subject to add question
def selectSub(request):
    zprn = request.session.get('ZPRN')          # Check if the session variable exists
    if zprn is None:
        return redirect('faculty/')  # Adjust the redirect as needed
    context = { 'zprn': zprn }

    
    rows= Exam_sub.objects.all()

    return render(request, 'faculty/selectSub.html',{'zprn': zprn, 'rows': rows})

# def addQues(request, sub_id):
#     try:
#         if request.session['ZPRN'] is None :
#             return redirect('faculty/')
#     except:
#         return redirect('/faculty/')          # Check if the session variable exists
#     zprn = request.session['ZPRN']  
#     try:
#         subrow= Exam_sub.objects.get(id= sub_id)
#         sn = subrow.Subject
#     except:
#         sn=''
#     records = Question.objects.filter(sub= sn)
#     print(records)
#     if request.method == 'POST':
#         try:
#             q = Question()
#             count = Question.objects.filter(sub=sn).count()
#             q.ques_no = count+1
#             q.ques = request.POST.get('question')
#             q.opt1 = request.POST.get('opt1')
#             q.opt2 = request.POST.get('opt2')
#             q.opt3 = request.POST.get('opt3')
#             q.opt4 = request.POST.get('opt4')
#             q.ans = request.POST.get('ans')
#             q.img = None
#             if len(request.FILES) !=0:
#                 q.img = request.FILES['img']
#             q.q_set = zprn
#             q.save()
#             # Question.objects.create(ques_no= ques_no, ques= ques, img= img, opt1= opt1, opt2= opt2, opt3= opt3, opt4= opt4, ans = ans,  sub=sn, ques_setter= q_set)
#             alert= {
#                 'cls': 'success', 'mg': 'Sucessfully', 'desc': 'Add question sucessfully'
#             }
#         except Exception as e:
#             print(e)
#             alert= { #' Something is Wrong..! question not added'
#                 'cls': 'danger', 'mg': 'ERROR', 'desc': e
#             }
#         return render(request, 'faculty/Add_edit_que.html', {'zprn': zprn, 'subname': sn, 'rows': records, 'alert': alert})

#     return render(request, 'faculty/Add_edit_que.html', {'zprn': zprn, 'subname': sn, 'rows': records })
  
def addQues(request, sub_id):
    try:
        if request.session['ZPRN'] is None:
            return redirect('faculty/')
    except KeyError:
        return redirect('/faculty/')  # Redirect if session variable doesn't exist
    zprn = request.session['ZPRN']  
    try:
        subrow = Exam_sub.objects.get(id=sub_id)
        sn = subrow.Subject
    except Exam_sub.DoesNotExist:
        sn = ''
    records = Question.objects.filter(sub=sn)

    if request.method == 'POST':
        try:
            # logic to update question no column
            q_count = Question.objects.filter(sub=sn).count()
            last_question = Question.objects.filter(sub=sn).order_by('-id').first()
            if q_count !=0 and last_question.ques_no != q_count :
                 # apply logic 
                q_asc = Question.objects.filter(sub=sn).order_by('id')
                counter=0
                for row in q_asc:
                    counter+=1
                    row.ques_no= counter
                    row.save()
            #add new question
            q = Question()
            q.ques = request.POST.get('question')
            q.opt1 = request.POST.get('opt1')
            q.opt2 = request.POST.get('opt2')
            q.opt3 = request.POST.get('opt3')
            q.opt4 = request.POST.get('opt4')
            q.ans = request.POST.get('ans')
            # Handle image upload
            if 'img' in request.FILES:
                q.img = request.FILES['img']
            else:
                q.img = None
            q.ques_no = q_count+1
            q.sub = sn
            q.ques_setter = zprn
            q.save()
            print(q)

            alert = {
                'cls': 'success',
                'mg': 'Successfully',
                'desc': 'Question added successfully'
            }
        except Exception as e:
            print(e)
            alert = {
                'cls': 'danger',
                'mg': 'ERROR',
                'desc': str(e)
            }
        
        return render(request, 'faculty/Add_edit_que.html', {
            'zprn': zprn,
            'subname': sn,
            'rows': records,
            'alert': alert
        })

    return render(request, 'faculty/Add_edit_que.html', {
        'zprn': zprn,
        'subname': sn,
        'rows': records
    })


#   edit the question 
def editQue(request, q_id):
    zprn = request.session.get('ZPRN')          # Check if the session variable exists
    if zprn is None:
        return redirect('faculty/')  # Adjust the redirect as needed
    context = { 'zprn': zprn }
    row=None
    sn=''   #subject name
    if request.method == 'GET':
        row = Question.objects.get(id=q_id)
        sn = row.sub
        id = Exam_sub.objects.get(Subject= sn).id
        return render(request, 'faculty/Edit_Question.html', {'row': row, 'zprn': zprn, 'sid': id})
    
    if request.method == 'POST':
        try:
            q = Question.objects.get(id=q_id)
            q.ques = request.POST.get('question')
            q.opt1 = request.POST.get('opt1')
            q.opt2 = request.POST.get('opt2')
            q.opt3 = request.POST.get('opt3')
            q.opt4 = request.POST.get('opt4')
            q.ans = request.POST.get('ans')

            # Handle image upload
            if 'img' in request.FILES:
                q.img = request.FILES['img']
            
            q.ques_setter = zprn
            q.save()

            alert = {
                'cls': 'success',
                'mg': 'Successfully',
                'desc': 'Question updated successfully'
            }
        except Exception as e:
            print(e)
            alert = {
                'cls': 'danger',
                'mg': 'ERROR',
                'desc': str(e)
            }
        row = Question.objects.get(id=q_id)
        
        sn = row.sub
        id = Exam_sub.objects.get(Subject= sn).id
        return render(request, 'faculty/Edit_Question.html', {
            'zprn': zprn,
            'row': row,
            'msg':alert,
            'sid': id
        })
    sn = row.sub
    id = Exam_sub.objects.get(Subject= sn).id
    return render(request, 'faculty/Edit_Question.html', {'zprn': zprn,'sid': id})


# delete question
# def deleteQue(request, q_id):
#     try:
#         if request.session['ZPRN'] is None:
#             return redirect('faculty/')
#     except KeyError:
#         return redirect('/faculty/')  # Redirect if session variable doesn't exist
#     zprn = request.session['ZPRN'] 

#     if request.method == 'POST':
#         try:
#             row = Question.objects.get(id=q_id)
#             sn = Exam_sub.objects.get(Subject= row.sub)
#             sid = sn.id
#             qid = row.id
#             row.delete()
#             messages.success(request, f' question of id: {qid} has been deleted successfully.')
#         except :
#             messages.success(request, f' question of id: {qid} has been not deleted something is wrong.')
#         url = f'/faculty/add-question/{sid}'
#     return render(request, url, {'zprn': zprn})

def deleteQue(request, q_id):
    try:
        if request.session['ZPRN'] is None:
            return redirect('faculty/')
    except KeyError:
        return redirect('/faculty/')  # Redirect if session variable doesn't exist

    zprn = request.session['ZPRN']

    if request.method == 'POST':
        # Attempt to retrieve the question
        row = get_object_or_404(Question, id=q_id)
        sn = get_object_or_404(Exam_sub, Subject=row.sub)
        sid = sn.id
        
        try:
            del_queno= row.ques_no
            row.delete()
            # logic to update question no
            que_row = Question.objects.filter(ques_no__gt= del_queno, sub=sn.Subject)
            
            for r in que_row:
                r.ques_no -= 1
                r.save()
            messages.success(request, f'Question of ID: {q_id} has been deleted successfully.')
        except Exception as e:
            messages.error(request, f'Failed to delete question of ID: {q_id}. Error: {str(e)}')

        return redirect(f'/faculty/add-question/{sid}')

    # If not a POST request, you might want to render a confirmation page or similar
    return render(request, 'your_template.html', {'zprn': zprn, 'question_id': q_id})




def logout(request):
    try:
        del request.session['ZPRN']  # Replace 'key_name' with the actual key
        return redirect('/faculty/') 
    except :
        print('call')
        return redirect('/faculty/') 