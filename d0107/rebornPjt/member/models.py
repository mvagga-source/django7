from django.db import models

class MyUser(models.Model):
    # 1. 아이디/비밀번호
    mem_id = models.CharField(max_length=25, unique=True) # 중복 불가
    mem_pw = models.CharField(max_length=200)
    
    # 2. 기본 정보
    mem_nm = models.CharField(max_length=50)
    nick_nm = models.CharField(max_length=50, unique=True) # 중복 불가
    email = models.CharField(max_length=200,unique=True)  # 중복 불가
    phone_number = models.CharField(max_length=13)
    
    # 3. 주소 (HTML의 zip_code, base_addr, detail_addr 대응)
    zip_code = models.CharField(max_length=10, blank=True, null=True) # 우편번호
    base_addr = models.CharField(max_length=255, blank=True, null=True) # 기본주소
    detail_addr = models.CharField(max_length=255, blank=True, null=True) # 상세주소
    
    # 4. 관심사 및 가입 경로
    # 복수 선택(food_cat)은 보통 콤마(,)로 구분된 문자열로 저장
    food_cat = models.CharField(max_length=200, blank=True, null=True) 
    join_path = models.CharField(max_length=50, blank=True, null=True)
    join_path_etc = models.CharField(max_length=200, blank=True, null=True)
    
    # 5. 가입일 (자동 생성)
    cr_dt = models.DateTimeField(auto_now_add=True)
    
    # 아래 한 줄을 추가해 주세요 (null=True여야 기존 데이터와 충돌이 없습니다)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.mem_id},{self.mem_nm},{self.email},{self.nick_nm}'