from django.shortcuts import render
from restaurants.models import *

# Create your views here.
def index(request):
    # location_qs = [
    #     {"locno": 1, "loc": "서울 강남", "is_main": "n", "sort": 1},
    #     {"locno": 2, "loc": "서울 강북", "is_main": "n", "sort": 2},
    # ]
    # locationDetail_qs = [
    #     {"locdno": 1, "location": location_qs[0], "locd_nm": "가로수길/신사역", "is_main": "y", "sort": 1},
    #     {"locdno": 2, "location": location_qs[0], "locd_nm": "압구정동/도산공원", "is_main": "y", "sort": 2},
    #     {"locdno": 3, "location": location_qs[0], "locd_nm": "청담동/강남구청역", "is_main": "y", "sort": 3},
    #     {"locdno": 4, "location": location_qs[0], "locd_nm": "논현동/영동시장", "is_main": "y", "sort": 4},
    #     {"locdno": 5, "location": location_qs[0], "locd_nm": "삼성동/대치동", "is_main": "y", "sort": 5},
    #     {"locdno": 6, "location": location_qs[0], "locd_nm": "선릉역/선정릉역", "is_main": "y", "sort": 6},
    #     {"locdno": 7, "location": location_qs[0], "locd_nm": "역삼동", "is_main": "y", "sort": 7},
    #     {"locdno": 8, "location": location_qs[0], "locd_nm": "도곡/양재/매봉", "is_main": "y", "sort": 8},
    #     {"locdno": 9, "location": location_qs[0], "locd_nm": "강남역", "is_main": "y", "sort": 9},
    #     {"locdno": 10, "location": location_qs[0], "locd_nm": "고속터미널/반포", "is_main": "y", "sort": 10},
    #     {"locdno": 11, "location": location_qs[0], "locd_nm": "교대/남부터미널/서초", "is_main": "y", "sort": 11},
    #     {"locdno": 12, "location": location_qs[0], "locd_nm": "방배/사당/이수", "is_main": "y", "sort": 12},
    #     {"locdno": 13, "location": location_qs[0], "locd_nm": "서래마을", "is_main": "y", "sort": 13},
    #     {"locdno": 14, "location": location_qs[0], "locd_nm": "서울대/관악구", "is_main": "y", "sort": 14},
    #     {"locdno": 15, "location": location_qs[0], "locd_nm": "가산디지털단지/구로", "is_main": "y", "sort": 15},
    #     {"locdno": 16, "location": location_qs[0], "locd_nm": "영등포", "is_main": "y", "sort": 16},
    #     {"locdno": 17, "location": location_qs[0], "locd_nm": "여의도", "is_main": "y", "sort": 17},
    #     {"locdno": 18, "location": location_qs[0], "locd_nm": "김포/마곡", "is_main": "y", "sort": 18},
    #     {"locdno": 19, "location": location_qs[0], "locd_nm": "목동/화곡", "is_main": "y", "sort": 19},
    #     {"locdno": 20, "location": location_qs[0], "locd_nm": "개포/일원/수서", "is_main": "y", "sort": 20},
    #     {"locdno": 21, "location": location_qs[0], "locd_nm": "가락/문정/오금/위례", "is_main": "y", "sort": 21},
    #     {"locdno": 22, "location": location_qs[0], "locd_nm": "잠실/방이/올림픽공원", "is_main": "y", "sort": 22},
    #     {"locdno": 23, "location": location_qs[0], "locd_nm": "석촌호수", "is_main": "y", "sort": 23},
    #     {"locdno": 24, "location": location_qs[0], "locd_nm": "강동구", "is_main": "y", "sort": 24},
    #     {"locdno": 25, "location": location_qs[1], "locd_nm": "노원/강북", "is_main": "y", "sort": 25},
    #     {"locdno": 26, "location": location_qs[1], "locd_nm": "동대문/성동", "is_main": "y", "sort": 26},
    #     {"locdno": 27, "location": location_qs[1], "locd_nm": "종로/중구", "is_main": "y", "sort": 27},
    # ]
    # foodType_qs = [
    #     {"ftypeno": 1, "ftype": "파스타", "img_url_main": "/static/images/home/food/pasta.jpg", "is_main": "y", "sort": 1},
    #     {"ftypeno": 2, "ftype": "피자", "img_url_main": "/static/images/home/food/pizza.jpg", "is_main": "y", "sort": 2},
    #     {"ftypeno": 3, "ftype": "라멘", "img_url_main": "/static/images/home/food/ramen.jpg", "is_main": "y", "sort": 3},
    #     {"ftypeno": 4, "ftype": "장어", "img_url_main": "/static/images/home/food/grilledEel.jpg", "is_main": "y", "sort": 4},
    #     {"ftypeno": 5, "ftype": "한정식", "img_url_main": "/static/images/home/food/koreanFixedMenu.jpg", "is_main": "y", "sort": 5},
    #     {"ftypeno": 6, "ftype": "한우오마카세", "img_url_main": "/static/images/home/food/hanwooOmakese.jpg", "is_main": "y", "sort": 6},
    #     {"ftypeno": 7, "ftype": "방어", "img_url_main": "/static/images/home/food/yellowtail.jpg", "is_main": "y", "sort": 7},
    #     {"ftypeno": 8, "ftype": "베트남식", "img_url_main": "/static/images/home/food/vietnameseFood.jpg", "is_main": "y", "sort": 8},
    #     {"ftypeno": 9, "ftype": "케이크", "img_url_main": "/static/images/home/food/cake.jpg", "is_main": "y", "sort": 9},
    #     {"ftypeno": 10, "ftype": "스시", "img_url_main": "/static/images/home/food/sushi.jpg", "is_main": "y", "sort": 10},
    #     {"ftypeno": 11, "ftype": "커피전문점", "img_url_main": "/static/images/home/food/coffee.jpg", "is_main": "y", "sort": 11},
    #     {"ftypeno": 12, "ftype": "스테이크", "img_url_main": "/static/images/home/food/steak.jpg", "is_main": "y", "sort": 12},
    #     {"ftypeno": 13, "ftype": "돼지갈비", "img_url_main": "/static/images/home/food/porkRibs.jpg", "is_main": "y", "sort": 13},
    #     {"ftypeno": 14, "ftype": "칼국수", "img_url_main": "/static/images/home/food/kalguksu.jpg", "is_main": "y", "sort": 14},
    # ]
    # 1. Location 테이블 조회
    location_qs = Location.objects.all().order_by('sort')
    # 2. LocationDetail 테이블 조회
    locationDetail_qs = LocationDetail.objects.select_related('location').filter(is_main='y').order_by('sort')
    # 3. FoodType 테이블 조회
    foodType_qs = FoodType.objects.filter(is_main='y').order_by('sort')
    context = {
        "location": location_qs,
        "locationDetail": locationDetail_qs,
        "foodType": foodType_qs,
    }
    return render(request, 'index.html', context)

def filPop(request):
    # 필터에 저장된 값들(블루리본에도 안 되어 있는걸로 보여서 X)
    context = {
        "req": request,
        "res_nm": request.GET.get("res_nm"),
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
    
    # 테스트용 가짜 데이터(충돌날 수 있어서 DB대신 임시로 테스트 사용중)
    # location_qs = [
    #     {"locno": 1, "loc": "서울 강남", "is_main": "n", "sort": 1},
    #     {"locno": 2, "loc": "서울 강북", "is_main": "n", "sort": 2},
    # ]
    # locationDetail_qs = [
    #     {"locdno": 1, "location": location_qs[0], "locd_nm": "가로수길/신사역", "is_main": "y", "sort": 1},
    #     {"locdno": 2, "location": location_qs[0], "locd_nm": "압구정동/도산공원", "is_main": "y", "sort": 2},
    #     {"locdno": 3, "location": location_qs[0], "locd_nm": "청담동/강남구청역", "is_main": "y", "sort": 3},
    #     {"locdno": 4, "location": location_qs[0], "locd_nm": "논현동/영동시장", "is_main": "y", "sort": 4},
    #     {"locdno": 5, "location": location_qs[0], "locd_nm": "삼성동/대치동", "is_main": "y", "sort": 5},
    #     {"locdno": 6, "location": location_qs[0], "locd_nm": "선릉역/선정릉역", "is_main": "y", "sort": 6},
    #     {"locdno": 7, "location": location_qs[0], "locd_nm": "역삼동", "is_main": "y", "sort": 7},
    #     {"locdno": 8, "location": location_qs[0], "locd_nm": "도곡/양재/매봉", "is_main": "y", "sort": 8},
    #     {"locdno": 9, "location": location_qs[0], "locd_nm": "강남역", "is_main": "y", "sort": 9},
    #     {"locdno": 10, "location": location_qs[0], "locd_nm": "고속터미널/반포", "is_main": "y", "sort": 10},
    #     {"locdno": 11, "location": location_qs[0], "locd_nm": "교대/남부터미널/서초", "is_main": "y", "sort": 11},
    #     {"locdno": 12, "location": location_qs[0], "locd_nm": "방배/사당/이수", "is_main": "y", "sort": 12},
    #     {"locdno": 13, "location": location_qs[0], "locd_nm": "서래마을", "is_main": "y", "sort": 13},
    #     {"locdno": 14, "location": location_qs[0], "locd_nm": "서울대/관악구", "is_main": "y", "sort": 14},
    #     {"locdno": 15, "location": location_qs[0], "locd_nm": "가산디지털단지/구로", "is_main": "y", "sort": 15},
    #     {"locdno": 16, "location": location_qs[0], "locd_nm": "영등포", "is_main": "y", "sort": 16},
    #     {"locdno": 17, "location": location_qs[0], "locd_nm": "여의도", "is_main": "y", "sort": 17},
    #     {"locdno": 18, "location": location_qs[0], "locd_nm": "김포/마곡", "is_main": "y", "sort": 18},
    #     {"locdno": 19, "location": location_qs[0], "locd_nm": "목동/화곡", "is_main": "y", "sort": 19},
    #     {"locdno": 20, "location": location_qs[0], "locd_nm": "개포/일원/수서", "is_main": "y", "sort": 20},
    #     {"locdno": 21, "location": location_qs[0], "locd_nm": "가락/문정/오금/위례", "is_main": "y", "sort": 21},
    #     {"locdno": 22, "location": location_qs[0], "locd_nm": "잠실/방이/올림픽공원", "is_main": "y", "sort": 22},
    #     {"locdno": 23, "location": location_qs[0], "locd_nm": "석촌호수", "is_main": "y", "sort": 23},
    #     {"locdno": 24, "location": location_qs[0], "locd_nm": "강동구", "is_main": "y", "sort": 24},
    #     {"locdno": 25, "location": location_qs[1], "locd_nm": "노원/강북", "is_main": "y", "sort": 25},
    #     {"locdno": 26, "location": location_qs[1], "locd_nm": "동대문/성동", "is_main": "y", "sort": 26},
    #     {"locdno": 27, "location": location_qs[1], "locd_nm": "종로/중구", "is_main": "y", "sort": 27},
    # ]
    # foodType_qs = [
    #     {"ftypeno": 1, "ftype": "파스타", "img_url_main": "/static/images/home/food/pasta.jpg", "is_main": "y", "sort": 1},
    #     {"ftypeno": 2, "ftype": "피자", "img_url_main": "/static/images/home/food/pizza.jpg", "is_main": "y", "sort": 2},
    #     {"ftypeno": 3, "ftype": "라멘", "img_url_main": "/static/images/home/food/ramen.jpg", "is_main": "y", "sort": 3},
    #     {"ftypeno": 4, "ftype": "장어", "img_url_main": "/static/images/home/food/grilledEel.jpg", "is_main": "y", "sort": 4},
    #     {"ftypeno": 5, "ftype": "한정식", "img_url_main": "/static/images/home/food/koreanFixedMenu.jpg", "is_main": "y", "sort": 5},
    #     {"ftypeno": 6, "ftype": "한우오마카세", "img_url_main": "/static/images/home/food/hanwooOmakese.jpg", "is_main": "y", "sort": 6},
    #     {"ftypeno": 7, "ftype": "방어", "img_url_main": "/static/images/home/food/yellowtail.jpg", "is_main": "y", "sort": 7},
    #     {"ftypeno": 8, "ftype": "베트남식", "img_url_main": "/static/images/home/food/vietnameseFood.jpg", "is_main": "y", "sort": 8},
    #     {"ftypeno": 9, "ftype": "케이크", "img_url_main": "/static/images/home/food/cake.jpg", "is_main": "y", "sort": 9},
    #     {"ftypeno": 10, "ftype": "스시", "img_url_main": "/static/images/home/food/sushi.jpg", "is_main": "y", "sort": 10},
    #     {"ftypeno": 11, "ftype": "커피전문점", "img_url_main": "/static/images/home/food/coffee.jpg", "is_main": "y", "sort": 11},
    #     {"ftypeno": 12, "ftype": "스테이크", "img_url_main": "/static/images/home/food/steak.jpg", "is_main": "y", "sort": 12},
    #     {"ftypeno": 13, "ftype": "돼지갈비", "img_url_main": "/static/images/home/food/porkRibs.jpg", "is_main": "y", "sort": 13},
    #     {"ftypeno": 14, "ftype": "칼국수", "img_url_main": "/static/images/home/food/kalguksu.jpg", "is_main": "y", "sort": 14},
    # ]

    context["weekdays"] = ["월", "화", "수", "목", "금", "토", "일"]
    context["location"] = location_qs
    context["locationDetail"] = locationDetail_qs
    context["foodType"] = foodType_qs
    
    return render(request, 'filPop.html', context)