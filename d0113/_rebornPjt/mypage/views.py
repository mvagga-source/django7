from django.contrib import messages
from django.shortcuts import redirect, render
from member.models import MyUser  
from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password, check_password as django_check_password

# 1. 정보 수정 화면 보여주기 (유지)
def mychange(request):
    user_session_id = request.session.get("user_id")
    if not user_session_id:
        return redirect('member:login')

    try:
        user = MyUser.objects.filter(mem_id=user_session_id).first()
        if not user:
            messages.error(request, "사용자 정보를 찾을 수 없습니다.")
            return redirect('member:login')
        return render(request, 'mypage/mychange.html', {'user': user})
    except Exception as e:
        print(f"Error: {e}")
        return redirect('member:login')

# 2. 정보 수정 데이터 처리 (유지)
def mychange_update(request):
    if request.method == "POST":
        mem_id = request.POST.get('mem_id')
        try:
            user = MyUser.objects.get(mem_id=mem_id)
            user.mem_nm = request.POST.get('mem_nm')
            user.nick_nm = request.POST.get('nick_nm')
            user.email = request.POST.get('email')
            user.zip_code = request.POST.get('zip_code')
            user.base_addr = request.POST.get('base_addr')
            user.detail_addr = request.POST.get('detail_addr')
            
            new_pw = request.POST.get('mem_pw')
            if new_pw:
                user.mem_pw = make_password(new_pw) 
            
            user.save()
            
            if "user_id" in request.session:
                del request.session["user_id"]
            auth_logout(request)
            
            messages.success(request, "정보 수정이 완료되었습니다. 다시 로그인해 주세요.")
            return redirect('member:login')
            
        except MyUser.DoesNotExist:
            messages.error(request, "수정하려는 사용자 정보를 찾을 수 없습니다.")
            return redirect('mypage:mychange')
        except Exception as e:
            messages.error(request, f"오류가 발생했습니다: {str(e)}")
            return redirect('mypage:mychange')
    return redirect('mypage:mychange')

# 3. 중복 확인 (유지)
def check_duplicate(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    current_user_id = request.session.get("user_id")
    exists = MyUser.objects.exclude(mem_id=current_user_id).filter(**{field: value}).exists()
    return JsonResponse({'exists': exists})

# 4. 계정 관리(탈퇴) 페이지 호출
def myaccount(request):
    return render(request, 'mypage/myaccount.html')

# 5. 실시간 비밀번호 검증 (수정됨: 세션 기반 DB 대조)
def check_password(request):
    if request.method == 'POST':
        input_pw = request.POST.get('password', '')
        user_id = request.session.get("user_id")
        
        try:
            user = MyUser.objects.get(mem_id=user_id)
            # 장고의 암호화된 비번과 입력 비번을 대조
            is_valid = django_check_password(input_pw, user.mem_pw)
            return JsonResponse({'is_valid': is_valid})
        except MyUser.DoesNotExist:
            return JsonResponse({'is_valid': False}, status=404)
            
    return JsonResponse({'is_valid': False}, status=400)

# 6. 회원 탈퇴 처리 (수정됨: 탈퇴 후 세션 삭제 및 홈 이동 준비)
def delete_user(request):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        try:
            user = MyUser.objects.get(mem_id=user_id)
            user.delete()  # 실제 데이터 삭제
            
            # 세션 삭제 및 로그아웃 처리
            if "user_id" in request.session:
                del request.session["user_id"]
            auth_logout(request)
            
            return JsonResponse({'status': 'success'})
        except MyUser.DoesNotExist:
            return JsonResponse({'status': 'fail'}, status=404)
            
    return JsonResponse({'status': 'fail'}, status=400)