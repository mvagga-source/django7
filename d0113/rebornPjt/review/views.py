from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Review, ReviewImage
from restaurants.models import Restaurant
from member.models import MyUser
from django.db.models import Avg, Count
from django.template.loader import render_to_string

# ----------------------------
# ajax 후기작성(세션 로그인 기준)
# ----------------------------
@require_POST
def write_review(request):
    
    # 로그인 채크(session)
    user_id=request.session.get('user_id')
    if not user_id:
        return JsonResponse({'result':'login_required'},status=401)
    try:
        restaurant_id=request.POST.get('restaurant_id')
        content=request.POST.get('content')
        rating=int(request.POST.get('rating'))
        
        if not content or not rating:
            return JsonResponse({'result':'fail','msg':'값 누락'},status=400)
        
        restaurant=Restaurant.objects.get(resno=restaurant_id)
        member=MyUser.objects.get(mem_id=user_id)
        
        # 1.리뷰 생성
        review=Review.objects.create(
            restaurant=restaurant,
            member=member,
            rcontent=content,
            rating=rating
        )
        
        # 2. 이미지 처리(여러장)
        images=request.FILES.getlist('images')
        for img in images:
            ReviewImage.objects.create(
                review=review,
                image=img
            )
        
        # 3.리뷰 개수/평점
        stats = Review.objects.filter(
            restaurant=restaurant
        ).aggregate(#DB에서 바로 계산
            avg_rating=Avg("rating"),
            review_count=Count("rno")
        )
        
        return JsonResponse({
            "result": "success",
            "review": {
                "id": review.rno,
                "user": member.nick_nm,
                "rating": review.rating,
                "content": review.rcontent,
                "date": review.rdate.strftime("%Y-%m-%d"),
                "images": [img.image.url for img in review.images.all()]
            },
            "stats": {
                "avg_rating": round(stats["avg_rating"], 1) if stats["avg_rating"] else 0,
                "review_count": stats["review_count"]
            }
        })
    
    except Exception as e:
        return JsonResponse({'result':'error','message':str(e)},status=500)

# ----------------------------
# 후기삭제(세션 로그인 기준)
# ----------------------------    
@require_POST
def delete_review(request):

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"result": "login_required"}, status=401)

    review_id = request.POST.get("review_id")

    try:
        review = Review.objects.get(rno=review_id)

        # 본인 확인 후 삭제
        if not review.member or review.member.mem_id != user_id:
            return JsonResponse({"result": "forbidden"}, status=403)

        restaurant = review.restaurant
        review.delete()

        # 리뷰 개수/평균 재계산
        stats = Review.objects.filter(
            restaurant=restaurant
        ).aggregate(
            avg_rating=Avg("rating"),
            review_count=Count("rno")
        )

        return JsonResponse({
            "result": "success",
            "stats": {
                "avg_rating": round(stats["avg_rating"], 1) if stats["avg_rating"] else 0,
                "review_count": stats["review_count"]
            }
        })

    except Review.DoesNotExist:
        return JsonResponse({"result": "not_found"}, status=404)
    
    except Exception as e:
        # 🔥 이 로그 꼭 남겨라 (개발 중)
        print("DELETE ERROR:", e)
        return JsonResponse({"result": "error"}, status=500)

# ----------------------------
# 후기수정(세션 로그인 기준)
# ----------------------------    
@require_POST
def update_review(request):

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"result": "login_required"}, status=401)

    try:
        review_id = request.POST.get("review_id")
        content = request.POST.get("content")
        rating = int(request.POST.get("rating"))

        review = Review.objects.get(rno=review_id)

        # 본인 확인
        if not review.member or review.member.mem_id != user_id:
            return JsonResponse({"result": "forbidden"}, status=403)

        # 1.리뷰 수정
        review.rcontent = content
        review.rating = rating
        review.save()

        # 2.기존 이미지 삭제
        deleted_ids = request.POST.getlist("deleted_images")
        ReviewImage.objects.filter(
            ino__in=deleted_ids,
            review=review
        ).delete()

        # 3.새 이미지 추가
        images = request.FILES.getlist("images")
        for img in images:
            ReviewImage.objects.create(
                review=review,
                image=img
            )

        return JsonResponse({"result": "success"})

    except Exception as e:
        print("UPDATE ERROR:", e)
        return JsonResponse({"result": "error"}, status=500)

# ----------------------------
# 후기정렬(부분 렌더링)
# ----------------------------   
def list_review(request):
    resno = request.GET.get("resno")
    sort = request.GET.get("sort", "latest")

    restaurant = Restaurant.objects.get(resno=resno)

    qs = Review.objects.filter(
        restaurant=restaurant
    ).select_related("member").prefetch_related("images")

    # 정렬 분기
    if sort == "rating":
        qs = qs.order_by("-rating", "-rdate")
    else:  # latest
        qs = qs.order_by("-rdate")

    html = render_to_string(
        "restaurants/review_list_partial.html",
        {"reviews": qs, "login_user_id": request.session.get("user_id")}
    )

    return JsonResponse({"html": html})