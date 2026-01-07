from django.shortcuts import render
from django.http import HttpResponse
from restaurants.models import *
from django.core.paginator import Paginator
from secret import api__func

def reslist(request):
    search=request.GET.get('search','')
    if not search:
        qs = Restaurant.objects.all()
    else:
        qs = Restaurant.objects.filter(res_name__contains=search)

    page=int(request.GET.get('page',1))# 없으면 default=1
    paginator=Paginator(qs,20)#20개씩 자르기
    list_qs=paginator.get_page(page)

    context={'list':list_qs,'page':page}
    return render(request,'restaurants/reslist.html',context)

# def reslist(request):
#     return HttpResponse("reslist 페이지입니다.")

app_key= api__func.kakao__API()

def resview(request, resno):
    # 식당정보
    qs = Restaurant.objects.get(resno=resno)
    # 운영시간 정보 (해당 식당 것만)
    qs2 = RestaurantOperTime.objects.filter(resno=qs)
    # 메뉴 정보 (해당 식당 것만)
    qs3 = FoodMenu.objects.filter(resno=qs)

    context={'view':qs, 'oper_time':qs2, 'menu':qs3, 'app_key':app_key}
    return render(request,'restaurants/resview.html',context)