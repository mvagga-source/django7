from django.shortcuts import render

# Create your views here.

def write(request):
    # render - html페이지 오픈
    return render(request,'write.html')