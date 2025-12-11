from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.urls import reverse

# Create your views here.

# 회원 로그인
def login(request):
    if request.method == "GET":
        return render(request,'member/login.html')
    elif request.method == "POST":
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        print("post input...",id,pw)
        
        qs = Member.objects.filter(id=id,pw=pw) # get : and, filter : or
        if qs:
            print("아이디와 비밀번호가 일치합니다.")
            context = {"error":"1"}
            return render(request,'member/login.html',context)
        else:
            print("아이디와 비밀번호가 일치하지 않습니다.")
            context = {"error":"0"}
            return render(request,'member/login.html',context)
        
        # return HttpResponse("post input...")


# 회원전체 리스트
def list(request):
    qs = Member.objects.all().order_by('-mdate')
    context = {"list":qs}
    return render(request,'member/list.html',context)

# 회원등록
def write(request):
    if request.method == "GET":
        return render(request,'member/write.html')
    elif request.method == "POST":
        
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        hobbys = request.POST.getlist('hobby')
        hobby = ','.join(hobbys)
        
        # qs = Member(id=id,pw=pw,name=name,phone=phone,gender=gender,hobby=hobby)
        # qs.save()
        Member.objects.create(
            id=id,pw=pw,name=name,phone=phone,gender=gender,hobby=hobby
        )
        
        print("post input..",id)
        # return HttpResponse("post input..")
        # return redirect(reverse('member:list')) # 앱이름 방식
        return redirect('/')