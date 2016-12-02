from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()


class DisplayImage(models.Model):
	user = models.OneToOneField(User,on_delete = models.CASCADE)
	image = models.ImageField(upload_to="profile_images/")

class ForgotPass(models.Model):
	user = models.ForeignKey(User)
	key = models.CharField(max_length=60)