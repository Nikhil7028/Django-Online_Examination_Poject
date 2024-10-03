from django.shortcuts import redirect, render
from django.http import HttpResponse
from Student.models import StudInfo, exam_result
from Faculty.models import Exam_sub, Question, ExamSubmission
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.conf import settings
from django.contrib.sessions.models import Session


from django.utils import timezone


# Create your views here.

def registration(request):
    if request.method== 'POST':
        data={}
        try: 
            r = request.POST.get('rollno')
            fn = request.POST.get('fname')
            ln = request.POST.get('lname')
            g = request.POST.get('gender')
            ins = request.POST.get('instit')
            co = request.POST.get('course')
            mob = request.POST.get('mobno')
            mail = request.POST.get('email')
            passw = request.POST.get('psw')
            registration = StudInfo(rollNo=r, firstName=fn, lastName=ln,  gender=g, institute=ins, 
                    course=co, mobNo=mob, email=mail,  password= passw) 
            registration.save()
            data={ 'cls':'success' , 'st':'Sucessfully', 'msg': '{} {} your registration is submitted'.format(fn,ln)

            }
        except  Exception as e:
             data={ 'cls':'danger' , 'st':'ERROR', 
                   'msg': e 
            }
        return render(request, 'Register.html', data)

    return render(request, 'Register.html')

# Login in for student
def login(request):
    if request.method == 'POST':
        rollno = request.POST['rollno']
        pwd = request.POST['pass']
        data = {}
        try:
            # Try to get a single FacultyLogin object
            strow = StudInfo.objects.get(rollNo=rollno)
            # Now check the ZPRN and password
            if strow.rollNo == rollno and strow.password == pwd: # Ideally, compare hashed passwords
                    request.session['rollno'] = strow.rollNo
                    print('hi Nikhil')
                    return redirect('/home/')
            else:
                data = {'error': 'Invalid rollno or password please try again'}
        except StudInfo.DoesNotExist:
            # Handle the case when the faculty login is not found
            data = {'error': "Your account Does Not Exist. First create account"}
        # Render the form with the error
        return render(request, 'index.html', data)
    return render(request, 'index.html')

# after login student home
def home(request):
    # if session is not set
    try:    
        if request.session['rollno'] is None :
            return redirect('/')
    except:
        return redirect('/')
    
    try:
        rollno = request.session['rollno']
        sr= StudInfo.objects.get(rollNo= rollno)
        sf = sr.firstName #student first name
        sl = sr.lastName    #student last name
    except Exception as e:
        sf = None
        sl = e   
        rollno = None
    dict={ 'rollno': rollno, 'sf': sf, 'sl': sl}
    return render(request, 'Home.html', dict)

# select the subject foe exam 

def selectSub(request):
    # Check if the session is set
    if 'rollno' not in request.session:
        return redirect('/')

    subs = Exam_sub.objects.all()

    cscolor = ['#ff0000', '#3cb371', '#0000ff', '#ffa500', '#ee82ee', '#6a5acd', '#0100ff']
    color_count = len(cscolor)

    return render(request, 'select_sub.html/', {
        'rollno': request.session['rollno'],
        'subs': subs,
        'colors': cscolor,
        'color_count': color_count,
    })


def instruction(request, sid):
    # Ensure the user is logged in
    if not request.session.get('rollno'):
        return redirect('/')  # Redirect to login page if not logged in

    # Fetch exam subject and time based on subject id
    try:
        exam_subject = Exam_sub.objects.get(id=sid)
    except Exam_sub.DoesNotExist:
        Exam_sub.error(request, "Invalid Subject ID")
        return redirect('select_sub')  # Redirect if subject does not exist
    
    # Store exam start flag in session
    request.session['exam_start'] = 'yes'
    
    context = {
        'user': request.session['rollno'],
        'subject': exam_subject.Subject,
        'exam_time': exam_subject.exam_time_min
    }
    
    return render(request, 'instruction.html', context)



# set_exam_type_session

def set_exam_type_session(request):
    if request.method == "GET":
        exam_category = request.GET.get('exam_category')

        # Store exam_category in session
        request.session['exam_category'] = exam_category

        # Query the database for the exam subject
        try:
            # Get exam details from the database
            exam_subject = Exam_sub.objects.get(Subject=exam_category)
            exam_time = exam_subject.exam_time_min  # Duration in minutes

            # Get the current time (timezone-aware)
            start_time = timezone.localtime(timezone.now())  # Get local time based on TIME_ZONE

            # Calculate the end time by adding the exam duration (in minutes)
            end_time = start_time + timedelta(minutes=exam_time)

            # Store end_time and exam duration in the session
            request.session['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
            request.session['exam_start'] = True  # This can be used to track if the exam has started

            # Optionally, store exam duration if you need it later
            request.session['exam_duration'] = exam_time

        # Return a success response (for an AJAX request or page load)
            return JsonResponse({'status': 'success', 'message': 'Exam session set', 'end_time': request.session['end_time']})
        except Exam_sub.DoesNotExist:
            # Handle the case where the subject doesn't exist
            return JsonResponse({'status': 'error', 'message': 'Exam category not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



# for exam paper
# def exampaper(request, sub):
#     if 'rollno' not in request.session:
#         return redirect('/')
#     min = Exam_sub.objects.get(Subject= sub).exam_time_min
#     hours = min // 60
#     remaining_minutes = min % 60
#     seconds = 0  # Assuming we want seconds as 0

#     # Format as hh:mm:ss
#     hhmmss = f"{hours:02}:{remaining_minutes:02}:{seconds:02}"

#     setSession(sub)
    
#     dict={
#         'sub': sub, 'rollno' : request.session['rollno'], 'time':hhmmss
#     }
#     return render(request, 'exam_paper.html', dict)


# exam page realted function  

def exam_paper(request):
    if not request.session.get('rollno'):
        return redirect('/')  # Redirect to login page if not logged in
    subj = request.session['exam_category']
    questions = Question.objects.filter(sub=subj).order_by('ques_no')
    rollno = request.session['rollno']

    if request.method == 'POST':        
        for ques in questions:
            selected_option = request.POST.get(f'selected_opt_{ques.id}')  # Adjust to match your radio button names
            if selected_option:
                # Save to ExamSubmission
                ExamSubmission.objects.create(
                    rollno=rollno,
                    ques_id=ques.id,
                    selected_ans=selected_option,
                    exam_sub = subj
                )
                print('Saved: Question ID:', ques.id, 'Selected Option:', selected_option)
        
        return redirect('result') 

    return render(request, 'exam_paper.html', {'questions': questions,  'rollno': rollno, 'subj': subj})

    # sub= request.session['exam_category']
    # user = request.user.username
    # sub = request.session.get('exam_category', None)
    # if not sub:
    #     return redirect('index')  # Redirect to index if no category found
    # return render(request, 'exam_paper.html', {'user': user, 'sub': sub})
# def result(request): 
    if not request.session.get('rollno'):
        return redirect('/')  # Redirect to login page if not logged in
    rollno = request.session['rollno']
    subj = request.session['exam_category']
    examSubmit = ExamSubmission.objects.filter(exam_sub= subj, rollno= rollno).order_by('ques_id')
    questions = Question.objects.filter( id__in=ExamSubmission.objects.filter(exam_sub=subj, rollno=rollno).values('ques_id') ).order_by('ques_no')

    
    return render(request, 'results.html', {'rollno': rollno, 'subj': subj, 'questions': questions})

# for result
def result(request): 
    if not request.session.get('rollno'):
        return redirect('/')  # Redirect to login page if not logged in
    
    rollno = request.session['rollno']
    subj = request.session['exam_category']

    # Get the submitted answers for the given subject and roll number
    exam_submissions = ExamSubmission.objects.filter(exam_sub=subj, rollno=rollno).order_by('ques_id')
    
    # Get the questions corresponding to those submissions
    questions = Question.objects.filter(
        id__in=exam_submissions.values('ques_id')
    ).order_by('ques_no')

    # Prepare a list of results combining questions and selected answers
    results = []
    try:
        for question in questions:
            
            # Find the corresponding submission for the question
            submission = exam_submissions.get(ques_id=question.id, rollno=rollno)
            q = Question.objects.get(id = question.id)
            
            
            results.append({
                'question': question,
                'selected_answer': submission.selected_ans,
                'correct_answer': q.ans,  # Assuming this is the field name for the correct answer

            })
    except Exception as e:
        print(e)
        results.append({'error': str(e)})
        
    
    # Count the number of attempted questions
    attempq = len(results)
    ttlq= Question.objects.filter(sub=  subj).count()

    #insert the marks in result table
    correctans = 0
    for result in results:
        if result.get('selected_answer') == result.get('correct_answer'):  # Correct dictionary access
            correctans += 1

    try :
        # 'exam_sub', 'total_ques', 'correct_ans', 'wrong_ans', 'exam_endtime']  
        erobj = exam_result(rollno=rollno, exam_sub=subj, total_ques=ttlq,  correct_ans= correctans, wrong_ans= ttlq - correctans ) 
        erobj.save()
    except Exception as e:
        print(e)
        results.append({'error': str(e)})

    # delete the session
    try:
        del request.session['exam_category']  # delete the session exam category
    except Exception as e :
        print(e)
     
    return render(request, 'results.html', {
        'rollno': rollno,
        'subj': subj,
        'results': results,
        'attempq':  attempq,
        'ttlq': ttlq

    })


def load_total_que(request):
    exam_category = request.session.get('exam_category')
    if exam_category:
        total_que = Question.objects.filter(sub=exam_category).count()
    else:
        total_que = 0  # Default to 0 if no exam category in session
    return JsonResponse(total_que, safe=False)

def load_questions(request):
    questionno = request.GET.get('questionno', 1)
    # Fetch question based on number
    subj = request.session.get('exam_category')

    # Use get() if you are sure only one question exists for a given ques_no and sub
    try:
        ques = Question.objects.get(sub=subj, ques_no=questionno)
        question = {
            "id": ques.ques_no,
            "text": ques.ques,
            "image_url": ques.img if ques.img else None,
            "options": [ques.opt1, ques.opt2, ques.opt3, ques.opt4]

        }
    except Question.DoesNotExist:
        # Handle case where no question is found
        question = {
            "error": "Question not found"
        }
    except Exception as e:
        question = {
            "text": e
        }
    print(question['image_url'])


    return JsonResponse(question)


def save_ans_in_session(request):
    questionno = request.GET.get('questionno')
    radiovalue = request.GET.get('value1')
    request.session[f'answer_{questionno}'] = radiovalue
    return JsonResponse({'status': 'saved'})


def load_timer(request):
    end_time = request.session.get('end_time', None)  # Retrieve end time from session
    print('end timing')
    print(end_time)

    if not end_time:
        return JsonResponse({"time": "00:00:00"})  # Return structured JSON with time

    # Convert session end_time to datetime and calculate the difference
    current_time = datetime.now()
    end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    time_diff = (end_time_obj - current_time).total_seconds()

    if time_diff <= 0:
        return JsonResponse({"time": "00:00:00"})  # Time over
    else:
        remaining_time = datetime.utcfromtimestamp(time_diff).strftime("%H:%M:%S")
        return JsonResponse({"time": remaining_time}) 

def setSession(request, sub):
    try:
        request.session['sub'] = sub
        request.session['exam_time'] = Exam_sub.objects.get(Subject=sub).exam_time_min
        exam_time_minutes = request.session.get('exam_time', 0)
    
        # Convert the minutes into a timedelta object
        exam_duration = timedelta(minutes=exam_time_minutes)

        # Format the timedelta as hh:mm:ss
        hours, remainder = divmod(exam_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        start_time_formatted = f"{hours:02}:{minutes:02}:{seconds:02}"

        # Store the formatted time in the session as 'start_time'
        request.session['start_time'] = start_time_formatted
        request.session['end_time'] =   ''
    except:
        pass


    
def oldExamRes(request):
    if not request.session.get('rollno'):
        return redirect('/')
    rollno = request.session['rollno']
    sr= StudInfo.objects.get(rollNo= rollno)
    sf = sr.firstName #student first name
    sl = sr.lastName    #student last name
    res = exam_result.objects.filter(rollno= rollno)

    return render(request, 'old_exam_res.html', {'rollno': rollno, 'sf':sf, 'sl':sl, 'institute': sr.institute, 'course':sr.course, 'results': res })




def logout(request):
    try:
        Session.object.all().delete()
        del request.session['rollno']  # Replace 'key_name' with the actual key
        return redirect('/') 
    except :
        print('call')
        return redirect('/') 
