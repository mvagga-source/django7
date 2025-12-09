from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def write(request):
    # return HttpResponse('aa')
    return render(request,'write.html')
    