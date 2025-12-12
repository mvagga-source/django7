from django.shortcuts import render
from .models import Member
from django.http import HttpResponse

# 로그인 부분
def login(request):
    
    if request.method == "GET":
        
        cook_id = request.COOKIES.get("cook_id","")
        context = {"cook_id":cook_id}
        
        return render(request,'member/login.html',context)
    elif request.method == "POST":
        
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        login_keep = request.POST.get("login_keep")
        
        qs = Member.objects.filter(id=id,pw=pw)
        
        
        
        if qs:
            print("아이디, 비번 일치!")
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            
            context = {"state_code":"1"}
            
            response = render(request,'member/login.html',context)
            
            if login_keep:
                response.set_cookie("cook_id",id)
            else:
                response.delete_cookie("cook_id")

        else:
            print("아이디, 비번 불일치!")            
            context = {"state_code":"0"}
            
            response = render(request,'member/login.html',context)
        
        return response
        
# 로그아웃 부분
def logout(request):
    
    request.session.clear()
    context = {"state_code":"-1"}
    return render(request,'member/login.html',context)