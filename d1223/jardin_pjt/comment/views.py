from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from comment.models import Comment
from member.models import Member
from customer.models import Board

# Create your views here.

def colist(request):
    # list 타입으로 변경을 해서 Json타입으로 변경을 해야 함
    # object.filter(), objects.all() -> list 타입

    return JsonResponse()

def codelete(request):
    # list 타입으로 변경을 해서 Json타입으로 변경을 해야 함
    # object.filter(), objects.all() -> list 타입
    
    cno = request.POST.get('cno')
    Comment.objects.get(cno=cno).delete()
    context = {'result':'성공'}
    
    return JsonResponse(context)

def cowrite(request):
    # list 타입으로 변경을 해서 Json타입으로 변경을 해야 함
    # object.filter(), objects.all() -> list 타입
    
    id = request.session['session_id']
    member = Member.objects.get(id=id)
    
    bno = request.POST.get('bno')
    board = Board.objects.get(bno=bno)
    
    cpw = request.POST.get('cpw','')
    ccontent = request.POST.get('ccontent','')
    print('넘어온 데이터 : ',cpw,ccontent)

    # DB저장
    qs = Comment.objects.create(cpw=cpw,ccontent=ccontent,member=member,board=board)
    l_qs = list(Comment.objects.filter(cno=qs.cno).values()) # json 데이터 형태로 변경
    
    print('l_qs data type : ',l_qs)
    
    context = {'result':'성공','co':l_qs}
    return JsonResponse(context)
