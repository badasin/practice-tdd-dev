from django.shortcuts import render
# addition
# change to use templates instead
#from django.http import HttpResponse

# Create your views here.

def home_page(request):
	#return HttpResponse('<html><title>To-Do lists</title></html>')
	return render(request, 'home.html')


