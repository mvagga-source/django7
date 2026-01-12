from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from member.models import Member
import json

# Create your views here.

def step03(request):
    return render(request,'member/step03.html')

def idCheck(request):
    
    id = request.GET.get('id','')
    qs = Member.objects.filter(id=id)
    if not qs:
        result = '사용가능'
    else:
        result = '사용불가'

    context = {'result':result}
    return JsonResponse(context)

def userAll(request):
    
    print('id : ',request.GET.get('id',''))
    print('name : ',request.GET.get('name',''))
    # print('name : ',request.POST.get('name',''))
    
    qs = Member.objects.all()
    l_qs = list(qs.values())
    
    context = {'arr':l_qs}
    return JsonResponse(context)

# user 추가
def userInsert(request):
    
    body = json.loads(request.body)
    id = body.get('id')
    
    print('id : ',id)
    
    qs = Member.objects.all()
    l_qs = list(qs.values())
    
    context = {'arr':l_qs}
    return JsonResponse(context)

