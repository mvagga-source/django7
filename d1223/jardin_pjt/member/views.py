from django.shortcuts import render,redirect
from django.http import JsonResponse
from member.models import Member

def logout(request):
    # 섹션 모두 삭제
    request.session.clear()
    
    return redirect('/')

# 로그인 부분
def login(request):
    if request.method == 'GET':
        return render(request,'member/login.html')
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        print("넘어온 데이터 : ",id,pw)
        
        # id,pw체크
        qs = Member.objects.filter(id=id,pw=pw)
        if qs: 
            result = 1    
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
        else: result = 0
        context = {'result':result}
        
        return render(request,'member/login.html',context)
        

# 회원가입
def step03(request):
    return render(request,'member/step03.html')

# json 리턴 : id가 존재하는지 확인
def idCheck(request):
    # db확인
    id = request.GET.get('id','')
    qs = Member.objects.filter(id=id)
    if not qs: result = '사용가능'
    else: result = '사용불가'    
    #----------------
    context = {'result':result}
    return JsonResponse(context)
