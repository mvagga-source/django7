from django.shortcuts import render
from django.http import HttpResponse
from board.models import Board
from member.models import Member

# Create your views here.

# 게시판 리스트
def list(request):
    
    qs = Board.objects.all().order_by('-bno')
    print(qs)
    context = {'list':qs}
    
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
        
        Board.objects.create(btitle=btitle,bcontent=bcontent,member=qs)
        
        context = {'flag':'1'}
        return render(request,'board/write.html',context)
    
