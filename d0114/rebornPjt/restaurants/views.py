from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from restaurants.models import *
from django.core.paginator import Paginator
from secret import api__func
from django.db.models import Avg, Count, Prefetch
from restaurants.models import Restaurant, RestaurantImage  # RestaurantImage 추가
from review.models import Review
from promo.models import Promo
from django.db.models import Q, Min, Max

def _main_img_url(restaurant):
    main = restaurant.images.filter(is_main=True).first()  # related_name="images"
    if main and getattr(main, "image", None):
        return main.image.url
    return f"https://picsum.photos/1200/420?{restaurant.resno}"

def reslist(request):
    search=request.GET.get('search','')
    if not search:
        qs = Restaurant.objects.all()
    else:
        qs = Restaurant.objects.filter(res_name__contains=search)
    
    q = Q()
    # 지역
    locno = request.GET.getlist('locno')
    if locno and locno != ['']:
        q &= Q(location__locno__in=locno)
    # 지역상세
    locdno = request.GET.getlist('locdno')
    if any(locdno):
        q &= Q(locationDetail__locdno__in=locdno)
    # 음식타입
    ftypeno = request.GET.getlist('ftypeno')
    if ftypeno:
        q &= Q(foodmenu__foodType__ftypeno__in=ftypeno)
    # 요일
    weeks = request.GET.getlist('weeks')
    if weeks:
        q &= Q(restaurantopertime__week__in=weeks)
    # 운영시간
    open_time = request.GET.get('open_time')
    close_time = request.GET.get('close_time')
    if open_time and close_time:
        is_overnight = open_time > close_time
        if not is_overnight:
            q &= Q(
                restaurantopertime__open_time__gte=open_time,
                restaurantopertime__close_time__lte=close_time,
            )
        else:
            q &= (
                # 당일 저녁 (06:00 ~ 23:59)
                Q(
                    restaurantopertime__open_time__gte=open_time,
                )
                |
                # 익일 새벽 (00:00 ~ 05:59)
                Q(
                    restaurantopertime__close_time__lte=close_time,
                )
            )
    qs = qs.filter(q)   # 필터
    # 가격(식당 메뉴 전체 가격 범위가 지정한 최소 최대 범위안에 모두 포함되어야 조회)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min and price_max:
        qs = qs.annotate(
            min_price=Min('foodmenu__price'),
            max_price=Max('foodmenu__price'),
        ).filter(
            min_price__gte=price_min,
            max_price__lte=price_max,
        )
    # 메뉴의 최소금액부터 최대금액까지 음식이 1개라도 포함만 되면 가져오기
    # if price_min:
    #     q &= Q(foodmenu__price__gte=price_min)
    # if price_max:
    #     q &= Q(foodmenu__price__lte=price_max)
    
    qs = qs.distinct()
    # qs = qs.filter(q).distinct()
    params = []     # 맵으로 반복 빼려면 홈쪽에서 팝업 전달 수정 필요
    for key in request.GET:
        if key not in ['page', 'search']:   # 페이지, 검색만 제외하고 hidden으로 넘겨줌
            for value in request.GET.getlist(key):
                params.append({'key': key, 'value': value})
    
    # 대표이미지
    promos = (Promo.objects
          .filter(is_active=True)
          .select_related("restaurant")
          .order_by("sort_order")[:4])

    for p in promos:
        p.img_url = _main_img_url(p.restaurant)

    # ✅ 평균별점 + 리뷰수 추가
    qs = qs.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews__rno')
    )
    
    # ✅ 대표이미지만 미리 가져오기
    qs = qs.prefetch_related(
        Prefetch("images", queryset=RestaurantImage.objects.filter(is_main=True))
    )
    
    page=int(request.GET.get('page',1))# 없으면 default=1
    paginator=Paginator(qs,12)#20개씩 자르기
    list_qs=paginator.get_page(page)

    context={'list':list_qs,'page':page, 'promos':promos, 'search':search}
    context['params']=params
    return render(request,'restaurants/reslist.html',context)

# def reslist(request):
#     return HttpResponse("reslist 페이지입니다.")

app_key= api__func.kakao__API()

def resview(request, resno):
    # 식당정보 + 이미지
    qs = get_object_or_404(Restaurant.objects.prefetch_related("images"), resno=resno)
    # ✅ 대표 / 서브 분리
    main_image = qs.images.filter(is_main=True).first()
    sub_images = qs.images.filter(is_main=False)
    # 운영시간 정보 (해당 식당 것만)
    qs2 = RestaurantOperTime.objects.filter(resno=qs)
    # 메뉴 정보 (해당 식당 것만)
    qs3 = FoodMenu.objects.filter(resno=qs)
    # 리뷰 조회
    qs4 = Review.objects.filter(restaurant=qs).select_related('member').prefetch_related('images').order_by('-rdate')
    # 리뷰 개수/평점
    qs5 = qs4.aggregate(avg_rating=Avg('rating'),review_count=Count('rno'))
    # 로그인 된 user_id
    qs6 = request.session.get('user_id')

    context={'view':qs, 'oper_time':qs2, 'menu':qs3, 'reviews':qs4, 'app_key':app_key,
            "avg_rating": round(qs5["avg_rating"], 1) if qs5["avg_rating"] else 0,
            "review_count": qs5["review_count"],
            "login_user_id": qs6,
            "main_image": main_image,
            "sub_images": sub_images,
    }
    return render(request,'restaurants/resview.html',context)

def respromo(request):
    return render(request,'restaurants/respromo.html')