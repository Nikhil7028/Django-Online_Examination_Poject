"""
URL configuration for OnlineEX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from OnlineEX import views
from Student import views as stud_views
from Faculty import views as fac_views
# for media files 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
   

    path('faculty/', fac_views.factLogin, name='facultylog'),
    path('faculty/home/', fac_views.home, name='home'),
    path('faculty/add-exam-category/', fac_views.addExamCategory, name='addSub'),
    path('faculty/delete-sub/<int:sub_id>', fac_views.deleteSub, name='deletesub'),
    path('faculty/edit-sub/<int:sub_id>/', fac_views.editSub, name='editSub'),

    path('faculty/selectSub/', fac_views.selectSub, name= 'selectSub'), # to select the subject to add question
    path('faculty/add-question/<int:sub_id>/', fac_views.addQues, name='addQues'),
    path('faculty/delete-que/<int:q_id>/', fac_views.deleteQue, name='deleteQue'),

    # Student side
    path('', stud_views.login, name='login'),   # student login
    path('stud-registration/', stud_views.registration),   #student registration
    path ('home/', stud_views.home, name='home'),
    path('select-sub/', stud_views.selectSub, name='selectSub'),
    path('instruction/<int:sid>/', stud_views.instruction, name='instruction'),

    # exam paper
    path('exampaper/<str:sub>/', stud_views.exampaper, name='exampaper'),
    path('logout/', stud_views.logout, name='slogout'),

    # exam page realated urls
    path('load_total_que/', stud_views.load_total_que, name='load_total_que'),
    path('load_questions/', stud_views.load_questions, name='load_questions'),
    path('save_ans_in_session/', stud_views.save_ans_in_session, name='save_ans_in_session'),
    path('load_timer/', stud_views.load_timer, name='load_timer'),
    
    path('faculty/logout/', fac_views.logout, name='flogout'),
    path('faculty/edit-que/<int:q_id>', fac_views.editQue, name='editQue'),
    path('index/', views.index),  
    path('ssession/',views.setsession),  
    path('gsession/',views.getsession)  
]  



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)



