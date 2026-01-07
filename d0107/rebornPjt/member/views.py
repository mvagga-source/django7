from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse # 서버가 브라우저에 응답을 보낼 때 쓰는 도구들
from .models import MyUser # 우리가 만든 회원 창고(모델)를 가져온다
from django.contrib.auth.hashers import make_password # 비밀번호를 암호화해주는 도구
from django.contrib.auth.hashers import check_password # 입력한 비번과 암호화된 비번이 맞는지 확인하는 도구
from django.contrib import messages # 화면에 "성공", "오류" 메시지를 잠시 띄워주는 도구
from django.contrib.auth import login as auth_login # 이름 중복 방지
from .models import MyUser

#-----------------------------로그인 페이지------------------------------------
def login(request):
    # 사용자가 로그인 버튼을 눌러서 데이터를 보냈을 때 (POST 방식)
    if request.method == 'POST':
        # 입력된 데이터값을
        user_id = request.POST.get('id') # 입력창에 쓴 아이디 가져오기
        user_pw = request.POST.get('pw') # 입력창에 쓴 비밀번호 가져오기
        # 콘솔창에 띄운다.
        print(f"아이디 : {user_id}")
        print(f"비밀번호 : {user_pw}")
        
        
        
        # 1. DB(창고)에서 사용자가 입력한 아이디로 회원 정보를 찾기
        # .filter().first()는 유저가 없으면 에러 대신 None을 돌려줘서 편리
        user = MyUser.objects.filter(mem_id=user_id).first()

        # 2. 비밀번호 대조 (암호화된 비번과 입력받은 비번 비교)
        # 회원이 존재하고(user) + 비밀번호도 맞는지(check_password) 확인
        if user and check_password(user_pw, user.mem_pw):
            print(f"로그인 성공!!! 사용자 이름: {user.mem_nm}")
            
            
            # last_login 필드가 없어도 에러가 나지 않도록 속성 설정
            user.last_login = None 
            
            # auth_login을 호출하되, 내부적으로 save()가 호출될 때 
            # last_login 필드를 찾지 않도록 처리하는 대신 
            # 아래처럼 모델 인스턴스에 속성만 부여한 뒤 진행합니다.
            # [중요] Django 표준 로그인 처리를 먼저 
            # 이 코드가 실행되어야 @login_required가 "아, 이 사람 로그인했구나!"라고 인식
            auth_login(request, user)
            
            # 로그인 성공 시 세션에 유저 정보 저장 / 서버 세션(비밀 메모장)에 로그인했다는 증거
            request.session['login_user'] = user.mem_id
            request.session['user_id'] = user.mem_id
            request.session['user_nm'] = user.nick_nm
            return redirect('/') # 메인 페이지로 이동
        else:
            # 아이디가 없거나 비번이 틀린 경우 모두 여기서 처리
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            # 다시 로그인 페이지를 보여주되, 입력했던 아이디는 남겨줘서 편리하게
            return render(request, 'member/login.html', {'id': user_id})
        
        

    # GET 방식(처음 페이지 접속)일 때 실행    
    return render(request, 'member/login.html')
        
    #     return redirect('/')
    # else:
    #     return render(request,'member/login.html')
    

# ------------------------------- [회원가입 단계별 페이지] -------------------------------------
# 회원가입 페이지
def join(request):
    return render(request,'member/join.html')

# 회원가입 페이지-1
def join1(request):
    return render(request,'member/join1.html')


# 회원가입 페이지-2
# ------------------------- [회원가입 2단계: 정보 입력 및 중복 확인] -----------------------------
def join2(request):
    # 페이지를 보여줄 때
    if request.method == "GET":
        return render(request,'member/join2.html')
    
    # '다음' 버튼을 눌러서 정보를 보냈을 때
    elif request.method == "POST":
        # 1. 사용자가 입력한 정보들을 서버의 임시 보관함(세션)에 'temp_data'라는 이름으로 잠시 보관
        # 왜냐하면 3단계(주소 입력)까지 가야 최종적으로 DB에 저장할 수 있기 때문
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


# 회원가입 페이지-2
# ------------------------------- [중복 확인 기능 (Ajax용)] -----------------------------------
def check_duplicate(request):
    field_type = request.GET.get('type') # '아이디'인지 '닉네임'인지 종류 확인
    value = request.GET.get('value') # 실제 입력한 값 확인
    
    is_available = True # 처음에는 사용 가능하다고 설정
    
    # DB 창고에서 해당 값이 이미 존재하는지 뒤져보기
    if field_type == 'mem_id':
        if MyUser.objects.filter(mem_id=value).exists():
            is_available = False # 이미 있으면 사용 불가!
    elif field_type == 'nick_nm':
        if MyUser.objects.filter(nick_nm=value).exists():
            is_available = False
    elif field_type == 'email':
        if MyUser.objects.filter(email=value).exists():
            is_available = False
    # 결과를 자바스크립트가 이해할 수 있는 JSON 형태로 돌려준다.      
    return JsonResponse({'is_available': is_available})


# 회원가입 페이지-3 
# ------------------------------ [회원가입 3단계: 주소 입력 및 최종 저장] --------------------------------
def join3(request):
    # 2단계에서 세션에 넣어둔 임시 데이터를 꺼내온다.
    # 세션에 저장된 데이터가 있는지 확인. (없으면 1단계로 쫓아냄)
    temp_data = request.session.get('temp_data')
    
    # 혹시나 보관함이 비어있다면(잘못된 접근) 1단계로 쫓아낸다.
    if not temp_data:
        messages.error(request, "잘못된 접근입니다. 처음부터 다시 가입해주세요.")
        return redirect('member:join1')
    
    if request.method == "GET":
        return render(request,'member/join3.html')
    elif request.method == "POST":
        # 1. 3단계에서 입력한 주소와 관심사 정보를 가져온기
        z_code = request.POST.get('zip_code')
        b_addr = request.POST.get('base_addr')
        d_addr = request.POST.get('detail_addr')
        
        # 체크박스(음식 카테고리) 여러 개 가져오기
        # 2. 여러 개 선택한 음식 카테고리를 리스트로 받아와서 "한식,중식" 처럼 글자로 합친다.
        f_cats = request.POST.getlist('food_cat')
        f_cat_str = ",".join(f_cats) # 예: "한식,중식"
        
        j_path = request.POST.get('join_path') # 가입 경로
        
        # db저장 부분
        # 데이터를 DB에 최종 저장 (비밀번호는 꼭 암호화해서 저장! temp_data에 있던 정보 + join3 정보 합체)
        # 3. [최종 합체] 보관함(세션) 데이터 + 지금 입력한 데이터를 모아 DB 모델 객체를 만듭니다.
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
        
        # 4. DB 창고에 실제로 저장
        user.save() 
        
        # 5. 저장이 끝났으니 임시 보관함(세션)은 깨끗하게 지워준다.
        del request.session['temp_data']
        
        # 6. 성공 메시지를 담아 로그인 페이지로 보내기
        messages.success(request, "가입을 축하드립니다. 로그인 후 더욱 다양한 reborn을 둘러보세요!")
        # 저장이 끝났으면 로그인 페이지로 보낸다.
        return redirect('member:login') # 로그인 페이지로 이동
        
        
# -------------------------------------- [로그아웃 기능] -----------------------------------------------
def logout_view(request):
    # 세션(서버의 비밀 메모장)을 완전히 비워서 로그아웃
    request.session.flush()
    
    # 비운 뒤에 메인 페이지('/')로 
    return redirect('/')