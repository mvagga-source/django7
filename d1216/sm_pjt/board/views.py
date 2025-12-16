from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import F,Q
from board.models import Board
from member.models import Member


# Create your views here.

def reply(request, bno):
    
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



# 게시판 수정
def update(request,bno):
    
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}        
        return render(request,'board/update.html',context)
    elif request.method == 'POST':
        # id = request.session.get('session_id')
        # member = Member.objects.get(id=id)        
        
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile:
            qs.bfile = bfile
        qs.save()

        return redirect(f'/board/view/{bno}/')

# 게시판 삭제
def delete(request,bno):
    
    qs = Board.objects.get(bno=bno)
    qs.delete()
    return redirect('/board/list/')


# 게시판 상세보기
def view(request,bno):
    
    qs = Board.objects.filter(bno=bno)
    # 조회된 데이터(F('bhit'))의 값증가시 F함수 사용가능(update, delete), filter사용
    qs.update(bhit=F('bhit')+1)
    context = {'board':qs[0]}
    return render(request,'board/view.html',context)


# 게시판 리스트
def list(request):
    
    qs = Board.objects.all().order_by('-bgroup','bstep')
    #하단 넘버링
    paginator = Paginator(qs,10) # 페이지 갯수 자동계산
    
    #현재페이지 넘김
    page = int(request.GET.get('page',1))
    list_qs = paginator.get_page(page)
    
    context = {'list':list_qs,'page':page}
    return render(request,'board/list.html',context)

# 게시판 작성
def write(request):
    
    if request.method == 'GET':
        return render(request,'board/write.html')
    elif request.method == 'POST':
        
        id = request.session.get('session_id')
        member_qs = Member.objects.get(id=id)
        
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        
        qs = Board.objects.create(btitle=btitle,bcontent=bcontent,member=member_qs,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        
        context = {'flag':'1'}
        return render(request,'board/write.html',context)