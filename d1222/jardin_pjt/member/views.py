from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from member.models import Member

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
