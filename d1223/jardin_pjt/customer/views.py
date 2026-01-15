from django.shortcuts import render, redirect
from customer.models import Board
from member.models import Member
from django.core.paginator import Paginator
from django.db.models import F,Q,Sum,Count
from comment.models import Comment
from django.http import JsonResponse

# get, post, put, delete 방식 지정
from rest_framework.decorators import api_view
# JsonResponse -> Response 사용
from rest_framework.response import Response
# status : 200 - 정상, 404 - 페이지 오류, 500 - 시스템 상태값 확인
from rest_framework import status

def clikes(request):
    
    
    if request.method == 'POST':
        bno = request.POST.get('bno')
        board = Board.objects.get(bno=bno)
        id = request.session['session_id']
        member = Member.objects.get(id=id)
        
        # board.likes.all() : 게시글에 좋아요를 클릭한 전체회원
        # member.likes_member.all() : 현재회원이 좋아요를 클릭한 게시글 전체목록

        # db에 좋아요 추가,삭제
        # Board 테이블에 likes컬럼에 데이터 추가, 삭제
        
        if board.likes.filter(pk=member.id).exists():
            board.likes.remove(member) # likes 안에 member를 제거
            likes_chk = 0
        else:
            board.likes.add(member) # likes 안에 member를 추가
            likes_chk = 1
        count = board.likes.count()
        
    print('좋아요 개수 확인 : ',board.likes.count())
    context = {'result':'성공','likes_chk':likes_chk,'count':count}
    return JsonResponse(context)


def cwrite(request):
    if request.method == 'GET':
        return render(request, 'customer/cwrite.html') # 관련 파일로 이동
    elif request.method == 'POST':
        id = request.session['session_id']
        
        member = Member.objects.get(id=id)
        
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        
        # db저장
        qs = Board.objects.create(member=member,btitle=btitle,bcontent=bcontent,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        
        return redirect('/customer/clist/') # 관련 함수로 이동

# board : 좋아요도 포함되어 전달됨
def cview(request, bno):
    
    # 1개 게시글
    qs = Board.objects.get(bno=bno)
    
    # 하단 댓글
    comment_qs = Comment.objects.all().order_by('-cno')
    
    # bgroup 역순정렬, bstep 순차정렬
    
    # 이전
    # Board.objects.filter(Q(bgroup__lt=qs[0].bgroup,bstep__lte=qs[0].bstep)|Q(bgroup=qs[0].bgroup,bstep__gt=qs[0].bstep)).order_by("-bgroup","bstep").first()
    pre_qs = Board.objects.filter(bgroup__lt=qs.bgroup).order_by('-bgroup','bstep').first()
    # pre_qs = Board.objects.filter(bgroup__lt=qs.bgroup).aggregate(min('bgroup'))
    print('이전글',pre_qs)
    
    # 다음
    # Board.objects.filter(Q(bgroup__gt=qs[0].bgroup,bstep__gte=qs[0].bstep)|Q(bgroup=qs[0].bgroup,bstep__lt=qs[0].bstep)).order_by("bgroup","-bstep").first()
    next_qs = Board.objects.filter(bgroup__gt=qs.bgroup).order_by('bgroup','-bstep').first()
    print('다음글',next_qs)
    
    context = {'c':qs,'pre_c':pre_qs,'next_c':next_qs,'comment_qs':comment_qs}
    
    return render(request, 'customer/cview.html',context)


def clist(request):
    
    # 검색기능
    
    search = request.GET.get('search','')
    category = request.GET.get('category','')
    
    print("검색 데이터 : ",category,search)
    
    if not search:
        qs = Board.objects.all().order_by('-bgroup','bstep')
    else:
        if category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search)
        elif category == 'bcontent':
            qs = Board.objects.filter(bcontent__contains=search)
        elif category == 'all':
            qs = Board.objects.filter(Q(btitle__contains=search)|Q(bcontent__contains=search))
            
    # Paginator 는 요청 페이지 번호가 있어야 함
    page = int(request.GET.get('page',1)) # page 번호 없으면 1 부여
    
    paginator = Paginator(qs,10)
    
    list_qs = paginator.get_page(page)
    
    context = {'list':list_qs,'page':page, 'category':category,'search':search}
    return render(request,'customer/clist.html', context)


# @api_view(['POST'])
@api_view(['GET'])
def clistJson(request):
    
    # axios Json 데이터로 전달
    
    # POST 방식    
    # page = request.data.get('page')
    # print('page : ',page)
    
    id = request.query_params.get('id')
    page = request.query_params.get('page')
    print('id : ',id,' page : ', page)
    
    qs = Board.objects.all().order_by('-bno')
    
    # Json
    l_qs = list(qs.values())
    context = {'list':l_qs}
    
    return Response(context, status=status.HTTP_200_OK)

@api_view(['POST'])
def cwriteJson(request):
    
    print('11')
    
    id = request.data.get('id','aaa')
    btitle = request.data.get('btitle','')
    bcontent = request.data.get('bcontent','')
    print('넘어온 데이터',id,btitle,bcontent)
    
    member = Member.objects.get(id=id)    
    
    qs = Board.objects.create(member=member,btitle=btitle,bcontent=bcontent)
    qs.bgroup = qs.bno
    qs.save()
    
    l_qs = list(Board.objects.filter(bno=qs.bno).values())
    
    context = {'result':'성공','board':l_qs}
    
    return Response(context, status=status.HTTP_200_OK)    
    
@api_view(['DELETE'])
def cdeleteJson(request, bno):
    
    name = request.data.get('name')
    print('넘어온 데이터 : ',bno,name)
    
    Board.objects.get(bno=bno).delete()
    
    context = {'result':'성공'}
    return Response(context, status=status.HTTP_200_OK)    
    
    