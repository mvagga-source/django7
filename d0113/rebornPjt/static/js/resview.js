document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("reviewModal");
    const openBtn = document.querySelector(".review-btn");
    const closeBtn = document.getElementById("closeModal");
    const submitBtn = document.getElementById("submitReview");

    const reviewText = document.getElementById("reviewText");
    const stars = document.querySelectorAll(".star-rating span");
    const grid = document.getElementById("reviewGrid");

    const imageInput = document.getElementById("reviewImages");
    const imagePreview = document.getElementById("imagePreview");

    let selectedRating = 0;
    let selectedImages = [];
    let editReviewId = null;
    let deletedImageIds = [];

    /* =========================
       후기 작성 버튼 클릭
    ========================= */
    openBtn.addEventListener("click", () => {
        // 로그인 여부는 서버에서 판단
        modal.classList.add("active");
    });

    /* =========================
       모달 닫기
    ========================= */
    closeBtn.addEventListener("click", () => {
        modal.classList.remove("active");
        resetReviewModal();
    });

    /* =========================
       별점 선택
    ========================= */
    stars.forEach(star => {
        star.addEventListener("click", () => {
            selectedRating = Number(star.dataset.value);
            stars.forEach(s =>
                s.classList.toggle(
                    "active",
                    Number(s.dataset.value) <= selectedRating
                )
            );
        });
    });
    
    /* =========================
        이미지 미리보기
    ========================= */
    imageInput.addEventListener("change", () => {

        // 새로 선택한 이미지들 배열에 추가
        [...imageInput.files].forEach(file => {
            if (!file.type.startsWith("image/")) return;
            selectedImages.push(file);
        });

        renderImagePreview();

        // 🔥 중요: input 초기화 (같은 파일 다시 선택 가능)
        imageInput.value = "";
    });

    function renderImagePreview() {
        imagePreview.innerHTML = "";

        selectedImages.forEach((file, index) => {

            const reader = new FileReader();
            reader.onload = e => {

                const wrapper = document.createElement("div");
                wrapper.className = "preview-item";

                const img = document.createElement("img");
                img.src = e.target.result;

                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "remove-btn";
                btn.innerText = "×";

                btn.addEventListener("click", () => {
                    selectedImages.splice(index, 1);
                    renderImagePreview();
                });

                wrapper.appendChild(img);
                wrapper.appendChild(btn);
                imagePreview.appendChild(wrapper);
            };

            reader.readAsDataURL(file);
        });
    }


    /* =========================
       submitBtn 분기
    ========================= */
    submitBtn.addEventListener("click", () => {

        if (editReviewId) {
            updateReview();
        } else {
            writeReview();
        }//submit 버튼 로직 분기
        return;
    });
    
    /* =========================
    후기 등록 (AJAX)
    ========================= */
    function writeReview() {
        const content = reviewText.value.trim();
        const restaurantId = document.getElementById("restaurantId").value;

        if (!selectedRating || !content) {
            alert("별점과 내용을 입력하세요.");
            return;
        }

        const formData = new FormData();
        formData.append("restaurant_id", restaurantId);
        formData.append("content", content);
        formData.append("rating", selectedRating);

        // ✅ 이미지 여러 장 추가
        selectedImages.forEach(img => {
            formData.append("images", img);
        });

        fetch("/review/write/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
                // ❗ Content-Type 지정 ❌ (FormData 자동 처리)
            },
            body: formData
        })
        .then(res => {
            if (res.status === 401) {
                alert("로그인이 필요합니다.");
                location.href = "/member/login/";
                return;
            }
            return res.json();
        })
        .then(data => {
            if (!data) return;

            if (data.result === "success") {
                prependReview(data.review);
                updateReviewStats(data.stats);
                resetReviewModal();
                modal.classList.remove("active");
            } else {
                alert("후기 등록 실패");
            }
        });
    };


    /* =========================
       등록 후 모달 초기화 함수
    ========================= */
    function resetReviewModal() {
        reviewText.value = "";
        selectedRating = 0;
        stars.forEach(s => s.classList.remove("active"));

        selectedImages = [];
        deletedImageIds = [];
        editReviewId = null;

        imagePreview.innerHTML = ""; // 미리보기 제거
    }

    /* =========================
       리뷰 상단 추가 함수
    ========================= */
    function prependReview(r) {

        const imagesHTML = r.images.length
        ? `<div class="review-images">
            ${r.images.map(img => `<img src="${img}">`).join("")}
           </div>`
        : "";

        const card = document.createElement("div");
        card.className = "review-card";
        card.dataset.reviewId = r.id;

        card.innerHTML = `
            <div class="review-header">
                <span class="user-id">${r.user}</span>
                <span class="rating">${"⭐".repeat(r.rating)}</span>
            </div>
            <p class="review-content">${r.content}</p>
            ${imagesHTML}
            <div class="review-date">${r.date}</div>
        `;

        grid.prepend(card);
    }

    /* =========================
       통계 갱신 함수
    ========================= */
    function updateReviewStats(stats) {
        document.getElementById("avgRating").innerText = stats.avg_rating;
        document.getElementById("reviewCount").innerText = stats.review_count;
    }

    /* =========================
        삭제 버튼 클릭
    ========================= */
    document.addEventListener("click", e => {
    
        if (!e.target.classList.contains("delete-review-btn")) return;
    
        if (!confirm("후기를 삭제하시겠습니까?")) return;
    
        const card = e.target.closest(".review-card");
        const reviewId = card.dataset.reviewId;
    
        const formData = new FormData();
        formData.append("review_id", reviewId);
    
        fetch("/review/delete/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.result === "success") {
                card.remove();
                updateReviewStats(data.stats);
            } else {
                alert("삭제 실패");
            }
        });
    });

    /* =========================
        수정 버튼 클릭
    ========================= */
    document.addEventListener("click", e => {

        if (!e.target.classList.contains("edit-review-btn")) return;

        const card = e.target.closest(".review-card");

        editReviewId = card.dataset.reviewId;
        deletedImageIds = [];

        selectedImages = [];           // 새 이미지 배열 초기화
        imageInput.value = "";         // 파일 input도 초기화

        // 내용
        reviewText.value =
            card.querySelector(".review-content").innerText;

        // 별점
        selectedRating =
            card.querySelector(".rating").innerText.length;
        stars.forEach(s =>
            s.classList.toggle(
                "active",
                Number(s.dataset.value) <= selectedRating
            )
        );

        // 기존 이미지 미리보기 구성
        imagePreview.innerHTML = "";
        card.querySelectorAll(".existing-image").forEach(imgDiv => {
            const clone = imgDiv.cloneNode(true);
            imagePreview.appendChild(clone);
        });

        modal.classList.add("active");
    });

    /* ===================================
        이미지 “X” 클릭 → 삭제 목록에 추가
    ==================================== */
    document.addEventListener("click", e => {

        if (!e.target.classList.contains("remove-existing-img")) return;

        const wrapper = e.target.closest(".existing-image");
        const imageId = wrapper.dataset.imageId;

        deletedImageIds.push(imageId);
        wrapper.remove();
    });

    /* =========================
        수정 함수
    ========================= */    
    function updateReview() {

        const formData = new FormData();

        formData.append("review_id", editReviewId);
        formData.append("content", reviewText.value.trim());
        formData.append("rating", selectedRating);

        // 🔥 삭제할 기존 이미지 id
        deletedImageIds.forEach(id => {
            formData.append("deleted_images", id);
        });

        // 🔥 새 이미지
        selectedImages.forEach(img => {
            formData.append("images", img);
        });

        fetch("/review/update/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.result === "success") {
                location.reload(); // ← 수정은 새로고침이 UX상 자연스러움
            } else {
                alert("수정 실패");
            }
        });
    }

    // =========================
    // 리뷰 정렬
    // =========================
    document.querySelectorAll(".sort-btn").forEach(btn => {

        btn.addEventListener("click", () => {

            // 버튼 active 토글
            document.querySelectorAll(".sort-btn")
                .forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const sortType = btn.dataset.sort;
            const resno = document.getElementById("restaurantId").value;

            fetch(`/review/list/?resno=${resno}&sort=${sortType}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById("reviewGrid").innerHTML = data.html;
            });
        });

    });
});//DOMContentLoaded

    

/* =========================
   CSRF 쿠키
========================= */
function getCookie(name) {
    let cookieValue = null;
    document.cookie.split(";").forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(
                cookie.substring(name.length + 1)
            );
        }
    });
    return cookieValue;
}
