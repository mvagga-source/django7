from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, PasswordConfirmForm
from django.contrib.auth import authenticate

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "회원가입 완료! 바로 시작해보자 😎")
            return redirect('pages:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "로그인 성공!")
            return redirect('pages:home')
        else:
            messages.error(request, "로그인 실패. 아이디/비번 확인 ㄱㄱ")
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "로그아웃 완료.")
    return redirect('pages:home')

@login_required
def profile_view(request):
    return redirect('accounts:profile_confirm')

@login_required
def profile_confirm_view(request):
    if request.method == 'POST':
        form = PasswordConfirmForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            if user:
                return render(request, 'accounts/profile.html')
            form.add_error('password', '비밀번호가 틀렸습니다.')
    else:
        form = PasswordConfirmForm()
    return render(request, 'accounts/profile_confirm.html', {'form': form})