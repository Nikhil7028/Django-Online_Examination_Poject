from django.db import models
# Create your models here.
class StudInfo(models.Model):
    rollNo = models.CharField(max_length=10, unique=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    gender = models.CharField(max_length=7)
    institute = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    mobNo = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    regDate = models.DateTimeField(auto_now_add=True)
    verifyStatus = models.BooleanField(default=False)



