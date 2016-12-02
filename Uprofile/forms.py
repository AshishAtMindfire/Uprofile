from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail


class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=8,max_length=25,widget=forms.TextInput(attrs={ 'minlength':'8','maxlength':'25' }))
    password = forms.CharField(required=True,min_length=8,max_length=25,widget=forms.PasswordInput(attrs={'minlength':'8','maxlength':'25'}))


class RegisterForm(forms.Form):
    fname = forms.CharField(max_length=15,label='First Name',widget=forms.TextInput(attrs = {'maxlength':'15'}))
    lname = forms.CharField(max_length=15,label='Last Name' ,widget=forms.TextInput(attrs = {'maxlength':'15'}))
    username = forms.CharField(max_length=25,min_length=8,label='Username',widget=forms.TextInput(attrs = {'minlength':'8','maxlength':'25'}))
    email = forms.EmailField(label='Email')
    password  = forms.CharField(max_length=25,min_length=8,widget=forms.PasswordInput(attrs = {'minlength':'8','maxlength':'25'}),label='Password')
    cpassword = forms.CharField(max_length=25,min_length=8,widget=forms.PasswordInput(attrs = {'minlength':'8','maxlength':'25'}),label= 'Confirm Password')

    def clean_email(self):
        data = self.cleaned_data
        if User.objects.filter(email= data['email']):
            raise ValidationError(_("This email is already registered !"))
        return data['email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError(_("This username is already taken"))
        return username


    def clean(self):
        data = self.cleaned_data
        password1 = data['password']
        password2 = data['cpassword']
        if password1 and password1 != password2:
            raise ValidationError(_('Passwords does not match !'))
        return data


    #Sending activation email ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #The email is written in a text file (it contains templatetags which are populated by the method below)
    def sendEmail(self,data):
        link = "http:127.0.0.1:8000/Uprofile/activate/" + data ['activation_key']
        subject = "Uprofile : Activate your account"
        message = "Dear User, \n Use the below link to activate your account on Uprofile\n\n %s  \n\n Regards\n Uprofile team." % (link)
        #print unicode(message).encode('utf8')
        print('sending mail')
        send_mail(subject, message, 'urofileteam@gmail.com', [data['email']], fail_silently=False)



class PasswordResetForm(forms.Form):
    mail = forms.EmailField(label="",widget=forms.EmailInput)

    def sendEmail(self,data):
        link = "http:127.0.0.1:8000/Uprofile/forgot/" + data ['key']
        subject = "Uprofile : Password reset request "
        message = "Dear User, \n Use the below link to reset your account's password on Uprofile\n\n   %s   \n\n Regards\n Uprofile team." % (link)
        #print unicode(message).encode('utf8')
        print('sending mail')
        send_mail(subject, message, 'urofileteam@gmail.com', [data['email']], fail_silently=False)


class ResetForm(forms.Form):

    new_password = forms.CharField(min_length=8,max_length=50,label="New Password",widget = forms.PasswordInput(attrs = {'minlength':'8','maxlength':'25'}))
    confirm_password  = forms.CharField(min_length=8,max_length=50,label="Confirm Password",widget = forms.PasswordInput(attrs={'minlength':'8','maxlength':'25'}))

    def clean(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password1 != password2:
            raise ValidationError(_("New Passwords dont match."))
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(min_length=8,max_length=50,label="Old Password",widget = forms.PasswordInput(attrs={'minlength':'8','maxlength':'25'}))
    new_password = forms.CharField(min_length=8,max_length=50,label="New Password",widget = forms.PasswordInput(attrs={'minlength':'8','maxlength':'25'}))
    confirm_password  = forms.CharField(min_length=8,max_length=50,label="Confirm Password",widget = forms.PasswordInput(attrs={'minlength':'8','maxlength':'25'}))

    def clean(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 and password1 != password2:
            raise ValidationError(_("New Passwords dont match."))
        return self.cleaned_data

class UploadDisplayPicture(forms.Form):
    image = forms.ImageField()