from django.contrib import admin
from Faculty.models import *
# Register your models here.

class Facultycls(admin.ModelAdmin):
    list_display=['id', 'ZPRN', 'FullName', 'password', 'gender', 'email', 'mobNo' ]

class ExamSub(admin.ModelAdmin):
    list_display = ['id', 'Subject', 'exam_time_min']



class Ques_admin(admin.ModelAdmin):
   list_display=['id', 'ques_no', 'ques','img', 'opt1', 'opt2', 'opt3', 'opt4', 'ans',  'sub', 'ques_setter']


admin.site.register(FacultyLogin, Facultycls)
admin.site.register(Exam_sub, ExamSub )
admin.site.register(Question, Ques_admin)
