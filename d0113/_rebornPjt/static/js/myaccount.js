let isPasswordValid = false;

// 1. 비밀번호 보이기/숨기기 토글
function togglePasswordVisibility() {
    const pwInput = document.getElementById('current_pw');
    const icon = document.querySelector('.toggle-pw-icon');
    if (pwInput.type === 'password') {
        pwInput.type = 'text';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    } else {
        pwInput.type = 'password';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    }
}

// 2. 실시간 비밀번호 검증 (서버 통신)
const passwordInput = document.getElementById('current_pw');
const errorMsg = document.getElementById('pw_error_msg');

passwordInput.addEventListener('input', function() {
    const password = this.value;

    // 입력창이 비어있으면 에러 메시지 삭제 및 상태 초기화
    if (password.length === 0) {
        errorMsg.innerText = "";
        isPasswordValid = false;
        return;
    }

    // 서버의 비밀번호 확인 엔드포인트로 요청
    fetch('/mypage/check_password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `password=${encodeURIComponent(password)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_valid) {
            // 비밀번호가 맞으면 빨간 문구 제거
            errorMsg.innerText = "";
            isPasswordValid = true;
        } else {
            // 틀리면 즉시 빨간 문구 출력
            errorMsg.innerText = "비밀번호가 일치하지 않습니다.";
            isPasswordValid = false;
        }
    })
    .catch(error => {
        console.error('검증 오류:', error);
        isPasswordValid = false;
    });
});

// 3. 탈퇴하기 버튼 클릭 시 로직
document.getElementById('btn-submit').addEventListener('click', function() {
    const agreeCheck = document.getElementById('agree_check');

    // 실시간 검증 통과 여부 확인
    if (!isPasswordValid) {
        errorMsg.innerText = "비밀번호가 일치하지 않습니다.";
        passwordInput.focus();
        return;
    }
    
    // 동의 여부 확인
    if (!agreeCheck.checked) {
        alert("주의사항 확인 및 동의에 체크해 주세요.");
        return;
    }

    // 최종 컨펌 후 탈퇴 처리
    if (confirm("정말 탈퇴하시겠습니까? 확인 즉시 계정이 삭제되고 홈 화면으로 이동합니다.")) {
        fetch('/mypage/delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 탈퇴 성공 시 홈 화면(로그인 전 화면)으로 리다이렉트
                window.location.href = '/'; 
            } else {
                alert("탈퇴 처리 중 오류가 발생했습니다.");
            }
        })
        .catch(error => {
            console.error('탈퇴 처리 중 에러:', error);
            alert("서버 통신 중 오류가 발생했습니다.");
        });
    }
});