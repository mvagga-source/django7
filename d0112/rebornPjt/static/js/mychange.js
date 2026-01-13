// 전역 변수
var isNickValid = true;
var isEmailValid = true;
var initialNick = "";
var initialEmail = "";

// 초기값 세팅
document.addEventListener('DOMContentLoaded', function() {
    var nInput = document.getElementById('nick_nm');
    var eInput = document.getElementById('email');

    if (nInput) {
        initialNick = nInput.value;
        nInput.addEventListener('input', function() {
            // 초기값과 다르면 중복확인 다시 해야함
            isNickValid = (nInput.value === initialNick);
        });
    }
    if (eInput) {
        initialEmail = eInput.value;
        eInput.addEventListener('input', function() {
            isEmailValid = (eInput.value === initialEmail);
        });
    }
});

// 중복 확인
function checkDuplicate(fieldId) {
    var inputElement = document.getElementById(fieldId);
    if (!inputElement) return;

    var val = inputElement.value.trim();
    var fieldName = (fieldId === 'nick_nm') ? '닉네임' : '이메일';

    if (!val) {
        alert(fieldName + "을 입력해주세요.");
        return;
    }

    if ((fieldId === 'nick_nm' && val === initialNick) || (fieldId === 'email' && val === initialEmail)) {
        alert("현재 사용 중인 " + fieldName + "입니다.");
        if (fieldId === 'nick_nm') isNickValid = true;
        else isEmailValid = true;
        return;
    }

    var url = "/mypage/check-duplicate/?field=" + fieldId + "&value=" + encodeURIComponent(val);
    
    fetch(url)
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (data.exists) {
                alert("이미 사용 중인 " + fieldName + "입니다.");
                if (fieldId === 'nick_nm') isNickValid = false;
                else isEmailValid = false;
            } else {
                alert("사용 가능한 " + fieldName + "입니다.");
                if (fieldId === 'nick_nm') isNickValid = true;
                else isEmailValid = true;
            }
        })
        .catch(function(err) {
            console.error(err);
            alert("통신 오류가 발생했습니다.");
        });
}

// 폼 검사 (수정완료 버튼 클릭 시 실행)
function validateForm() {
    var p1 = document.getElementById('password').value;
    var p2 = document.getElementById('password_confirm').value;

    // 1. 비밀번호 입력했을 경우에만 일치 확인
    if (p1 || p2) {
        if (p1 !== p2) {
            alert("비밀번호가 일치하지 않습니다.");
            return false;
        }
    }

    // 2. 중복 확인 체크
    if (!isNickValid) {
        alert("닉네임 중복 확인을 해주세요.");
        return false;
    }
    if (!isEmailValid) {
        alert("이메일 중복 확인을 해주세요.");
        return false;
    }

    return confirm("정말로 수정하시겠습니까?");
}

// 비밀번호 일치 실시간 검사 (ID 수정: password_match_message -> pw_match_msg)
function checkPasswordMatch() {
    var p1 = document.getElementById('password');
    var p2 = document.getElementById('password_confirm');
    var msg = document.getElementById('pw_match_msg'); // HTML ID와 일치시킴

    if (!p1 || !p2 || !msg) return;

    var val1 = p1.value;
    var val2 = p2.value;

    if (val1 === "" && val2 === "") {
        msg.innerHTML = "";
        return;
    }

    if (val1 === val2) {
        msg.innerHTML = "비밀번호가 일치합니다.";
        msg.style.color = "green";
    } else {
        msg.innerHTML = "비밀번호가 일치하지 않습니다.";
        msg.style.color = "red";
    }
}

// 비밀번호 토글 및 주소 API는 기존과 동일
function togglePasswordVisibility(inputId, element) {
    var input = document.getElementById(inputId);
    var icon = element.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

function execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function(data) {
            document.getElementById('zip_code').value = data.zonecode;
            document.getElementById('base_addr').value = data.address;
            document.getElementById('detail_addr').focus();
        }
    }).open();
}

function submitEditForm() {
    var p1 = document.getElementById('password').value;
    var p2 = document.getElementById('password_confirm').value;

    // 비밀번호 입력 시 일치 확인
    if (p1 || p2) {
        if (p1 !== p2) {
            alert("비밀번호가 일치하지 않습니다.");
            return;
        }
    }

    // 중복 확인 여부 체크
    if (!isNickValid) {
        alert("닉네임 중복 확인을 해주세요.");
        return;
    }
    if (!isEmailValid) {
        alert("이메일 중복 확인을 해주세요.");
        return;
    }

    // 모든 조건 만족 시 전송
    if (confirm("정말로 수정하시겠습니까?")) {
        var form = document.getElementById('edit-form');
        if (form) {
            form.submit();
        } else {
            alert("폼을 찾을 수 없습니다.");
        }
    }
}

// 실시간 비번 체크 함수도 ID 오류 안나게 확실히 수정
function checkPasswordMatch() {
    var p1 = document.getElementById('password');
    var p2 = document.getElementById('password_confirm');
    var msg = document.getElementById('pw_match_msg'); // HTML에 있는 span ID와 동일해야 함

    if (!p1 || !p2 || !msg) return;

    if (p1.value === "" && p2.value === "") {
        msg.innerHTML = "";
        return;
    }

    if (p1.value === p2.value) {
        msg.innerHTML = "비밀번호가 일치합니다.";
        msg.style.color = "green";
    } else {
        msg.innerHTML = "비밀번호가 일치하지 않습니다.";
        msg.style.color = "red";
    }
}