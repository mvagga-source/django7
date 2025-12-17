from django.shortcuts import render
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse,HttpResponse  # 전송 Json타입으로 변경해서 전송
from django.core import serializers   # Json타입으로 전달된 데이터를 파이썬데이터로 변경

# Create your views here.

def cwrite(request):
    
    if request.method == 'POST':
        
        bno = request.POST.get('bno')
        board = Board.objects.get(bno=bno)
        cpw = request.POST.get('cpw')
        ccontent = request.POST.get('ccontent')
        
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)
        
        print(f"bno : {bno}")
        
        qs = Comment.objects.create(board=board,cpw=cpw,ccontent=ccontent,member=member)
        c_qs = list(Comment.objects.filter(cno=qs.cno).values())
        context = {'c_comment':c_qs[0]}
        return JsonResponse(context)
    
    
    # datetime 타입, FileField 타입 -> json타입으로 변경이 안됨
    # qs = Comment.objects.all()
    # l_qs = serializers.serialize('json',qs) # json타입으로 변경
    # # HttpResponse 자체를 리턴
    # return HttpResponse(l_qs,content_type='application/json')
    
def clist(request):
    
    bno = request.GET.get('bno')
    
    print('bno :',bno)
    board = Board.objects.get(bno=bno)
    
    qs = Comment.objects.filter(board=board)
    list_qs = list(qs.values())
    context = {'result':'success','list':list_qs}
    return JsonResponse(context)
    
    
    # datetime 타입, FileField 타입 -> json타입으로 변경이 안됨
    # qs = Comment.objects.all()
    # l_qs = serializers.serialize('json',qs) # json타입으로 변경
    # # HttpResponse 자체를 리턴
    # return HttpResponse(l_qs,content_type='application/json')
