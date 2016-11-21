from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail


class LoginForm(forms.Form):
	username = forms.CharField(required=True,label='Username',min_length=8,max_length=25)
	password = forms.CharField(widget=forms.PasswordInput,label='Password',required=True,min_length=8,max_length=20)


class RegisterForm(forms.Form):
	fname = forms.CharField(max_length=15,label='First Name',widget=forms.TextInput(attrs = {'maxlength':'15'}))
	lname = forms.CharField(max_length=15,label='Last Name',widget=forms.TextInput(attrs = {'maxlength':'15'}))
	username = forms.CharField(max_length=25,min_length=8,label='Username',widget=forms.TextInput(attrs = {'maxlength':'25'}))
	email = forms.EmailField(label='Email')
	password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs = {'maxlength':'20'}),label='Password')
	cpassword = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs = {'maxlength':'20'}),label= 'Confirm Password')

	def clean_email(self):
		data = self.cleaned_data
		if User.objects.get(email= data['email']):
			raise ValidationError(_("this email is already registered !"))
		return data['email']


	def clean(self):
		data = self.cleaned_data
		password1 = data['password']
		password2 = data['cpassword']
		if password1 and password1 != password2:
			raise ValidationError(_('Passwords does not match !'))
		return data

	def save(self, datas):
		u = User.objects.create_user(datas['username'],datas['email'],datas['password1'])
		u.is_active = False
		u.save()
		profile=Profile()
		profile.user=u
		profile.activation_key=datas['activation_key']
		profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
		profile.save()
		return u

    #Sending activation email ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #The email is written in a text file (it contains templatetags which are populated by the method below)
	def sendEmail(self, datas):
		link="http:127.0.0.1/activate/"+datas['activation_key']
		c=Context({'activation_link':link,'username':datas['username']})
		f = open(MEDIA_ROOT+datas['email_path'], 'r')
		t = Template(f.read())
		f.close()
		message=t.render(c)
        #print unicode(message).encode('utf8')
		send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)



class PasswordResetForm(forms.Form):
	mail = forms.EmailField()




class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(min_length=8,max_length=50,label="Old Password",widget = forms.PasswordInput(attrs={}))
	new_password = forms.CharField(min_length=8,max_length=50,label="New Password",widget = forms.PasswordInput(attrs={}))
	confirm_password  = forms.CharField(min_length=8,max_length=50,label="Confirm Password",widget = forms.PasswordInput(attrs={}))

	def clean(self):
		password1 = self.cleaned_data.get('old_password')
		password2 = self.cleaned_data.get('new_password')
		if password1 and password1 != password2:
			raise ValidationError(("New Passwords dont match."))
		return self.cleaned_data
