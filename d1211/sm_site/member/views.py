from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.urls import reverse

# Create your views here.

def logout(request):
    
    # del request.session['session_id']
    request.session.clear()
    context = {"error":"-1"}
    return render(request,'member/login.html',context)

# 회원 로그인
def login(request):
    if request.method == "GET":
        
        cook_id = request.COOKIES.get("cook_id","")
        context = {"cook_id":cook_id}
        
        return render(request,'member/login.html', context)
    elif request.method == "POST":
        
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        cook_keep = request.POST.get("cook_keep")
        print("post input...",id,pw)
        
        qs = Member.objects.filter(id=id,pw=pw)
        # qs = Member.objects.get(id=id,pw=pw).DoesNotExist
        if qs:
            
            print("아이디와 비밀번호가 일치합니다.")
            
            # 세션설정
            # 저장
            request.session['session_id'] = id
            
            context = {"error":"1"}
            response = render(request,'member/login.html',context)
            
            # 쿠키설정
            if cook_keep:
                # 저장
                response.set_cookie("cook_id",id,max_age=60*60*24*30)
            else:
                # 삭제
                response.delete_cookie("cook_id")
            
            return response
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