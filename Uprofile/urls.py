from django.conf.urls import url

from . import views

app_name= 'Uprofile'

urlpatterns = [
		url(r'^$',views.index,name='index'),
		url(r'^login/$',views.login,name='login'),
		url(r'^register/$',views.register,name='register'),
		url(r'^activate/(?P<key>.+)$', views.activation,name='activation'),
		url(r'^changepassword/$',views.changepassword,name='changepassword'),
		url(r'^show/$',views.show,name='show'),
		url(r'^forgot/$',views.forgot_pass,name="forgot")
]