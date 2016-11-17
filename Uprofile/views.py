from django.shortcuts import render


# Create your views here.
def index(request):

	return render(request,)

def login(request):
	request.POST.get('name')

def register(request):
	return render(request,)

def show(request):
	return render(request,)