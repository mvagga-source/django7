from django.shortcuts import render
from django.http import HttpResponse

def blist(request):
    return render(request,'board/blist.html')
