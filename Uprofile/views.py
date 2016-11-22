from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Uprofile.forms import LoginForm, RegisterForm, PasswordResetForm, ChangePasswordForm
from django.core.mail import send_mail
from django.urls import reverse
import hashlib
from .models import Profile
import datetime


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
    if request.method == 'POST':
        login_details = LoginForm(request.POST)
        if login_details.is_valid():
            #if request.POST.get('name_user') and request.POST.get('pass_key'):
            #   if request.POST['name_user'].strip() != '' and request.POST['pass_key'].strip() != '':
            #       pass # check for user login credentials
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
                    errors = "This account is not activated. Please activate it first."
            else:
                errors = "Login failed. Invalid details"
                
        else:
            errors = "Validation failed. Something nasty is going on. Mail send to administrator."
    else: 
        errors = "Mischivous Usage..."
    return redirect('/Uprofile/index') 
        

def register(request):
    print("Method : %s" % (request.method))
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
            user = User.objects.create_user(username,user_email,password)
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
            return render(request,"Uprofile/register.html",{'username':details['username'],'email':details['email'],'errors':None})
        else:
            errors = "some error!"
            return render(request,"Uprofile/register",{'errors':errors,'form':register_details})
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

    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
    return render(request, 'siteApp/activation.html', locals())

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

def testing(request,errors):
    return HttpResponse('this is a test view')
