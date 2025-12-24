from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# 마이페이지 이동시 비밀번호 확인 폼 추가
class PasswordConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 입력'}),
        label='비밀번호'
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'autocomplete': 'email'
        })
    )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Django 내부객체이기에 기본으로 제공됨. 사용하지 않으려면 None 처리
        # self.fields['username'].help_text = None
        self.fields['username'].help_text = '아이디는 8자이상 영문소문자만 가능합니다.'
        self.fields['email'].help_text = '이메일은 선택사항입니다.'
        self.fields['password1'].help_text = (
            "• 동일한 숫자,문자를 3번 연속으로 사용할 수 없습니다.<br>"
            "• 비밀번호는 최소 8자 이상이어야 합니다.<br>"
            "• 숫자,문자,특수문자 조합으로 가능합니다."
        )
        #-------------------------------------------------
        
        self.fields['username'].widget.attrs.update({
            'placeholder': '사용할 아이디를 입력하세요',
            'autocomplete': 'username'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': '비밀번호 (8자 이상)',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '비밀번호 확인',
            'autocomplete': 'new-password'
        })

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': '아이디',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': '비밀번호',
            'autocomplete': 'current-password'
        })