from django.shortcuts import render, redirect
from board.models import Board
import datetime

# Create your views here.

def write(request):
    if request.method == 'GET':
        return render(request,'board/write.html')
    elif request.method == 'POST':
        
        btitle = request.POST.get('btitle')
        bfile = request.FILES.get('bfile')
        # 같은 파일의 경우 다른 이름이름으로 저장 가능
        # bfile = f'{datetime.datetime.now().microsecond}_{bfile}'
        print('post btitle 정보 : ', btitle)
        print('post bfile 정보 : ', bfile)
        print('날짜 :',datetime.datetime.now())
        # print('날짜 :',datetime.datetime.now().microsecond)        
        
        # 파일저장
        qs = Board(btitle=btitle,bfile=bfile)
        qs.save()
        
        return render(request,'board/write.html')
