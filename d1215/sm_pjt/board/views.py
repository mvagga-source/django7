from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from board.models import Board
from member.models import Member
from django.db.models import F,Q

# Create your views here.


# 답글
def reply(request,bno):
    
    if request.method == 'GET':
        
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/reply.html',context)
    elif request.method == 'POST':
        
        bgroup = request.POST.get('bgroup')
        bstep = int(request.POST.get('bstep'))
        bindent = int(request.POST.get('bindent'))
        
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        
        id = request.session['session_id']
        qs = Member.objects.get(id=id)
        
        # 1. bgroup에 부모보다 높은 bstep을 1증가를 시커주기
        bstepup_qs = Board.objects.filter(bgroup=bgroup,bstep__gt=bstep)
        # 2. 검색된 데이터에서 bstep을 뽑아서 1씩 증가
        bstepup_qs.update(bstep=F('bstep')+1)
        
        Board.objects.create(btitle=btitle,bcontent=bcontent,member=qs,\
            bgroup=bgroup,bstep=bstep+1,bindent=bindent+1)
        
        return redirect('/board/list?flag=2') # request->flag 파라미터 방식

# 게시글 수정
def update(request,bno):
    
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}        
        return render(request,'board/update.html',context)
    elif request.method == 'POST':
        
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        qs.save()

        return redirect(f'/board/view/{bno}/')

# 게시글 삭제
def delete(request,bno):
    
    qs = Board.objects.get(bno=bno)
    qs.delete()
    return redirect("/board/list/")

# 게시판 상세보기
def view(request,bno):
    
    qs = Board.objects.get(bno=bno)
    context = {"board":qs}
    return render(request,'board/view.html',context)

# 게시판 리스트
def list(request):
    
    qs = Board.objects.all().order_by('-bgroup','bstep')
    flag = request.GET.get("flag",'')
    context = {'list':qs,'flag':flag}
    
    return render(request,'board/list.html', context)

# 글쓰기 화면/저장
def write(request):
    
    if request.method == 'GET':
        
        return render(request,'board/write.html')
    elif request.method == 'POST':
        
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        
        id = request.session['session_id']
        qs = Member.objects.get(id=id)
        qs = Board.objects.create(btitle=btitle,bcontent=bcontent,member=qs)
        qs.bgroup = qs.bno
        qs.save()
        
        context = {'flag':'1'}
        return render(request,'board/write.html',context)
    
