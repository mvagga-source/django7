from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MyUser # 우리가 만든 회원 창고(모델)를 가져온다
from django.contrib.auth.hashers import make_password # 비밀번호를 암호화해주는 도구
from django.contrib.auth.hashers import check_password # 비밀번호 확인 도구
from django.contrib import messages
from django.shortcuts import redirect

# 로그인 페이지
def login(request):
    if request.method == 'POST':
        # 입력된 데이터값을
        user_id = request.POST.get('id')
        user_pw = request.POST.get('pw')
        # 콘솔창에 띄운다.
        print(f"아이디 : {user_id}")
        print(f"비밀번호 : {user_pw}")
        
        
        
        # 1. DB에서 아이디로 유저 찾기
        # .filter().first()는 유저가 없으면 에러 대신 None을 돌려줘서 편리
        user = MyUser.objects.filter(mem_id=user_id).first()

        # 2. 비밀번호 대조 (암호화된 비번과 입력받은 비번 비교)
        if user and check_password(user_pw, user.mem_pw):
            print(f"로그인 성공!!! 사용자 이름: {user.mem_nm}")
            # 로그인 성공 시 세션에 유저 정보 저장
            request.session['login_user'] = user.mem_id
            request.session['user_id'] = user.mem_id
            request.session['user_nm'] = user.mem_nm
            return redirect('/') # 메인 페이지로 이동
        else:
            # 아이디가 없거나 비번이 틀린 경우 모두 여기서 처리
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            # 입력했던 아이디는 남겨줘서 사용자를 배려
            return render(request, 'member/login.html', {'id': user_id})

    # GET 방식(처음 페이지 접속)일 때 실행    
    return render(request, 'member/login.html')
        
    #     return redirect('/')
    # else:
    #     return render(request,'member/login.html')
    


# 회원가입 페이지
def join(request):
    return render(request,'member/join.html')

# 회원가입 페이지-1
def join1(request):
    return render(request,'member/join1.html')

# 회원가입 페이지-2
def join2(request):
    if request.method == "GET":
        return render(request,'member/join2.html')
    elif request.method == "POST":
        # 1. 사용자가 입력한 데이터를 서버 메모리(세션)에 'temp_data'라는 이름으로 잠시 보관
        request.session['temp_data'] = {
            'mid': request.POST.get('mem_id'),
            'mpw': request.POST.get('mem_pw'),
            'mnm': request.POST.get('mem_nm'),
            'nnm': request.POST.get('nick_nm'),
            'eml': request.POST.get('email'),
            'phn': request.POST.get('phone_number'),
        }
        # 2. 데이터를 담았으니 바로 다음 단계 페이지로 이동
        return redirect('member:join3')


# 회원가입 페이지-3 (주소/관심사 입력 및 최종 저장 단계)
def join3(request):
    # 세션에 저장된 데이터가 있는지 확인. (없으면 1단계로 쫓아냄)
    temp_data = request.session.get('temp_data')
    if not temp_data:
        messages.error(request, "잘못된 접근입니다. 처음부터 다시 가입해주세요.")
        return redirect('member:join1')
    
    if request.method == "GET":
        return render(request,'member/join3.html')
    elif request.method == "POST":
        # # HTML의 name="mem_id" 등으로 적었던 데이터들을 가져온다.
        # # Hidden으로 숨겨왔던 join2 데이터들
        # mid = request.POST.get('mem_id')
        # mpw = request.POST.get('mem_pw')
        # mnm = request.POST.get('mem_nm')
        # nnm = request.POST.get('nick_nm')
        # eml = request.POST.get('email')
        # phn = request.POST.get('phone_number')
        
        # join3에서 새로 입력한 데이터들
        z_code = request.POST.get('zip_code')
        b_addr = request.POST.get('base_addr')
        d_addr = request.POST.get('detail_addr')
        
        # 체크박스(음식 카테고리) 여러 개 가져오기
        f_cats = request.POST.getlist('food_cat')
        f_cat_str = ",".join(f_cats) # 예: "한식,중식"
        
        j_path = request.POST.get('join_path')
        
        # db저장 부분
        # 데이터를 DB에 저장 (비밀번호는 꼭 암호화해서 저장!)
        # DB에 최종 저장 (temp_data에 있던 정보 + join3 정보 합체)
        user = MyUser(
            mem_id = temp_data['mid'],
            mem_pw = make_password(temp_data['mpw']), # 비밀번호 암호화
            mem_nm = temp_data['mnm'],
            nick_nm = temp_data['nnm'],
            email = temp_data['eml'],
            phone_number = temp_data['phn'],
            zip_code = z_code,
            base_addr = b_addr,
            detail_addr = d_addr,
            food_cat = f_cat_str,
            join_path = j_path
        )
        
        user.save() # 실제로 DB에 저장하는 순간!
        
        # 저장이 끝났으니 서버에 메모리(세션)를 비워준다.
        del request.session['temp_data']
        
        # 가입 축하 메시지 등록
        messages.success(request, "가입을 축하드립니다. 로그인 후 더욱 다양한 reborn을 둘러보세요!")
        # 저장이 끝났으면 로그인 페이지로 보냅니다.
        return redirect('member:login') # 로그인 페이지로 이동
        
        # # 저장이 끝났으면 03단계(완료 페이지)로 보냅니다.
        # return redirect('/') 
        # # return redirect('member:join2') # 잘못 들어오면 다시 뒤로

# def join_save(request):
#     if request.method == "POST":
#         return redirect('/?result=1') # 잘못 들어오면 다시 뒤로


def logout_view(request):
    # 1. 세션 바구니를 완전히 비웁니다 (로그인 정보 삭제)
    request.session.flush()
    
    # 2. 비운 뒤에 메인 페이지('/')로 보냅니다
    return redirect('/')