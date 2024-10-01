from django.shortcuts import redirect, render
from django.http import HttpResponse
from Student.models import StudInfo
from Faculty.models import Exam_sub, Question
from datetime import timedelta

from django.http import JsonResponse
from django.conf import settings


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

# instruction page
def instruction(request, sid):
    if 'rollno' not in request.session:
        return redirect('/')
    
    dict={}
    try:
        subs = Exam_sub.objects.get(id= sid)
        sn = subs.Subject
        time = subs.exam_time_min
        qcount = Question.objects.filter(sub= sn).count()
        attemp= True
        if qcount==0:
            attemp= False        

        # student info
        dict={
            'sn': sn, 'time': time, 'qcount':qcount , 'rollno': request.session['rollno'], 
            'sid': sid, 'attemp': attemp
        }
    except Exception as e:
        print(e)

    return render(request, 'instruction.html', dict)

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
    user = request.user.username
    sub = request.session.get('exam_category', None)
    
    if not sub:
        return redirect('index')  # Redirect to index if no category found
    
    return render(request, 'examapp/exam_paper.html', {'user': user, 'sub': sub})

def load_total_que(request):
    # Assuming you're calculating total questions dynamically
    total_questions = 10  # Replace with your logic
    return JsonResponse(total_questions, safe=False)

def load_questions(request):
    questionno = request.GET.get('questionno', 1)
    # Fetch question based on number
    question = {
        "id": questionno,
        "text": "This is question {}".format(questionno),
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"]
    }
    return JsonResponse(question)

def save_ans_in_session(request):
    questionno = request.GET.get('questionno')
    radiovalue = request.GET.get('value1')
    request.session[f'answer_{questionno}'] = radiovalue
    return JsonResponse({'status': 'saved'})

def load_timer(request):
    # Implement timer logic, hardcoded here for demonstration
    return JsonResponse('00:10:00', safe=False)


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


    




def logout(request):
    try:
        del request.session['rollno']  # Replace 'key_name' with the actual key
        return redirect('/') 
    except :
        print('call')
        return redirect('/') 
