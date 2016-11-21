from django.conf.urls import url

from . import views

app_name= 'Uprofile'

urlpatterns = [
		url(r'^$',views.index,name='index'),
		url(r'^.*$',views.index,name='loginreturn'),
		url(r'^login/$',views.login,name='login'),
		url(r'^register/$',views.register,name='register'),
		url(r'^show/$',views.show,name='show'),
		url(r'^forgot/$',views.forgot_pass,name="forgot"),
		url(r'^testing/',views.testing,name='testing')
]