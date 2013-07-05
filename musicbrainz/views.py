# Create your views here.


from django.http import HttpResponse

def home(request):
	if request.GET:
		return HttpResponse("Username found")
		# call username API
		# send to template that charts out each 
	else:
		return HttpResponse("No username.")