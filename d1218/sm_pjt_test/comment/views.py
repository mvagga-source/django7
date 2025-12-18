from django.shortcuts import render
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse # 전송할때 Json타입으로 변경해서 전송
from django.core import serializers  # Json타입으로 전달된 데이터를 파이썬데이터(set)로 변경

# 하단댓글 수정
def cupdate(request):
    if request.method == 'POST':
        cno = request.POST.get('cno')
        ccontent = request.POST.get('ccontent')
        # qs = Comment.objects.get(cno=cno)
        # qs.ccontent = ccontent
        # qs.save()
        
        # json데이터 변환하기 위한 list타입 변경
        Comment.objects.filter(cno=cno).update(ccontent=ccontent)
        c_qs = list(Comment.objects.filter(cno=cno).values())
        context = {'comment':c_qs[0],'result':'성공'}
        return JsonResponse(context)
    
# 하단댓글 삭제
def cdelete(request):
    if request.method == 'POST':
        cno = request.POST.get('cno')
        Comment.objects.get(cno=cno).delete()
        context = {'result':'성공'}
        return JsonResponse(context)


# 하단댓글 추가 
def cwrite(request):
    if request.method == 'POST':
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)
        bno = request.POST.get('bno')
        board = Board.objects.get(bno=bno)
        cpw = request.POST.get('cpw') 
        ccontent = request.POST.get('ccontent') 
        print(f"bno : {bno}, cpw : {cpw}, ccontent : {ccontent}")
        
        qs = Comment.objects.create(board=board,cpw=cpw,ccontent=ccontent,member=member)
        # print("qs.cno : ",qs)
        # dict_qs = model_to_dict(qs)
        # context = {'comment':dict_qs,'result':'성공'}
        
        # values()를 해야 list타입으로 변경됨.
        c_qs = list(Comment.objects.filter(cno=qs.cno).values())
        context = {'comment':c_qs[0],'result':'성공'}
        return JsonResponse(context)

# 하단댓글 리스트 
def clist(request):
    bno = request.GET.get('bno') 
    print("bno : ",bno)
    board = Board.objects.get(bno=bno)
    qs = Comment.objects.filter(board=board).order_by('-cno')
    list_qs = list(qs.values())  # QuerySet → 리스트
    context = {'result': 'success','list':list_qs}
    return JsonResponse(context)

   