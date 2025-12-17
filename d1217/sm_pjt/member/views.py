from django.shortcuts import render, redirect
from member.models import Member

# Create your views here.

def logout(request):
    request.session.clear()
    context = {'flag':'-1'}
    return render(request,'member/login.html', context)

def login(request):
    if request.method == "GET":
        return render(request,'member/login.html')
    elif request.method == "POST":
        
        # id = request.POST['id'] # 없을때 error
        # try: id = request.POST['id'] # 없을때 error
        # except: id = None
                
        id = request.POST.get('id') # 없을때 None
        pw = request.POST.get('pw') # 없을때 None
        
        qs = Member.objects.filter(id=id,pw=pw) # 없을때 []
        # try: qs = Member.objects.get(id=id,pw=pw) # 없을때 error
        # except: qs = None
        
        if qs:
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            context = {'flag':'1'}
        else:
            context = {'flag':'0','id':id,'pw':pw}
            
        return render(request,'member/login.html',context)
