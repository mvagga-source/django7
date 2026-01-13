from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 1. 매니저 클래스 (MyUser보다 위에 있어야 함)
class MyUserManager(BaseUserManager):
    def create_user(self, mem_id, mem_nm, password=None):
        if not mem_id:
            raise ValueError('아이디는 필수입니다.')
        user = self.model(mem_id=mem_id, mem_nm=mem_nm)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mem_id, mem_nm, password=None):
        user = self.create_user(mem_id, mem_nm, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# 2. 유저 모델 (AbstractBaseUser 상속으로 수정)
class MyUser(AbstractBaseUser):
    # --- 기존 필드 유지 ---
    mem_id = models.CharField(max_length=25, unique=True)
    mem_pw = models.CharField(max_length=200) # 직접 관리하는 비번 필드
    
    mem_nm = models.CharField(max_length=50)
    nick_nm = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=13)
    
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    base_addr = models.CharField(max_length=255, blank=True, null=True)
    detail_addr = models.CharField(max_length=255, blank=True, null=True)
    
    food_cat = models.CharField(max_length=200, blank=True, null=True) 
    join_path = models.CharField(max_length=50, blank=True, null=True)
    join_path_etc = models.CharField(max_length=200, blank=True, null=True)
    
    cr_dt = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # --- 필수 추가 항목 ---
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'mem_id'      # 로그인 시 ID로 사용할 필드
    REQUIRED_FIELDS = ['mem_nm']    # 슈퍼유저 생성 시 필수로 물어볼 필드

    def __str__(self):
        return f'{self.mem_id},{self.mem_nm},{self.email},{self.nick_nm}'

    # 관리자 페이지 및 권한 확인을 위한 필수 메서드 (수정 불필요)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    # 비밀번호 필드를 mem_pw로 쓰고 계시므로 장고 표준 password 필드와 연결 (호환성)
    @property
    def password(self):
        return self.mem_pw

    @password.setter
    def password(self, raw_password):
        self.set_password(raw_password)