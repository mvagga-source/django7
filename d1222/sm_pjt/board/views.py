from django.shortcuts import render,redirect
from board.models import Board
from member.models import Member
from django.db.models import F,Q
from django.core.paginator import Paginator
import requests
import json
from . import func_api

# 차트 그리기
def chart(request):
    return render(request,'board/chart.html')

# 공공데이터 api
def list2(request):
    public_key = func_api.public_api()
    context = {'result':'성공'}
    return render(request,'board/list2.html',context)


# 게시판 답글달기
def reply(request,bno):
    if request.method == 'GET':
        # 게시글 가져오기
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/reply.html',context)
    elif request.method == 'POST':
        # 답글저장
        bgroup = request.POST.get('bgroup')
        bstep = int(request.POST.get('bstep'))
        bindent = int(request.POST.get('bindent'))
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)
        bfile = request.FILES.get('bfile','')
        # 1. 답글달기 : 우선 같은 그룹에 있는 게시글의 bstep 1씩 먼저 증가
        board_qs = Board.objects.filter(bgroup=bgroup,bstep__gt = bstep)
        board_qs.update(bstep=F('bstep')+1) # F함수 : 검색된 그 컬럼에만 값을 적용
        
        # 2. 답글저장
        Board.objects.create(btitle=btitle,bcontent=bcontent,member=member,bgroup=bgroup,\
            bstep=bstep+1,bindent=bindent+1,bfile=bfile)
        
        
        context = {'flag':1}
        return render(request,'board/reply.html',context)


# 게시판 수정
def update(request,bno):
    if request.method == 'GET':
        # 게시글 가져오기
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/update.html',context)
    elif request.method == 'POST':
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        # 수정
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile: qs.bfile = bfile
        qs.save()    
        return redirect(f'/board/view/{bno}/')    
                
# 게시판 삭제
def delete(request,bno):
    # 게시글 가져오기
    qs = Board.objects.get(bno=bno)
    qs.delete()
    context = {'flag':2}
    return redirect("/board/list/")

# 게시판 상세보기 - 해당 하단댓글도 함께 가져올수 있음.
def view(request,bno):
    page = request.GET.get('page')
    search = request.GET.get('search')
    # 게시글 가져오기
    qs = Board.objects.filter(bno=bno)
    
    # 조회수 1증가
    # 조회를 한후 조회된 데이터들을 update,delete : F
    qs.update(bhit = F('bhit') + 1 )
    context = {'board':qs[0],'search':search,'page':page}
    return render(request,'board/view.html',context)

# 게시판 상세보기 - 해당 하단댓글도 함께 가져올수 있음.
def view2(request,bno):
    print("bno : ",bno)
    # 게시글 가져오기
    qs = Board.objects.filter(bno=bno)
    # 하단댓글
    c_qs = Comment.objects.filter(board=qs[0]).order_by('-cno')
    context = {'board':qs[0],'clist':c_qs}
    return render(request,'board/view2.html',context)


# 게시판 리스트
def list(request):
    search = request.GET.get('search','')
    page = int(request.GET.get('page',1))
    if search == '':
        # 게시글 모두 가져오기
        qs = Board.objects.all().order_by('-bgroup','bstep')
        # 하단 넘버링 (qs,10) -> 1페이지 10개씩
        paginator = Paginator(qs,10)  # 101 -> 11
        # 현재페이지 넘김.
        list_qs = paginator.get_page(page) # 1page -> 게시글 10개를 전달
    else:
        qs = Board.objects.filter(btitle__icontains = search)
        # and 조건
        # qs = Board.objects.filter(btitle__icontains = '답글',bcontent__icontains='답글')
        # or 조건
        # qs = Board.objects.filter(Q(btitle__icontains = '답글')|Q(bcontent__icontains = '답글'))
        # 하단 넘버링 (qs,10) -> 1페이지 10개씩
        paginator = Paginator(qs,10)  # 101 -> 11
        # 현재페이지 넘김.
        list_qs = paginator.get_page(page) # 1page -> 게시글 10개를 전달
    context = {'list':list_qs,'page':page,'search':search}
    return render(request,'board/list.html',context)

# 게시판 글쓰기
def write(request):
    if request.method == 'GET':
        return render(request,'board/write.html')
    elif request.method == 'POST':
        id = request.session.get('session_id')
        member_qs = Member.objects.get(id=id)
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        # bgroup 값을 입력
        qs = Board.objects.create(btitle=btitle,bcontent=bcontent,member=member_qs,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        context = {'flag':'1'}
        return render(request,'board/write.html',context)
        