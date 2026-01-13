// 다음 주소 API 호출
function execDaumPostcode() {
    new daum.Postcode({
        oncomplete: function(data) {
            var addr = (data.userSelectedType === 'R') ? data.roadAddress : data.jibunAddress;
            $('#zip_code').val(data.zonecode);
            $('#base_addr').val(addr);
            $('#detail_addr').focus();
        }
    }).open();
}

$(document).ready(function() {
    // 유입 경로 '기타' 선택 시 입력창 노출
    $('#join_path').on('change', function() {
        if ($(this).val() === 'etc') {
            $('#join_path_etc').slideDown(200).focus();
        } else {
            $('#join_path_etc').slideUp(200).val('');
        }
    });

    // 최종 폼 제출 검사
    $('#join-form-final').on('submit', function() {
        if ($('#zip_code').val() === "") {
            alert("주소를 입력해 주세요.");
            return false;
        }
        if ($('input[name="food_cat"]:checked').length === 0) {
            alert("취향 정보를 하나 이상 선택해 주세요.");
            return false;
        }
        if ($('#join_path').val() === null) {
            alert("가입 경로를 선택해 주세요.");
            return false;
        }
        return true;
    });
});