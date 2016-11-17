from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import *
# Create your views here.
def index(request):
	return render(request,'Uprofile/index.html',{})

def login(request):
	if request.POST.get('name_user') and request.POST.get('pass_key'):
		if request.POST['name_user'].strip() != '' and request.POST['pass_key'].strip() != '':
			pass # check for user login credentials
	return HttpResponseRedirect(reverse('Uprofile:show',args=(name_user)))

def register(request):
	if request.POST.get('fname') and request.POST.get('lname') and request.POST.get('name_user') \
			and request.POST.get('pass_key') and request.POST.get('cpass_key') and \
			request.POST.get('email'):
			pass #registration code here
	return render(request,"Uprofile/index.html",{})

def show(request):
	return render(request,"Uprofile/show.html",{})