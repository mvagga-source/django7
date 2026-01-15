$(document).ready(function() {
    // [준비물] 중복 확인 버튼을 눌러서 '통과'했는지 기억해둘 도장판 (처음엔 모두 미통과: false)
    // 중복 확인 통과 여부를 저장하는 변수 (기본값 false)
    var isIdChecked = false;    // 아이디 통과 여부
    var isNickChecked = false;  // 닉네임 통과 여부
    var isEmailChecked = false; // 이메일 통과 여부

    // 사용자가 값을 수정하면 '중복 확인 다시 하기'를 유도하기 위해 체크 변수 초기화

    // [실시간 감시] 중복 확인을 받았더라도 글자를 한 글자라도 바꾸면 다시 '미통과'로 되돌림
    // 아이디 칸에 글자를 입력(input)하면 실행되는 함수
    $('input[name="mem_id"]').on('input', function() { 
        isIdChecked = false; // 도장을 지움
        $(this).removeClass('is-valid is-invalid'); // 칸의 초록색/빨간색 테두리 효과를 제거
        $('#mem_id_msg').hide();  // "사용 가능합니다" 같은 안내 문구를 숨김
    });
    // 닉네임 칸 실시간 감시
    $('input[name="nick_nm"]').on('input', function() { 
        isNickChecked = false; // 도장을 지움
        $(this).removeClass('is-valid is-invalid'); // 칸의 초록색/빨간색 테두리 효과를 제거
        $('#nick_nm_msg').hide(); // "사용 가능합니다" 같은 안내 문구를 숨김
    });
    // 이메일 칸 실시간 감시
    $('input[name="email"]').on('input', function() { 
        isEmailChecked = false; // 도장을 지움
        $(this).removeClass('is-valid is-invalid'); // 칸의 초록색/빨간색 테두리 효과를 제거
        $('#email_msg').hide(); // "사용 가능합니다" 같은 안내 문구를 숨김
    });

    // --- [중복 확인 실행 함수] ---
    // HTML 버튼의 onclick="checkDuplicate('...')"에서 호출됨
    // HTML의 중복 확인 버튼을 클릭하면 호출되는 진짜 기능
    window.checkDuplicate = function(fieldType) { // fieldType은 'mem_id'나 'nick_nm'처럼 어떤 칸을 검사할지 알려주는 이름표
        const inputField = $(`input[name="${fieldType}"]`); // 검사할 그 입력칸 찾기
        const msgLabel = $(`#${fieldType}_msg`); // 메시지를 보여줄 글자 칸 찾기
        const val = inputField.val().trim(); // 입력한 글자에서 앞뒤 공백을 제거하고 가져오기

        // (예외 처리) 글자를 아예 안 적고 버튼만 눌렀을 때
        if (!val) {
            alert(inputField.attr('placeholder') + " 항목을 입력해 주세요."); // 경고창 띄우기
            inputField.focus(); // 그 칸으로 마우스 커서 보내기
            return; // 함수를 여기서 끝냄 (더 이상 아래 코드를 실행 안 함)
        }
        // [서버와 통신 시작] Ajax를 이용해 장고(Django)에게 물어봄
        $.ajax({
            url: "../check_duplicate/", // 서버의 중복 체크 URL / 장고 views.py의 check_duplicate 함수 주소
            type: "GET", // 데이터를 가져오는 방식
            data: { 'type': fieldType, 'value': val },// "아이디 검사할 건데 값은 이거야"라고 전달
            success: function(res) { // 장고가 대답을 무사히 보내줬을 때 (res에 대답이 담김)
                if (res.is_available) { // 장고가 "중복 아니야(True)"라고 대답했다면
                    // [사용 가능]
                    // 1. 칸 테두리를 초록색(is-valid)으로 바꿈
                    inputField.addClass("is-valid").removeClass("is-invalid");
                    // 2. "사용 가능한 ~입니다" 메시지를 초록색으로 띄움
                    msgLabel.text("사용 가능한 " + getFieldName(fieldType) + "입니다.")
                            .addClass("success").removeClass("error").fadeIn();
                    // 3. 도장판에 '통과' 도장을 찍음
                    if(fieldType === 'mem_id') isIdChecked = true;
                    if(fieldType === 'nick_nm') isNickChecked = true;
                    if(fieldType === 'email') isEmailChecked = true;

                } else { // 장고가 "이미 누가 쓰고 있어(False)"라고 대답했다면
                    // [중복됨]
                    // 1. 칸 테두리를 빨간색(is-invalid)으로 바꿈
                    inputField.addClass("is-invalid").removeClass("is-valid");
                    // 2. "이미 사용 중인 ~입니다" 메시지를 빨간색으로 띄움
                    msgLabel.text("이미 사용 중인 " + getFieldName(fieldType) + "입니다.")
                            .addClass("error").removeClass("success").fadeIn();
                    // 3. 통과 못 했으니 도장판을 다시 미통과(false)로 설정
                    if(fieldType === 'mem_id') isIdChecked = false;
                    if(fieldType === 'nick_nm') isNickChecked = false;
                    if(fieldType === 'email') isEmailChecked = false;
                }
            },
            error: function() { // 서버가 죽었거나 주소가 틀려서 대화가 안 될 때
                alert("통신 오류가 발생했습니다.");
            }
        });
    };
    // 영어로 된 이름표를 한국어로 바꿔주는 보조 기능 (예: mem_id -> 아이디)
    function getFieldName(type) {
        if(type === 'mem_id') return '아이디';
        if(type === 'nick_nm') return '닉네임';
        return '이메일';
    }


    // --- [다음 단계 버튼 클릭 시 최종 검사] ---
    // '다음 단계' 버튼을 클릭하면 위에서 했던 검사들을 최종적으로 확인함
    $('#next-step-btn').click(function() { // '다음 단계' 버튼을 클릭했을 때 이 안의 내용들이 실행
        // --- [1단계] 빈칸 검사 ---
        // 1. 모든 입력창(.input-field)을 하나씩 검사하기
        var isEmpty = false; // 빈칸이 있는지 체크할 변수
        var targetName = ""; // 빈칸인 항목의 이름을 담을 변수

        // 모든 입력창(.input-field)을 하나씩 돌아가며 확인
        $('.input-field').each(function() { //클래스가 input-field인 모든 요소를 하나씩 순례하며 검사
            if ($(this).val().trim() === "") { // 만약 현재 확인 중인 칸의 값이 빈칸이라면
                isEmpty = true;// 빈칸이 있다고 표시
                targetName = $(this).attr('placeholder'); // 사용자가 뭘 안 적었는지 알려주기 위해, 그 칸에 써있던 **가이드 문구(예: "이메일")**를 가져옴
                $(this).focus(); // 경고창을 확인한 후 사용자가 바로 입력할 수 있게 해당 칸으로 마우스 커서
                return false; // 하나라도 비었으면, 빈칸을 찾으면 반복문(each)을 멈춤
            }
        });

        // 빈칸이 발견되었다면 경고창을 띄우고 전송을 중단
        if (isEmpty) {
            alert(targetName + ' 항목을 입력해 주세요.');
            return false; // 빈칸이 있으면 여기서 전체 중단
        }


        // --- [2단계] 중복 확인 도장판 확인 ---
        // 아이디 중복 확인 도장이 안 찍혀 있다면
        if (!isIdChecked) {
            alert('아이디 중복 확인이 필요합니다.');
            $('input[name="mem_id"]').focus();
            return false; // 다음 단계로 못 가게 막음
        }
        // 닉네임 중복 확인 도장이 안 찍혀 있다면
        if (!isNickChecked) {
            alert('닉네임 중복 확인이 필요합니다.');
            $('input[name="nick_nm"]').focus();
            return false;
        }
        // 이메일 중복 확인 도장이 안 찍혀 있다면
        if (!isEmailChecked) {
            alert('이메일 중복 확인이 필요합니다.');
            $('input[name="email"]').focus();
            return false;
        }

        // --- [3단계] 비밀번호 복잡성 검사 ---
        // 1. 입력한 값들 가져오기
        var pw = $('#password').val(); // 입력한 비밀번호 값
        var pwCheck = $('#password-check').val(); // 확인용 비밀번호 값
        
        // 2. 정규표현식 (검사 규칙)
        // 특수문자가 하나라도 있는지 검사
        var specialRegex = /[!@#$%^&*(),.?":{}|<>]/;
        // 소문자와 숫자만 골라내기
        var alphaNumMatch = pw.match(/[a-z0-9]/g); 
        // 골라낸 소문자+숫자의 개수 (없으면 0)
        var alphaNumCount = alphaNumMatch ? alphaNumMatch.length : 0;

        // 규칙 검사 실행!
        if (!specialRegex.test(pw) || alphaNumCount < 9) {
            alert('비밀번호 조건을 확인해 주세요.\n(특수문자 1개 이상, 소문자+숫자 조합 9자 이상)');
            $('#password').focus();
            return false; // 규칙에 안 맞으면 여기서 중단!
        }
        

        // --- [4단계] 비밀번호 재확인 검사 ---
        // 비밀번호와 비밀번호 확인 칸에 적힌 글자가 서로 다르면
        // 조건 A: 특수문자가 없는가? (!는 '반대'라는 뜻)
        // 조건 B: 소문자+숫자 합이 9개 미만인가?
        if (pw !== pwCheck) {
            alert('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
            $('#password-check').focus();
            return false; // 일치 안 하면 여기서 전체 중단
        }
        // --- [최종] 모든 검문소를 통과했을 때만 실행 ---
        // 위 검사들을 모두 통과했다면, HTML에서 만든 'join-form' 봉투를 서버(Django)로 전송
        $('#join-form').submit();
    });
});