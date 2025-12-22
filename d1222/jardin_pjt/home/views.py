from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.models import ChartData

# Create your views here.

def index(request):
    return render(request,'main.html')

def chart(request):
    return render(request,'chart1.html')

@csrf_exempt # csrf_token 예외처리
def chart_json(request):
    context = {'dd_data':[10, 5, 9, 8, 3, 6],'ll_data':['홍길동','유관순','이순신','강감찬','김구','김유신']}
    return JsonResponse(context)

def chart2(request):
    return render(request,'chart2.html')

def chart2_json(request):
    
    qs = ChartData.objects.all()
    qs_list = list(qs.values())
    context = {'list':qs_list}
    return JsonResponse(context)

