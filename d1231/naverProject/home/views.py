from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
import requests
import urllib.request

def index(request):
    
    client_id = 'j7KaOMGirpd_EoxbjKDB'
    client_secret = '98WTnc2agN'
    
    encText = urllib.parse.quote("블루리본매거진")
    max_display = 10
    # JSON 결과
    # url = f"https://openapi.naver.com/v1/search/book.json?query={encText}&display={max_display}"
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        # print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
    
    
    # JSON -> 딕셔너리 타입변환
    data = json.loads(response_body)
    print(data)
    
    # list 추출
    book_list = data['items']
    # print(book_list)
    
    context = {"list":book_list}
    
    return render(request,'index.html',context)




[{'title': '&lt;<b>블루리본</b> 서베이 <b>매거진</b>&gt;에 소개되었습니다.', 'link': 'https://blog.naver.com/gute_leute/222625197824', 'description': '© <b>블루리본</b>서베이<b>매거진</b> 소개해 주신 <b>블루리본</b>서베이 에디터 님께 감사의 말씀을 전하며, 늘 함께해주시는 여러분들께 보답할 수 있는 구테로이테 되겠습니다. 콘텐츠 전문은 아래 링크에서 만나보실 수... ', 'bloggername': '좋은사람들 구테로이테', 'bloggerlink': 'blog.naver.com/gute_leute', 'postdate': '20220118'}, {'title': '신사역 카페 커피휘엘 11년 연속 <b>블루리본</b> 로스터리 커피', 'link': 'https://blog.naver.com/kh750/224128469135', 'description': '서적과 <b>매거진</b>들이 놓여 있어 커피휘엘이 지향하는 예술적 감성을 엿볼 수 있게 합니다 매장 중앙에 는 빨간 <b>리본</b>이 가득 달린 대형 크리스마스트리가 자리 잡고 있어 방문객들에게 포근하고 설레는 연말... ', 'bloggername': '커피사랑 경화의 소소하고 맛깔난 이야기들', 'bloggerlink': 'blog.naver.com/kh750', 'postdate': '20251231'}, {'title': '논실커피 <b>블루리본</b> 12년째 인증 카페', 'link': 'https://blog.naver.com/sohory/223850198710', 'description': '리 본 두 개 맛집은 140개로 2024년 판과 동일하며, 리본 한 개 맛집은 1,526개로 2024년 판보다 122개가... 맛집가이드북 #<b>블루리본매거진</b> #블루리본 #블루리본20주년 #블루리본서베이20주년... ', 'bloggername': 'Nonsilcoffee Roasters', 'bloggerlink': 'blog.naver.com/sohory', 'postdate': '20250429'}, {'title': '<b>블루리본</b> 뜻과 의미, 선정 기준 <b>블루리본</b> 서베이 받는법', 'link': 'https://blog.naver.com/hananharu/223374367848', 'description': '<b>블루리본</b> 서베이 <b>매거진</b> 음식에 관련된 다양한 뉴스, 인플루언서 칼럼, <b>블루리본</b> 맛집 서적 등 다양한 <b>매거진</b>을 제공하고 있으며 <b> 블루리본</b> 서베이 맛집 검색 음식점에 대한 메뉴, 가격대 위치정보, 리뷰를 볼 수... ', 'bloggername': '우당탕탕 퍼포먼스 마케터', 'bloggerlink': 'blog.naver.com/hananharu', 'postdate': '20240306'}, {'title': '&lt;<b>블루리본</b> 서베이 <b>매거진</b>&gt;에 구테로이테 에피소드점이... ', 'link': 'https://blog.naver.com/gute_leute/222779577307', 'description': " 한국형 미슐랭가이드 &lt;<b>블루리본</b> 서베이 <b>매거진</b>&gt;에 구테로이테 수유 에피