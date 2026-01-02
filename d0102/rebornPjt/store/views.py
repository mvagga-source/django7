from django.shortcuts import render
import requests
from .models import Book
from secret import api__func

# 책정보 상세보기 
def sview(request,bisbn):
    
    print("도서 고유번호: ",bisbn)
    
    # Book테이블에서 < bisbn = 1 >
    qs= Book.objects.get(bisbn=bisbn)
    
    # [추가] 조회수 증가 로직 (여기가 핵심!)
    qs.bhit += 1   # 현재 조회수에 1을 더함
    qs.save()      # 변경된 내용을 DB에 "저장" (이걸 해야 반영됨)
    context= {'sbook':qs}
    
    return render(request,'store/sview.html',context)


# 책카드 목록보기
def slist(request):
    
    # 1. API 키 설정
    secret__list= api__func.naver__API()
    client_id= secret__list[0]
    client_secret= secret__list[1]

    # 2. 사용자 검색어 및 페이지 계산 (**API 호출 전에** 해야 함!)
    user_input = request.GET.get('query', '')
    page = int(request.GET.get('page', 1))
    
    # [1번 위치] 정렬 기준(sort) 받기
    # 손님이 버튼을 눌러서 보낸 'sort' 값을 받습니다. 없으면 기본값은 'sim'(정확도순)
    sort_param = request.GET.get('sort', 'sim')
    
    display_count = 8
    start_index = (page - 1) * display_count + 1

    # 검색어 필터링 로직
    if user_input:
        target_query = f"{user_input} 요리"
    else:
        target_query = "요리"
    
        
    # [1.5번 위치] 네이버 API에게 보낼 정렬 조건 설정
    # 만약 손님이 '신상품순(new)'을 원하면, 네이버 API 코드인 'date'로 바꿔줍니다.
    # (인기순은 네이버가 모르니 그냥 'sim'으로 둡니다)
    if sort_param == 'new':
        naver_sort = 'date'
    else:
        naver_sort = 'sim'

    # 3. 네이버 API 호출 준비
    url = "https://openapi.naver.com/v1/search/book.json"
    headers = {
        "X-Naver-Client-Id": 'C_MasXzr3nCzi13g19wN',
        "X-Naver-Client-Secret": 'mUtwlSX2ES'
    }
    params = {
        "query": target_query,
        "display": display_count, 
        "sort": "sim",
        "start": start_index  # 계산된 시작 위치 적용
    }

    # 템플릿에 보낼 선물 가방 미리 준비
    context = {
        'search_query': user_input,
        'current_page': page,
        'books': [] # 일단 빈 리스트로 시작
    }

    try:
        # 4. 실제 API 호출
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', []) # 네이버가 준 책 8권 리스트
            
            saved_books = [] # DB에 저장하거나 화면에 보여줄 책들을 담을 바구니

            # ★ 핵심 수정: 리스트(items)는 반드시 반복문(for)을 돌려야 함
            for item in items:
                # ISBN이 있는 경우만 처리
                if item.get('isbn'):
                    # DB에 저장 (이미 있으면 가져오고, 없으면 생성)
                    # 주의: models.py의 필드명과 정확히 일치해야 합니다. (예: title, author...)
                    book, created = Book.objects.get_or_create(
                        
                        # 검색조건
                        bisbn=item['isbn'],
                        # 책이 없어서 새로 만들어야 할 때 사용하는 정보들
                        defaults={
                            'btitle': item['title'].replace('<b>', '').replace('</b>', ''),
                            'bauthor': item['author'],
                            'bpublisher': item['publisher'],
                            'bpubdate': item['pubdate'],
                            'bprice': int(item['discount']),
                            'bimage': item['image'],
                            'blink': item['link'],
                            'bdescription': item['description']
                        }
                    )
                    saved_books.append(book)
            
            
            # [2번 위치] 인기순 정렬 로직 (우리 DB 데이터로 줄 세우기)
            # 네이버에서 다 받아와서 saved_books에 넣은 다음,
            # 만약 'popular'라면 조회수(bhit)를 기준으로 내림차순 정렬합니다.
            if sort_param == 'popular':
                # 파이썬 리스트 정렬 기능(sort)을 사용합니다.
                # reverse=True는 '큰 숫자부터(내림차순)'라는 뜻입니다.
                saved_books.sort(key=lambda x: x.bhit, reverse=True)

            # 정렬이 끝난 목록을 context에 담기
            context['books'] = saved_books
            print(f"저장된 책 {len(saved_books)}권을 {sort_param} 기준으로 보여줍니다.")

        else:
            print(f"API 에러 발생: {response.status_code}")

    except Exception as e:
        print(f"서버 에러: {e}")

    # 5. 최종 렌더링
    return render(request, 'store/slist.html', context)