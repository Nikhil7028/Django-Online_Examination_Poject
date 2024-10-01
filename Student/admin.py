from django.contrib import admin
from Student.models import StudInfo
# Register your models here.
class resAdmin(admin.ModelAdmin):
    list_display =[ 'id', 'rollNo', 'firstName', 'lastName',  'gender', 'institute', 
                   'course', 'mobNo', 'email',  'password', 'regDate',  'verifyStatus'  
                   ]          

admin.site.register(StudInfo, resAdmin)