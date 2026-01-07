/* 검색필터 팝업 */
function SearchFilterModal(id) {
    // Django URL name을 사용하여 서버로부터 HTML 조각을 가져옵니다.
    const url = "/pop/filPop/"; 
    
    $.ajax({
    url: url,
    type: 'GET',
    success: function(response) {
        // 성공 시, 빈 모달 껍데기 안에 서버가 보낸 HTML 내용을 채웁니다.
        $('#'+id).html(response);
        // 2. 바디에 클래스 추가해서 배경 어둡게 + 스크롤 방지
        $('body').addClass('modal-open');
        
        // 내용을 채운 후 모달을 띄웁니다.
        $('#'+id).show().addClass('show');
    },
    error: function(error) {
        console.error("모달 내용을 불러오는 데 실패했습니다.", error);
    }
    });
}