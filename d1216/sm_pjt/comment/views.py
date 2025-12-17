from django.shortcuts import render
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse,HttpResponse  # 전송 Json타입으로 변경해서 전송
from django.core import serializers   # Json타입으로 전달된 데이터를 파이썬데이터로 변경
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

# Create your views here.

def list(request):
    
    # datetime 타입, FileField 타입 -> json타입으로 변경이 안됨
    qs = Comment.objects.all()
    l_qs = serializers.serialize('json',qs) # json타입으로 변경
    # HttpResponse 자체를 리턴
    return HttpResponse(l_qs,content_type='application/json')
    
    # qs = list(Comment.objects.all().values())
    # for q in qs:
    #     q['cdate'] = q['cdate'].strftime('%Y-%m-%d')
    # JsonResponse(qs,safe=False,encoder=DjangoJSONEncoder)