from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def write(request):
    return render(request,'member/write.html')
    # return HttpResponse("write")