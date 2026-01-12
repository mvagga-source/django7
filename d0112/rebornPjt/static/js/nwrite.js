document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('inquiry-form');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // 간단한 유효성 검사
        const name = document.getElementById('user_name').value;
        const email = document.getElementById('user_email').value;

        if(!name || !email) {
            alert('필수 정보를 입력해주세요.');
            return;
        }

        // 실제 전송 전 연출 (버튼 비활성화)
        const submitBtn = form.querySelector('.btn-submit');
        submitBtn.innerText = '전송 중...';
        submitBtn.disabled = true;

        // AJAX 전송 로직이 들어갈 자리 (여기서는 시뮬레이션만)
        setTimeout(() => {
            alert('문의가 성공적으로 접수되었습니다.');
            window.location.href = '/'; // 홈으로 이동
        }, 1000);
    });
});