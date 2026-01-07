document.addEventListener('DOMContentLoaded', () => {
    console.log("게시판 스크립트 로드 완료");
    
    // 검색 버튼 클릭 이벤트 예시
    const searchBtn = document.querySelector('.search-box button');
    searchBtn.addEventListener('click', () => {
        const query = document.querySelector('.search-box input').value;
        if(query) alert(`'${query}' 검색 결과로 이동합니다.`);
    });
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