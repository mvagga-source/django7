from django.shortcuts import render, redirect
from django.core.paginator import Paginator # 동료가 추천한 그 도구!
from django.http import HttpResponse
import requests
from .models import Book
from secret import api__func

# ------------------------------------------------------------------
# [관리자용] 1. 네이버에서 요리책 데이터를 몽땅 가져와서 내 DB에 저장하는 함수
# 주소창에 /init_db 라고 치면 실행되게 연결하면 됩니다.
# ------------------------------------------------------------------
def init_db(request):
    # 1. API 키 설정
    secret__list = api__func.naver__API()
    headers = {
        "X-Naver-Client-Id": secret__list[0],
        "X-Naver-Client-Secret": secret__list[1]
    }
    
    # 2. 요리책 100권 가져오기 (네이버는 한 번에 최대 100개까지 줌)
    url = "https://openapi.naver.com/v1/search/book.json"
    params = {
        "query": "요리", 
        "display": 100, # 100개를 한 번에!
        "sort": "sim"   # 일단 정확도순으로 가져옴
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        items = response.json().get('items', [])
        
        # 가져온 책들을 내 DB(Book 모델)에 저장
        for item in items:
            if item.get('isbn'):
                # 제목에서 <b> 태그 제거
                clean_title = item['title'].replace('<b>', '').replace('</b>', '')
                
                # 이미 있는 책은 건너뛰고(get), 없는 책만 생성(create)
                Book.objects.get_or_create(
                    bisbn=item['isbn'],
                    defaults={
                        'btitle': clean_title,
                        'bauthor': item['author'],
                        'bpublisher': item['publisher'],
                        'bpubdate': item['pubdate'],
                        'bprice': int(item.get('discount', 0) or 0),
                        'bimage': item['image'],
                        'blink': item['link'],
                        'bdescription': item['description'],
                        'bhit': 0 # 처음엔 조회수 0
                    }
                )
        return HttpResponse(f"{len(items)}권의 책을 데이터베이스에 저장했습니다!")
    else:
        return HttpResponse("API 호출 실패")


# ------------------------------------------------------------------
# [사용자용] 2. 책 목록 보기 (이제 DB에서만 가져옵니다!)
# ------------------------------------------------------------------
def slist(request):
    
    # 1. 정렬 기준 받기 (기본값: 최신순)
    # url에서 ?sort=popular 같은 꼬리표를 확인합니다.
    sort_param = request.GET.get('sort', 'new')

    # 2. DB에서 모든 책 꺼내오기 (일단 다 가져와서 준비)
    if sort_param == 'popular':
        # 조회수(bhit) 내림차순(-), 그다음 최신순
        qs = Book.objects.all().order_by('-bhit', '-bpubdate')
    else:
        # 신상품(bpubdate) 내림차순(-) (기본값)
        qs = Book.objects.all().order_by('-bpubdate')

    # 3. 페이징 처리 (동료가 알려준 핵심 로직!)
    # 가져온 qs(책 뭉치)를 8개씩 자릅니다.
    paginator = Paginator(qs, 8) 
    
    page_number = request.GET.get('page', 1) # 사용자가 요청한 페이지 번호
    page_obj = paginator.get_page(page_number) # 해당 페이지의 책들만 딱 꺼냄

    context = {
        'books': page_obj,   # 8개만 들어있는 선물상자
        'sort': sort_param,  # 정렬 기준 기억하기 (버튼 색깔 유지용)
    }

    return render(request, 'store/slist.html', context)


# ------------------------------------------------------------------
# [사용자용] 3. 책 상세 보기 (기존 코드 유지)
# ------------------------------------------------------------------
def sview(request, bisbn):
    qs = Book.objects.get(bisbn=bisbn)
    
    # 조회수 증가
    qs.bhit += 1
    qs.save()
    
    context = {'sbook': qs}
    return render(request, 'store/sview.html', context)