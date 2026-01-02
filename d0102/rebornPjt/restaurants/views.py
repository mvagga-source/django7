from django.shortcuts import render
from django.http import HttpResponse

def reslist(request):
    
    return render(request,'restaurants/reslist.html')
