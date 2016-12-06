from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import os


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10,default="")
    contact_mobile = models.IntegerField(null=True)
    addressline1 = models.CharField(max_length=30,default="")
    addressline2 = models.CharField(max_length=30,default="") 
    addressline3 = models.CharField(max_length=30,default="")
    pincode = models.IntegerField(null=True)
    education_level = models.CharField(max_length=30,default="")
    location = models.CharField(max_length=20,default="")




def user_directory_path(instance, filename):
    _,ext = os.path.splitext(filename)
    return 'profile_images/{0}/{1}'.format(instance.user.username,filename)


class DisplayImage(models.Model):
    user =  models.OneToOneField(User,on_delete = models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path,null=True,blank=True,editable=True)


class ForgotPass(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=60)
