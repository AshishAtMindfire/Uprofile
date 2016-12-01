from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Uprofile.forms import LoginForm, RegisterForm, PasswordResetForm, ResetForm, ChangePasswordForm
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
import hashlib
from .models import Profile, ForgotPass 
import datetime


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('Uprofile:show'))
    else:
        context = {}
        return render(request,'Uprofile/index.html',context)


def register(request):
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


def login(request):
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
        




def show(request):
    if request.user.is_authenticated():
        context = {}
        return render(request,"Uprofile/show.html",context)
    else:
        return render(request,"Uprofile/not_allowed.html",{})



# View for forgot password
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


def resetpassword(request,key):
    ForgotPassObj = ForgotPass.objects.get(key = key)
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
    return render(request,'Uprofile/reset.html',context)


def changepassword(request):
    context = {'form' : ChangePasswordForm() }
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
                    render(request,"Uprofile/change_successful",{})
            else:
                context['errors'] = "Form Validation failed ! "
    else:
        context['errors'] = "Your are not allowed to perform this action."
    return render(request,"Uprofile/changePassword.html",context)

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





'''
def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username']=user.username
        datas['email']=user.email
        datas['email_path']="/ResendEmail.txt"
        datas['email_subject']="Nouveau lien d'activation yourdomain"

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = datas['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key']= hashlib.sha1(salt+usernamesalt).hexdigest()

        profile = Profile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(datas)
        request.session['new_link']=True #Display: new link sent

    return redirect(home)
'''
def testing(request,errors):
    return HttpResponse('this is a test view')
