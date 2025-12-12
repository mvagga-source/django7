from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

def login(request):
    
    if request.method == "GET":
        
        # 쿠키 검색
        cooksave_id = request.COOKIES.get("cooksave_id","")
        context = {"cooksave_id":cooksave_id}
        return render(request,'member/login.html', context) # => HttpResponse 객체 생성

    
    
    elif request.method == "POST":
        
        # 쿠키저장        
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        login_keep = request.POST.get("login_keep")
        
        # print('login_keep ', login_keep)

        # response 정의
        response = redirect("/") # url방식, response = redirect("index") # 앱방식

        if login_keep:
            response.set_cookie("cooksave_id",id,max_age=60*60*24*30) # key, value
        else:
            response.delete_cookie("cooksave_id")

        return response
