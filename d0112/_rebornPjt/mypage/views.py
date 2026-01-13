from django.contrib import messages
from django.shortcuts import redirect, render
from member.models import MyUser
from django.http import JsonResponse
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# 유저 모델 가져오기
User = get_user_model()

# 1. 정보 수정 화면 보여주기

def mychange(request):
    # 로그인 안 된 사용자는 로그인 페이지로 (선택 사항)
    # if not request.user.is_authenticated:
    if not request.session.get('user_id'):
        return redirect('member:login')
    return render(request, 'mypage/mychange.html')

# 2. 정보 수정 데이터 처리
def mychange_update(request):
    if request.method == "POST":
        # 폼에서 넘어온 아이디로 유저 찾기
        mem_id = request.POST.get('mem_id')
        try:
            user = User.objects.get(mem_id=mem_id)
            
            # 데이터 업데이트
            user.mem_nm = request.POST.get('mem_nm')
            user.nick_nm = request.POST.get('nick_nm')
            user.email = request.POST.get('email')
            user.zip_code = request.POST.get('zip_code')
            user.base_addr = request.POST.get('base_addr')
            user.detail_addr = request.POST.get('detail_addr')
            
            # 비밀번호 변경 여부 확인
            new_pw = request.POST.get('mem_pw')
            if new_pw:
                user.mem_pw = make_password(new_pw)  # ✅ mem_pw에 암호화해서 저장
            
            # DB 저장
            user.save()
            
            # 무조건 로그아웃 처리 후 로그인 페이지로 리다이렉트
            logout(request)
            messages.success(request, "정보 수정이 완료되었습니다. 다시 로그인해 주세요.")
            return redirect('/member/login/')
            
        except User.DoesNotExist:
            messages.error(request, "사용자를 찾을 수 없습니다.")
            return redirect('mypage:mychange')
    
    # POST 요청이 아닐 경우
    return redirect('mypage:mychange')

def check_duplicate(request):
    field = request.GET.get('field') # 'nick_nm' 또는 'email'
    value = request.GET.get('value')
    
    # 본인의 현재 값과는 중복되어도 상관없으므로 제외하고 검색
    exists = User.objects.exclude(mem_id=request.user.mem_id).filter(**{field: value}).exists()
    
    return JsonResponse({'exists': exists})

def myaccount(request):
    # 회원탈퇴 페이지나 계정 관리 페이지를 렌더링합니다.
    # 해당 html 파일이 없다면 일단 아래처럼 작성해 두세요.
    return render(request, 'mypage/myaccount.html')