from django.conf.urls import url

from . import views

app_name= 'Uprofile'

urlpatterns = [
		url(r'^$',views.index,name='index'),
		url(r'^login/$',views.uprofile_login,name='login'),
		url(r'^logout/$',views.uprofile_logout,name='logout'),
		url(r'^register/$',views.register,name='register'),
		url(r'^activate/(?P<key>.+)$', views.activation,name='activation'),
		url(r'^changepassword/$',views.changepassword,name='changepassword'),
		url(r'^show/$',views.show,name='show'),
		url(r'^forgot/$',views.forgot,name="forgot"),
		url(r'^forgot/(?P<key>.+)$',views.resetpassword,name="reset"),

]