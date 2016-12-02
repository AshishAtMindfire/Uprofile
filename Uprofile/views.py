from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from Uprofile.forms import LoginForm, RegisterForm, PasswordResetForm, ResetForm, ChangePasswordForm
from django.urls import reverse
from django.utils import timezone
import hashlib
from .models import Profile, ForgotPass 
import datetime
from django.views import View

# Creating IndexView here

class MyIndexView(View):

    template_name = "Uprofile/index.html"

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Uprofile:show'))
        context = {'username':request.user.username}
        return render(request, self.template_name,context)


'''
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('Uprofile:show'))
    else:
        context = {'username':request.user.username}
        return render(request,'Uprofile/index.html',context)
'''


class MyRegisterView(View):

    form_class = RegisterForm
    template_name =  'Uprofile/register.html'

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Uprofile:show'))
        return render(request,self.template_name,{ 'form': self.form_class() })


    def post(self,request):

        register_details = RegisterForm(request.POST)
        if register_details.is_valid():
            details = register_details.cleaned_data

            details['activation_key'] = self.generatekey(details['username'])
            details['key_expires'] = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
            
            # sending mail
            register_details.sendEmail(details)
            
            # Registering user account
            user = User.objects.create_user(username=details['username'], email=details['email'], password = details['password'])
            user.first_name = details['fname']
            user.last_name = details['lname']
            user.is_active = False
            user.save()

            # Using Profile model to store the activation key and expiry time
            profile =  Profile(user = user, activation_key = details['activation_key'], key_expires = details['key_expires'])
            profile.save()
            return render(request, self.template_name, {'name':details['fname'],'email':details['email']})

        context = { 'errors' : "Validation failed !!", 'form': register_details }
        return render(request,self.template_name,context)


    def generatekey(self,username):

        return hashlib.md5(username.encode()).hexdigest()


"""
def register(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('Uprofile:show'))

    register_details = RegisterForm()
    if request.method ==  "POST":
        register_details = RegisterForm(request.POST)
        if register_details.is_valid():
            details = register_details.cleaned_data
            username = details['username']
            password = details['password']
            user_email = details['email']
            first_name = details['fname']
            last_name = details['lname']
            details['activation_key'] = hashlib.md5(username.encode()).hexdigest()
            details['key_expires'] = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
            print("sending mail")
            register_details.sendEmail(details)
            user = User.objects.create_user(username=username,email=user_email,password = password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            print("User saved")

            # Using Profile model to store the activation key and expiry time
            profile =  Profile()
            profile.user = user
            profile.activation_key =  details['activation_key']
            profile.key_expires =  details['key_expires']
            profile.save()
            return render(request,"Uprofile/register.html",{'username':details['username'],'email':details['email']})
    
    context = { 'form' : register_details }
    return render(request,'Uprofile/register.html',context)

"""


class MyActivationView(View):

    template_name = 'Uprofile/activation.html'

    def get(self,request,key):

        Invalid_url = False 
        activation_expired = False
        already_active = False
        try:
            profile = Profile.objects.get(activation_key=key)
        except Profile.DoesNotExist :
            Invalid_url = True
        else:
            if profile.user.is_active == False:
                if timezone.now() > profile.key_expires:
                    activation_expired = True #Display: offer the user to send a new activation link
                    id_user = profile.user.id
                else: #Activation successful
                    profile.user.is_active = True
                    profile.user.save()
                    profile.delete()

            else:
                already_active = True
        return render(request, self.template_name, locals())


"""
def activation(request, key):

    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if timezone.now() > profile.key_expires:
            activation_expired = True #Display: offer the user to send a new activation link
            id_user = profile.user.id
        else: #Activation successful
            profile.user.is_active = True
            profile.user.save()

    else:
        already_active = True
    return render(request, 'Uprofile/activation.html', locals())
"""
class MyLoginView(View):

    form_class = LoginForm
    template_name = "Uprofile/login.html"

    def get(self,request):

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Uprofile:show'))

        context = { 'form' : self.form_class() }
        return render(request, self.template_name, context)

    def post(self,request):
        login_details = LoginForm(request.POST)
        context = {}
        if login_details.is_valid():
            #if request.POST.get('name_user') and request.POST.get('pass_key'):
            #   if request.POST['name_user'].strip() != '' and request.POST['pass_key'].strip() != '':
            #       pass # check for user login credentials
            details = login_details.cleaned_data
            username = details.get('username')
            password = details.get('password')
            current_user = authenticate(username=username,password=password)
            if current_user is not None:
                if current_user.is_active:
                    login(request,current_user)
                    return HttpResponseRedirect(reverse('Uprofile:show'))
                else:
                    #the user is disabled
                    errors = "This account is not activated. Please activate it first."
            else:
                errors = "Login failed. Invalid details"
                
        else:
            errors = "Validation failed. Something nasty is going on. Mail send to administrator."
    
        context['form'] = LoginForm()
        context['errors'] = errors
        return render(request, self.template_name, context)



"""
def uprofile_login(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('Uprofile:show'))


    context = {}
    errors = None
    if request.method == 'POST':
        login_details = LoginForm(request.POST)
        if login_details.is_valid():
            #if request.POST.get('name_user') and request.POST.get('pass_key'):
            #   if request.POST['name_user'].strip() != '' and request.POST['pass_key'].strip() != '':
            #       pass # check for user login credentials
            details = login_details.cleaned_data
            username = details.get('username')
            password = details.get('password')
            print(username,password)
            current_user = authenticate(username=username,password=password)
            print ('authentication done : ',current_user)
            if current_user is not None:
                if current_user.is_active:
                    login(request,current_user)
                    return HttpResponseRedirect(reverse('Uprofile:show'))
                else:
                    #the user is disabled
                    errors = "This account is not activated. Please activate it first."
            else:
                errors = "Login failed. Invalid details"
                
        else:
            errors = "Validation failed. Something nasty is going on. Mail send to administrator."
    
    context['form'] = LoginForm()
    context['errors'] = errors
    return render(request,"Uprofile/login.html",context) 
        
"""


def show(request):
    if request.user.is_authenticated():
        context = {'username':request.user.username}
        return render(request,"Uprofile/show.html",context)
    else:
        return render(request,"Uprofile/not_allowed.html",{})



# View for forgot password

class MyForgotView(View):

    form_class = PasswordResetForm
    template_name = "Uprofile/forgot.html"

    def get(self,request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Uprofile:show'))
        form = PasswordResetForm() 
        return render(request,self.template_name,locals())


    def post(self,request):
        request_accepted = False
        not_registered = False
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            if len(User.objects.filter(email=form.cleaned_data['mail'])):
                user = User.objects.filter(email=form.cleaned_data['mail'])[0]
                code = user.username + str( datetime.datetime.now().timestamp )
                key = hashlib.md5(code.encode()).hexdigest()
                data = { 'key' : key , 'email': form.cleaned_data['mail']}
                form.sendEmail(data)
                x = ForgotPass()
                x.user = user
                x.key = data['key']
                x.save()
                request_accepted = True
            else:
                not_registered = True   #"The given email address is not registered." 

        return render(request, self.template_name, locals())

"""
def forgot(request):
    request_accepted = False
    not_registered = False
    form = PasswordResetForm() 
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            if len(User.objects.filter(email=form.cleaned_data['mail'])):
                user = User.objects.filter(email=form.cleaned_data['mail'])[0]
                code = user.username + str( datetime.datetime.now().timestamp )
                key = hashlib.md5(code.encode()).hexdigest()
                data = { 'key' : key , 'email': form.cleaned_data['mail']}
                form.sendEmail(data)
                x = ForgotPass()
                x.user = user
                x.key = data['key']
                x.save()
                request_accepted = True
            else:
                not_registered = True   #"The given email address is not registered." 

    return render(request,'Uprofile/forgot.html',locals())
"""


class MyResetPasswordView(View):

    template_name = "Uprofile/reset.html"
    form_class = ResetForm


    def get(self,request,key):
        try:
            ForgotPassObj = ForgotPass.objects.get(key = key)
        except ForgotPass.DoesNotExist:
            context = { 'Invalid_url' : True }           
        else:
            context = { 'form' : self.form_class() }

        return render(request, self.template_name, context)


    def post(self,request,key):
        try:
            ForgotPassObj = ForgotPass.objects.get(key = key)
        except ForgotPass.DoesNotExist:
            context = { 'Invalid_url' : True }           
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                ForgotPassObj.user.set_password(form.cleaned_data['new_password'])
                ForgotPassObj.user.save()
                ForgotPassObj.delete()
                return render(request,"Uprofile/resetsuccess.html",{})
            else:
                context = {}
                context['errors'] = " Form Validation failed !"
                context['form'] = form
                
        return render(request, self.template_name, context)

"""
def resetpassword(request,key):
    ForgotPassObj = ForgotPass.objects.get(key = key)
    Invalid_url = False
    context = {}
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            ForgotPassObj.user.set_password(form.cleaned_data['new_password'])
            ForgotPassObj.user.save()
            return render(request,"Uprofile/resetsuccess.html",{})
        else:
            context['errors'] = " Form Validation failed !"

    context['form'] = ResetForm()
    #context['Invalid_url'] = True
    return render(request,'Uprofile/reset.html',context)
"""


class MyChangePasswordView(View):

    template_name = "Uprofile/changePassword.html"
    form_class = ChangePasswordForm


    def get(self,request):
        if request.user.is_authenticated():
            context = {'form' : self.form_class() , 'username' : request.user.username }
        else:
            context = {'not_allowed': True }
        return render(request, self.template_name, context)
        

    def post(self,request):
        context = {'form' : self.form_class()  }
        if request.user.is_authenticated():
            context['username'] =  request.user.username 
            form = self.form_class(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                old_password = data['old_password']
                new_password = data['new_password']
                if request.user.check_password(old_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    print("password changed!")
                    update_session_auth_hash(request,request.user)
                    return render(request,"Uprofile/change_successful.html",context)
                else:
                    context['errors'] = " Wrong Password !! "
            else:
                context['errors'] = "Form Validation failed ! "
        else:
            context['not_allowed'] = True

        return render(request, self.template_name, context)

"""
def changepassword(request):
    context = {'form' : ChangePasswordForm() , 'username' : request.user.username }
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                old_password = data['old_password']
                new_password = data['new_password']
                if request.user.check_password(old_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    print("password changed!")
                    return render(request,"Uprofile/change_successful.html",{})
                else:
                    context['errors'] = " Wrong Password !! "
            else:
                context['errors'] = "Form Validation failed ! "
    else:
        context['errors'] = "Your are not allowed to perform this action."
    return render(request,"Uprofile/changePassword.html",context)
"""



# Logout View


class MyLogoutView(View):

    template_name = "Uprofile/logout.html"
    
    def get(self,request):
        if request.user.is_authenticated():
            name = request.user.get_full_name()
            context = { 'name': name }
            logout(request)
        else:
            context = {}
        return render(request, self.template_name, context)
            

"""
def uprofile_logout(request):
    
    if request.user.is_authenticated():
        name = request.user.get_full_name()
        context = { 'name': name }
        logout(request)
        return render(request,'Uprofile/logout.html',context)
    else:
        return render(request,"Uprofile/logout.html",{})

"""