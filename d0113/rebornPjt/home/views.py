from django.shortcuts import render
from restaurants.models import *
from member.models import MyUser
from django.db.models import Q, Avg, Count

# Create your views here.
def index(request):
    # 1. Location 테이블 조회
    location_qs = Location.objects.all().order_by('sort')
    # 2. LocationDetail 테이블 조회
    locationDetail_qs = LocationDetail.objects.select_related('location').filter(is_main='y').order_by('sort')
    # 3. FoodType 테이블 조회
    foodType_qs = FoodType.objects.filter(is_main='y').order_by('sort')
    # 4. 음식선호도(로그인된 사람만)
    id = request.session.get('user_id')
    res_qs = []
    res_list = []
    if id:
        member_qs = MyUser.objects.filter(mem_id=id).first()
        if member_qs and member_qs.food_cat:
            food_cat_list = [cat.strip() for cat in member_qs.food_cat.split(',')]
            # 카테고리별 최소 1개씩
            used_res_ids = set()
            for food_cat in food_cat_list:
                res = (
                    Restaurant.objects
                    .filter(foodmenu__foodType__foodCategory__food_cat=food_cat)
                    .exclude(resno__in=used_res_ids)
                    # .order_by('?')    # 랜덤
                    .first()
                )

                if res:
                    res_list.append(res)
                    used_res_ids.add(res.resno)
            # 다섯개 미만이면 채워넣기
            if len(res_list) < 5:
                extra_qs = (
                    Restaurant.objects
                    .filter(
                        foodmenu__foodType__foodCategory__food_cat__in=food_cat_list,
                        img__isnull=False   # 이미지 있는 것만(임시)
                    )
                    # 별점
                    # .annotate(
                    #     avg_rating=Avg('comment__rating'),
                    #     review_count=Count('comment')
                    # )
                    .exclude(resno__in=used_res_ids)
                    .distinct()
                    # .order_by('-avg_rating')  # 평균별점 높은 순
                    # .order_by('?')    # 랜덤
                )

                for res in extra_qs:
                    res_list.append(res)
                    if len(res_list) >= 5:
                        break
            res_qs = res_list
            for res in res_qs:
                food_cat = (
                    FoodCategory.objects
                    .filter(foodtype__foodmenu__resno=res)
                    .values_list('food_cat', flat=True)
                    .distinct()
                    .first()
                )
                res.main_food_cat = food_cat
            # food_category_qs = FoodCategory.objects.filter(food_cat__in=food_cat_list)
            # food_type_qs = FoodType.objects.filter(foodCategory__in=food_category_qs)
            # res_qs = Restaurant.objects.filter(foodmenu__foodType__in=food_type_qs).distinct()[:5]
            # print(member_qs.food_cat)
    
    context = {
        "location": location_qs,
        "locationDetail": locationDetail_qs,
        "foodType": foodType_qs,
        "res_list":res_qs,
    }
    return render(request, 'index.html', context)

def filPop(request):
    # 필터에 저장된 값들(블루리본에도 안 되어 있는걸로 보여서 X)
    context = {
        "req": request,
        "res_name": request.GET.get("res_name"),
        "checked_locno": request.GET.getlist("locno"),
        "checked_locdno": request.GET.getlist("locdno"),
        "checked_ftypeno": request.GET.getlist("ftypeno"),
        "checked_weeks": request.GET.getlist("weeks"),
        "price_min": request.GET.get("price_min"),
        "price_max": request.GET.get("price_max"),
        "open_time": request.GET.get("open_time"),
        "close_time": request.GET.get("close_time"),
    }
    
    # 지역, 음식타입 테이블에 있는걸로 가져와서 팝업에 체크박스 생성
    # # 1. Location 테이블 조회
    location_qs = Location.objects.all().order_by('sort')
    # # 2. LocationDetail 테이블 조회
    locationDetail_qs = LocationDetail.objects.select_related('location').all().order_by('sort')
    # # 3. FoodType 테이블 조회
    foodType_qs = FoodType.objects.all().order_by('sort')

    context["weekdays"] = ["월", "화", "수", "목", "금", "토", "일"]
    context["location"] = location_qs
    context["locationDetail"] = locationDetail_qs
    context["foodType"] = foodType_qs
    
    return render(request, 'filPop.html', context)