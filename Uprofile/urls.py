from django.conf.urls import url

from . import views

app_name= 'Uprofile'

urlpattern = [
		url(r'^$',views.index,name='entry')
]