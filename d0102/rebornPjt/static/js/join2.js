$(document).ready(function() {
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

        // --- [2단계] 비밀번호 조건 ------ 
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
        

        // --- [3단계] 비밀번호 일치 검사 ---
        // 조건 A: 특수문자가 없는가? (!는 '반대'라는 뜻)
        // 조건 B: 소문자+숫자 합이 9개 미만인가?
        if (pw !== pwCheck) {
            alert('비밀번호와 비밀번호 확인이 일치하지 않습니다.');
            $('#password-check').focus();
            return false; // 일치 안 하면 여기서 전체 중단
        }
        // --- [최종] 모든 검문소를 통과했을 때만 실행 ---
        // 위 검사들을 모두 통과했다면, HTML에서 만든 'join-form' 봉투를 서버로 보냄.
        $('#join-form').submit();
    });
});