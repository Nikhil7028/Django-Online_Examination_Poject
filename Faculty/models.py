from django.db import models
from Student.models import StudInfo
# Create your models here.
class FacultyLogin(models.Model):
    ZPRN = models.CharField(max_length=10, unique=True)
    FullName = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=7)
    email = models.EmailField(unique=True)
    mobNo = models.CharField(max_length=14)

# table of exam subject
class Exam_sub(models.Model):
    Subject = models.CharField(max_length=10, unique=True)
    exam_time_min = models.IntegerField()

# question table
class Question(models.Model):
    ques_no = models.IntegerField()
    img = models.ImageField(upload_to='q_img/', default=None)
    ques = models.CharField(max_length=600)
    opt1 = models.CharField(max_length=200)
    opt2 = models.CharField(max_length=200)
    opt3 = models.CharField(max_length=200, default=None)
    opt4 = models.CharField(max_length=200, default=None)
    ans = models.CharField(max_length=201)
    sub = models.CharField(max_length=11)
    ques_setter = models.CharField(max_length=51)
    full_name = models.CharField(max_length=50)

class ExamSubmission(models.Model):
    rollno = models.CharField(max_length=10)
    ques_id = models.IntegerField()
    selected_ans = models.CharField(max_length=200, default=None)
    exam_sub = models.CharField(max_length=11)
    submitted_at = models.DateTimeField(auto_now_add=True)

    
