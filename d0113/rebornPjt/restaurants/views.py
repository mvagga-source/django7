from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from restaurants.models import *
from django.core.paginator import Paginator
from secret import api__func
from django.db.models import Avg, Count, Prefetch
from restaurants.models import Restaurant, RestaurantImage  # RestaurantImage 추가
from review.models import Review
from promo.models import Promo

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
    paginator=Paginator(qs,20)#20개씩 자르기
    list_qs=paginator.get_page(page)

    context={'list':list_qs,'page':page, 'promos':promos}
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