// [다음 단계로] 버튼 클릭 시 체크 로직
$('#next-step-btn').click(function(e) { //아이디가 next-step-btn인 버튼을 클릭하는 순간, 중괄호{ } 안의 내용을 실행하고 이때 발생한 클릭 이벤트 정보를 e라는 이름으로 가져와라
    // 1. 필수 체크박스의 총 개수와 체크된 개수를 가져온다.
    var requiredTotal = $('.chk.required').length; //클래스에 chk와 required를 둘 다 가진 요소가 총 몇 개인지 세서 requiredTotal에 저장(필수 항목의 총 개수)
    var requiredChecked = $('.chk.required:checked').length; //필수 항목 중에서 현재 체크가 되어 있는 것만 골라서 개수를 셈

    // 2. 만약 필수 항목을 다 체크하지 않았다면
    if (requiredTotal !== requiredChecked) {
        e.preventDefault(); // 브라우저의 기본 동작을 한 번 더 확실히 막아줌
        alert('필수 약관에 모두 동의하셔야 다음 단계로 진행이 가능합니다.');
        return false; // 함수를 종료하여 아래의 이동 코드가 실행되지 않게 함
    }
    
    // 3. 모두 체크되었다면 여기서 페이지를 이동시킵니다.
    location.href = "{% url 'member:join2' %}";
});







// $('.chk').change(function() { //클래스가 chk인 체크박스의 상태가 변할 때(클릭할 때) 중괄호 안의 코드를 실행하라
//     var requiredTotal = $('.chk.required').length; //클래스에 chk와 required를 둘 다 가진 요소가 총 몇 개인지 세서 requiredTotal에 저장(필수 항목의 총 개수)
//     var requiredChecked = $('.chk.required:checked').length;//필수 항목 중에서 현재 체크가 되어 있는 것만 골라서 개수를 셈

//     if (requiredTotal === requiredChecked) {
//         $('#next-step-btn').removeClass('disabled').css('pointer-events', 'auto'); 
//     } else {
//         $('#next-step-btn').addClass('disabled').css('pointer-events', 'none');
//     }
// });

// // 버튼 클릭 시 체크박스 확인 로직 추가
// $('#next-step-btn').click(function(e) {
//     var requiredTotal = $('.chk.required').length;
//     var requiredChecked = $('.chk.required:checked').length;

//     if (requiredTotal !== requiredChecked) {
//         e.preventDefault(); // 중요! 다음 페이지로 넘어가는 걸 강제로 막음
//         alert('필수 약관에 모두 동의해주세요.');
//     }
// });