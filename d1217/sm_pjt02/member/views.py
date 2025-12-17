from django.shortcuts import render
from member.models import Member

# Create your views here.

def login(request):
    
    if request.method == 'GET':
        
        return render(request,'member/login.html')
    elif request.method == 'POST':
        
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        
        qs = Member.objects.get(id=id,pw=pw)
        
        if qs:
            context = {'flag':'1'}
            
            request.session['session_id'] = id
            
        else:
            context = {'flag':'0'}    
        
        return render(request,'member/login.html')
