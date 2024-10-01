from django.http import HttpResponse
from django.shortcuts import render
from Student.models import StudInfo

def home(request):
    return render(request,'index.html')

def index(request):
    return HttpResponse("OK") 

    

def setsession(request):  
    request.session['sname'] = 'irfan'  
    request.session['semail'] = 'irfan.sssit@gmail.com'  
    return HttpResponse("session is set")  
def getsession(request):  
    studentname = request.session['sname']  
    studentemail = request.session['semail']  
    return HttpResponse(studentname+" "+studentemail);  
