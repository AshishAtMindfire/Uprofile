from django import forms


class LoginForm(forms.Form):
	name_user = forms.CharField(required=True)
	pass_key = forms.PasswordField(required=True)


class RegisterForm(forms.Form):
	fname = forms.CharField(max_length=15)
	lname = forms.CharField(max_length=15)
	name_user = forms.CharField(max_length=25)
	email = forms.EmailField()
	pass_key = forms.PasswordField()
	cpass_key = forms.PasswordField()
