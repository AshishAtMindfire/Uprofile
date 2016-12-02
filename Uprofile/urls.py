from django.conf.urls import url

from . import views

app_name= 'Uprofile'

urlpatterns = [
		url(r'^$',views.MyIndexView.as_view(),name='index'),
		url(r'^login/$',views.MyLoginView.as_view(),name='login'),
		url(r'^logout/$',views.MyLogoutView.as_view(),name='logout'),
		url(r'^register/$',views.MyRegisterView.as_view(),name='register'),
		url(r'^activate/(?P<key>.+)$', views.MyActivationView.as_view(),name='activation'),
		url(r'^changepassword/$',views.MyChangePasswordView.as_view(),name='changepassword'),
		url(r'^show/$',views.show,name='show'),
		url(r'^forgot/$',views.MyForgotView.as_view(),name="forgot"),
		url(r'^forgot/(?P<key>.+)$',views.MyResetPasswordView.as_view(),name="reset"),

]