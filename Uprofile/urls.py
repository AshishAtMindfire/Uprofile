from django.conf.urls import url

from . import views

app_name= 'Uprofile'

urlpatterns = [
		url(r'^$',views.index,name='entry')
]