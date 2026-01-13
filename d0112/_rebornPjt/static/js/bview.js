/**
 * 게시판 상세보기 통합 스크립트 (확대/축소 + 토글 + 파일명)
 */

// --- 1. 게시글 및 댓글 토글 기능 ---

// 본문 수정창 토글
function togglePostEdit() {
    const display = document.getElementById('post-display');
    const form = document.getElementById('post-edit-form');
    if (display && form) {
        const isHidden = display.style.display === 'none';
        display.style.display = isHidden ? 'block' : 'none';
        form.style.display = isHidden ? 'none' : 'block';
    }
}

// 댓글/답글 수정창 토글
function toggleEdit(id) {
    if (!isUserLoggedIn) return; // 비로그인 차단
    
    const content = document.getElementById(`content-${id}`);
    const form = document.getElementById(`edit-form-${id}`);
    if (content && form) {
        const isHidden = form.style.display === 'none' || form.style.display === '';
        form.style.display = isHidden ? 'block' : 'none';
        content.style.display = isHidden ? 'none' : 'block';
    }
}

// 답글 입력창 토글
function toggleReply(id) {
    // 1. 로그인 체크
    if (!isUserLoggedIn) {
        if (confirm("로그인이 필요한 서비스입니다. 로그인 페이지로 이동하시겠습니까?")) {
            location.href = "{% url 'member:login' %}"; // 프로젝트의 로그인 URL로 변경
        }
        return;
    }

    // 2. 로그인된 경우 기존 로직 실행
    const form = document.getElementById(`reply-form-${id}`);
    if (form) {
        form.style.display = (form.style.display === 'none' || form.style.display === '') ? 'block' : 'none';
    }
}

// 파일명 표시 업데이트 (게시글 수정, 댓글, 답글 공통 사용)
function updateFileName(input, targetId) {
    const fileName = input.files.length > 0 
        ? (input.files.length > 1 ? `${input.files[0].name} 외 ${input.files.length - 1}개` : input.files[0].name)
        : "선택된 파일 없음";
    const target = document.getElementById(targetId);
    if (target) target.textContent = fileName;
}

// --- 2. 이미지 확대/축소 로직 ---

const zoomState = {
    scale: 1,
    panX: 0,
    panY: 0,
    start: { x: 0, y: 0 },
    isPanning: false
};

function applyTransform() {
    const img = document.getElementById("fullImage");
    if (img) {
        img.style.transform = `translate(${zoomState.panX}px, ${zoomState.panY}px) scale(${zoomState.scale})`;
    }
}

function zoomImage(imgSrc) {
    const modal = document.getElementById("imageModal");
    const img = document.getElementById("fullImage");
    
    zoomState.scale = 1;
    zoomState.panX = 0;
    zoomState.panY = 0;
    
    img.src = imgSrc;
    applyTransform();
    
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
}

function closeModal() {
    document.getElementById("imageModal").style.display = "none";
    document.body.style.overflow = "auto";
}

// 이벤트 바인딩
window.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.getElementById('modalWrapper');
    if (!wrapper) return;

    wrapper.addEventListener('wheel', (e) => {
        e.preventDefault();
        const delta = -e.deltaY;
        const factor = 0.2;
        if (delta > 0) zoomState.scale *= (1 + factor);
        else zoomState.scale /= (1 + factor);
        zoomState.scale = Math.min(Math.max(1, zoomState.scale), 10);
        applyTransform();
    }, { passive: false });

    wrapper.addEventListener('mousedown', (e) => {
        if (zoomState.scale <= 1) return;
        zoomState.isPanning = true;
        zoomState.start = { x: e.clientX - zoomState.panX, y: e.clientY - zoomState.panY };
        wrapper.style.cursor = 'grabbing';
    });

    window.addEventListener('mousemove', (e) => {
        if (!zoomState.isPanning) return;
        zoomState.panX = e.clientX - zoomState.start.x;
        zoomState.panY = e.clientY - zoomState.start.y;
        applyTransform();
    });

    window.addEventListener('mouseup', () => {
        zoomState.isPanning = false;
        if (wrapper) wrapper.style.cursor = 'grab';
    });
});