from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Uprofile.forms import LoginForm, RegisterForm, PasswordResetForm, ChangePasswordForm
from django.core.mail import send_mail
from django.urls import reverse
import hashlib


# Create your views here.
def index(request,errorcode=None):
	errors = None
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('Uprofile:show'))
	else:
		if str(errorcode) == '1':
			errors = "This account is currently disabled. Contact the site administrator."
		elif str(errorcode) == '2':
			errors = "Login failed. Invalid details"
		elif str(errorcode) == '3':
			errors = "Validation failed. Something nasty is going on. Mail send to administrator."
		elif str(errorcode) == '4':
			errors = "Mischivous Usage..."

		context = {'lform':LoginForm(),"rform": RegisterForm(),'errors':errors}
		return render(request,'Uprofile/index.html',context)



def login(request):
	print ('u entered login')
	if request.method == 'POST':
		login_details = LoginForm(request.POST)
		if login_details.is_valid():
			#if request.POST.get('name_user') and request.POST.get('pass_key'):
			#	if request.POST['name_user'].strip() != '' and request.POST['pass_key'].strip() != '':
			#		pass # check for user login credentials
			details = login_details.cleaned_data
			username = details.get('username')
			password = details.get('password')
			current_user = authenticate(username=username,password=password)
			if current_user is not None:
				if current.is_active:
					login(request,current_user)
					return HttpResponseRedirect(reverse('Uprofile:show'))
				else:
					#the user is disabled
					errors = "This account is currently disabled. Contact the site administrator."
			else:
				errors = "Login failed. Invalid details"
				
		else:
			errors = "Validation failed. Something nasty is going on. Mail send to administrator."
	else: 
		errors = "Mischivous Usage..."
	print('checkpoint 1 reached!!')
	return redirect('/Uprofile/index') 



def register(request):
	if request.method ==  "POST":
		register_details = RegisterForm(request.POST)
		if register_details.is_valid():
			details = register_details.cleaned_data
			username = details['username']
			password = details['password']
			user_email = details['email']
			first_name = details['fname']
			last_name = details['lname']
			user = User.objects.create_user(username,user_email,password)
			user.first_name = first_name
			user.last_name = last_name
			user.is_active = False
			user.save()
			activation_key = hashlib.md5(user.username.encode()).hexdigest()



	else:
		errors = ""
		return HttpResponseRedirect(reverse('Uprofile:index'))





def show(request,username):
	return HttpResponse('this is a test view')
	if request.user.is_authenticated():
		
		return render(request,"Uprofile/show.html",context)
	else:
		return render(request,"Uprofile/not_allowed.html",{})



# View for forgot password
def forgot_pass(request):
	context = {'form': PasswordResetForm() }
	return render(request,'Uprofile/forgot.html',context)



def changepassword(request):
	 context = {'form' : ChangeResetForm() }
	 return render(request,"Uprofile:Changepassword",context)

# Logout View
def logout(request):
	name = None
	context = { 'name': name }
	if request.user.is_authenticated():
		name = request.user.get_full_name()
		logout(request.user)
		return render(request,'Uprofile/logout.html',context)
	else:
		return render(request,"Uprofile/logout.html",context)


def testing(request,errors):
	return HttpResponse('this is a test view')
