from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # 쿠키 검색 - request
    # 쿠키 저장 - response
    
    # 쿠키 검색
    cook_info = request.COOKIES
    print("쿠키 모든 정보 : ",cook_info)
    cook_id = request.COOKIES.get("cook_id","") # 쿠키 정보 있으면 "cook_id", 없으면 ""
    print("쿠키 id 정보 : ",cook_id)
    
    response = render(request,'index.html')
    if not cook_id: # 쿠키 정보가 없을때 쿠키 저장 진행
    
        ## 쿠키 저장 / 유지시간이 없으면 브라우저 종료시 사라짐, 시간을 설정하면 시간동안 유지
        response.set_cookie("smsite","ok") # key, value
        response.set_cookie("ip","127.0.0.1:8000",max_age=60*60*24) # key, value  / 60*60*24 = 1day
    
    return response