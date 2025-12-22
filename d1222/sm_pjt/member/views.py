from django.shortcuts import render
from .models import Member

# 로그인
def login(request):
    if request.method == 'GET':
        return render(request,'member/login.html')
    elif request.method == 'POST':
        id = request.POST.get('id') # 없을때 None
        pw = request.POST.get('pw') # 없을때 None
        # try: id = request.POST['id'] # 없을때 에러
        # except: id = None
            
        qs = Member.objects.filter(id=id,pw=pw) #없을때 에러나지 않음 => []빈공백
        if qs:
            # 섹션추가
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            context = {'flag':'1'}
        else:
            context = {'flag':'0','id':id,'pw':pw}
        # try: qs = Member.objects.get(id=id,pw=pw)    #없을때 에러
        # except: qs = None
        
        return render(request,'member/login.html',context)

# 로그아웃
def logout(request):
    request.session.clear()
    context = {'flag':'-1'}
    return render(request,'member/login.html',context)