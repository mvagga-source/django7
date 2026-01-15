from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from functools import wraps
from django.contrib import messages
from restaurants.models import Restaurant
from .models import Promo

# 로그인확인
def _is_logged_in(request) -> bool:
    # member/views.py에서 저장하는 세션 키 기준
    return bool(request.session.get("login_user") or request.session.get("user_id"))

def member_login_required(view_func):
    """페이지(HTML) 접근 보호: 로그인 안했으면 member:login으로 보내기"""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if _is_logged_in(request):
            return view_func(request, *args, **kwargs)
        messages.warning(request, "로그인 후 이용 가능합니다.")
        return redirect("member:login")
    return _wrapped

def member_login_required_api(view_func):
    """AJAX API 보호: 로그인 안했으면 401 JSON 반환"""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if _is_logged_in(request):
            return view_func(request, *args, **kwargs)
        return JsonResponse({"ok": False, "error": "LOGIN_REQUIRED"}, status=401)
    return _wrapped

# 식당 대표이미지 불러오기
def _main_img_url(restaurant: Restaurant) -> str:
    """
    RestaurantImage에서 is_main=True 대표이미지 1장을 사용.
    없으면 placeholder로 대체.
    """
    main = restaurant.images.filter(is_main=True).first()  # related_name="images"
    if main and getattr(main, "image", None):
        return main.image.url
    return f"https://picsum.photos/1200/420?{restaurant.resno}"

@member_login_required
def promo_admin(request):
    # 페이지 최초 렌더: select 옵션에 data-img로 대표이미지 넣기 위함
    restaurant_list = Restaurant.objects.all().order_by("res_name")
    for r in restaurant_list:
        r.main_img_url = _main_img_url(r)

    return render(request, "promo/promo_admin.html", {
        "restaurant_list": restaurant_list,
    })

@require_http_methods(["GET"])
@member_login_required_api
def promo_list_api(request):
    promos = Promo.objects.select_related("restaurant").all()
    out = []
    for p in promos:
        r = p.restaurant
        out.append({
            "promo_id": p.promo_id,
            "resno": r.resno,
            "res_name": r.res_name,
            "kicker": p.kicker,
            "title": p.title,
            "sub": p.sub,
            "cta_text": p.cta_text,
            "img": _main_img_url(r),
            "link": f"/restaurants/resview/{r.resno}/",
            "is_active": p.is_active,
            "sort_order": p.sort_order,
        })
    return JsonResponse({"ok": True, "promos": out})

@require_http_methods(["POST"])
@member_login_required_api
def promo_save_api(request):
    promo_id = request.POST.get("promo_id", "").strip()
    resno = request.POST.get("resno")
    restaurant = get_object_or_404(Restaurant, resno=resno)

    if promo_id:
        promo = get_object_or_404(Promo, promo_id=promo_id)
    else:
        promo = Promo()

    promo.restaurant = restaurant
    promo.kicker = request.POST.get("kicker", "")
    promo.title = request.POST.get("title", "")
    promo.sub = request.POST.get("sub", "")
    promo.cta_text = request.POST.get("cta_text", "자세히 보기")
    promo.save()

    return JsonResponse({"ok": True, "promo_id": promo.promo_id})

@require_http_methods(["POST"])
@member_login_required_api
def promo_delete_api(request, promo_id):
    promo = get_object_or_404(Promo, promo_id=promo_id)
    promo.delete()
    return JsonResponse({"ok": True})