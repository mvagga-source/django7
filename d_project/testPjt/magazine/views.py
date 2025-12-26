from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def mlist(request):
    return render(request,'magazine/mlist.html')
