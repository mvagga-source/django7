const axios = require('axios');
// 파일 상단에 추가 (Node.js 기본 기능)
const queryFromUser = process.argv[2] || '맛집추천도서'; // 터미널 입력값이 없으면 '베스트셀러' 검색

// ▼▼▼ 여기에 본인의 키를 붙여넣으세요 ▼▼▼
const CLIENT_ID = 'C_MasXzr3nCzi13g19wN';
const CLIENT_SECRET = 'mUtwlSX2ES';
// ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

async function callNaverApi() {
    // 1. 요청할 주소 (책 검색)
    const url = 'https://openapi.naver.com/v1/search/book.json';

    try {
        // 2. API 요청 보내기 (네이버야, '자바스크립트' 책 정보 좀 줘!)
        const response = await axios.get(url, {
            params: {
                query: queryFromUser, // 검색어
                display: 8            // 3개만 보여줘
            },
            headers: {
                'X-Naver-Client-Id': CLIENT_ID,
                'X-Naver-Client-Secret': CLIENT_SECRET
            }
        });

        // 3. 받아온 데이터(JSON) 눈으로 확인하기
        console.log("=== API 호출 성공! 받아온 데이터는 아래와 같습니다 ===");
        console.log(response.data); 

    } catch (error) {
        // 에러가 났을 때
        console.error("=== 에러가 발생했습니다 ===");
        if(error.response) {
            console.error("에러 코드:", error.response.status); // 401이면 인증오류, 403이면 권한오류
            console.error("에러 내용:", error.response.data);
        } else {
            console.error(error.message);
        }
    }
}

callNaverApi();