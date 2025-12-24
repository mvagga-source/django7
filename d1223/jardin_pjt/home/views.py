from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json
from django.conf import settings


from home.models import ChartData

def index(request):
    return render(request,'main.html')

def my_map(request):
    return render(request,'my_map.html')

def chart2(request):
    return render(request,'chart2.html')



# ----------------------------------------
KAKAO_API_KEY='DEVAB1B66151B3EB7CA7FD58C60D6F7D04218058'
KAKAOPAY_BASE_URL = 'https://open-api.kakaopay.com/online/v1/payment/ready'

# 1. 카카오페이 연결을 위한 페이지
def kakao_pay(request):
    return render(request,'kakao_pay.html')

# 2. 카카오페이 결제 준비 API 호출
@csrf_exempt
def prepare_payment(request):
    headers = {
      "Authorization":f"SECRET_KEY {KAKAO_API_KEY}",
      "Content-Type":"application/json",
    }

    
    print("headers : ",headers)
    
    data = {
      "cid": "TC0ONETIME",  # 테스트용 CID, 상용은 발급받은 CID 사용
      "partner_order_id": "order_id_12345",  # 고유 주문 ID
      "partner_user_id": "user_id_67890",  # 고유 사용자 ID
      "item_name": "초코파이",  # 상품명
      "quantity": "1",  # 수량 (0이 아닌 양수)
      "total_amount": "1000",  # 총 결제 금액 (0보다 커야 함)
      "vat_amount": "100",  # 부가세 금액 (총 금액보다 작거나 같아야 함)
      "tax_free_amount": "0",  # 비과세 금액 (생략 가능)
      "approval_url": "http://127.0.0.1:8000/paySuccess",
      "cancel_url": "http://127.0.0.1:8000/payFail",
      "fail_url": "http://127.0.0.1:8000/payCancel",
    }
    
    print("KAKAOPAY_BASE_URL : ",KAKAOPAY_BASE_URL)
    print("전송 데이터:", json.dumps(data, ensure_ascii=False))
    
    response = requests.post(KAKAOPAY_BASE_URL, headers=headers, data=json.dumps(data, ensure_ascii=False))

    result = response.json()
    print("결과 : ",result)

    # 결과 넘어옴.
    request.session["tid"] = result["tid"]

    if response.status_code == 200:
        print("다음 결과 url : ",result["next_redirect_pc_url"])
        return JsonResponse({"next_redirect_pc_url": result["next_redirect_pc_url"]})
    else:
        return JsonResponse({"error": result}, status=400)


# approval_url
def paySuccess(request):
    context = {'dd_data':''}
    return HttpResponse('성공')
# payFail
def payFail(request):
    context = {'dd_data':''}
    return HttpResponse('실패')
# payCancel
def payCancel(request):
    context = {'dd_data':''}
    return HttpResponse('취소')
#-----------------------------------------


# @csrf_exempt  # csrf_token 예외처리
# 단순데이터 처리
def chart_json(request):
    context = {'dd_data':[10, 5, 9, 8, 3, 6],'ll_data':['홍길동','유관순','이순신','강감찬','김구','김유신']}
    return JsonResponse(context)

# db데이터 처리
def chart_json2(request):
    qs = ChartData.objects.all()
    l_qs = list(qs.values()) 
    
    context = {'list_data':l_qs}
    return JsonResponse(context)
