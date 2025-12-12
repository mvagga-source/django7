from django.shortcuts import render,redirect
from django.http import HttpResponse
from member.models import Member

# Create your views here.

def logout(request):
    
    request.session.clear()
    context = {"state_code":"-1"}
    return render(request,'member/login.html',context)

def login(request):
    
    if request.method == "GET":
        
        cook_id = request.COOKIES.get("cook_id","")
        context = {'cook_id':cook_id}
        
        return render(request,'member/login.html',context)
    
    elif request.method == "POST":
        
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        
        qs = Member.objects.filter(id=id,pw=pw)
        
        if qs:
            
            # 세션 저장
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            
            context = {"state_code":"1"}
            
            response = render(request,'member/login.html',context)
            
            login_keep = request.POST.get("login_keep")
            if login_keep:
                response.set_cookie("cook_id",id)
            else:
                response.delete_cookie("cook_id")
            
        else:
            print("id,pw 불일치")
            context = {"state_code":"0"}
            response = render(request,'member/login.html',context)
        
        return response
