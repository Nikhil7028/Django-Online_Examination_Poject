from django.contrib import admin
from Student.models import StudInfo, exam_result
# Register your models here.
class resAdmin(admin.ModelAdmin):
    list_display =[ 'id', 'rollNo', 'firstName', 'lastName',  'gender', 'institute', 
                   'course', 'mobNo', 'email',  'password', 'regDate',  'verifyStatus'  
                   ]        

class resuttblcls(admin.ModelAdmin):
    list_display = ['id', 'rollno', 'exam_sub', 'total_ques', 'correct_ans', 'wrong_ans', 'exam_endtime']  

admin.site.register(StudInfo, resAdmin)
admin.site.register(exam_result, resuttblcls)