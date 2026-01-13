document.addEventListener('DOMContentLoaded', () => {
    console.log("게시판 스크립트 로드 완료");
    
    // 1. 검색 버튼 에러 방지
    const searchBtn = document.querySelector('.search-box button');
    if (searchBtn) { // 요소가 존재할 때만 이벤트 리스너 등록
        searchBtn.addEventListener('click', function() {
            console.log('검색 실행');
        });
    }

    // 2. 글쓰기 버튼 등 다른 요소도 동일하게 처리
    const writeBtn = document.querySelector('.btn-write');
    if (writeBtn) {
        writeBtn.addEventListener('click', function() {
            location.href = '/board/write/';
        });
    }
});

function checkLoginAndWrite(isAuthenticated) {
    console.log("로그인 상태:", isAuthenticated);
    // isAuthenticated는 문자열 'true' 또는 'false'로 들어옵니다.
    if (isAuthenticated === 'true') {
        // 로그인 상태면 글쓰기 페이지로 이동
        location.href = '/board/bwrite/';
    } else {
        // 비로그인 상태면 컨펌창 출력
        const goToLogin = confirm("로그인이 필요한 서비스입니다. 로그인하시겠습니까?");
        
        if (goToLogin) {
            // '확인' 클릭 시 로그인 페이지로 이동 (실제 로그인 URL로 수정하세요)
            location.href = '/login/'; 
        }
    }
}