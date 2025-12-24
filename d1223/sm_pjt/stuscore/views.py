from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse # 전송할때 Json타입으로 변경해서 전송
from django.core import serializers  # Json타입으로 전달된 데이터를 파이썬데이터(set)로 변경
from stuscore.models import Stuscore

def slist(request):
    if request.method == 'POST':
        no = int(request.POST.get('no'))
        qs = Stuscore.objects.all().order_by('sno')[no:(no+6)]
        list_qs = list(qs.values())  # QuerySet → 리스트
        context = {'result': 'success','list':list_qs}
        return JsonResponse(context)
