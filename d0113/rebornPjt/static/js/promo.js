document.addEventListener("DOMContentLoaded", () => {
  const listEl = document.getElementById("promoRegistered");
  const form = document.getElementById("promoForm");

  const promoIdEl = document.getElementById("promoId");
  const resnoEl = document.getElementById("promoResno");
  const kickerEl = document.getElementById("promoKicker");
  const titleEl = document.getElementById("promoTitle");
  const subEl = document.getElementById("promoSub");
  const ctaTextEl = document.getElementById("promoCtaText");
  const previewImgEl = document.getElementById("promoPreviewImg");
  const ctaLinkEl = document.getElementById("promoCtaLink");

  const resetBtn = document.getElementById("promoResetBtn");
  const deleteBtn = document.getElementById("promoDeleteBtn");

  const API_LIST = "/promo/api/list/";
  const API_SAVE = "/promo/api/save/";
  const API_DELETE = (id) => `/promo/api/delete/${id}/`;

  // --- CSRF
  function getCookie(name) {
    const v = document.cookie.split("; ").find((row) => row.startsWith(name + "="));
    return v ? decodeURIComponent(v.split("=")[1]) : "";
  }
  const csrftoken = getCookie("csrftoken");

  function setPreviewFromSelect() {
    const opt = resnoEl.options[resnoEl.selectedIndex];
    const img = opt?.dataset?.img || "/static/images/common/noimage.png";
    previewImgEl.src = img;

    const resno = resnoEl.value;
    ctaLinkEl.href = resno ? `/restaurants/resview/${resno}/` : "#";
  }

  function setFormMode(isEdit) {
    deleteBtn.disabled = !isEdit;
  }

  function resetForm() {
    promoIdEl.value = "";
    resnoEl.value = "";
    kickerEl.value = "";
    titleEl.value = "";
    subEl.value = "";
    ctaTextEl.value = "";
    previewImgEl.src = "/static/images/common/noimage.png";
    ctaLinkEl.href = "#";
    setFormMode(false);
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function renderList(promos) {
    if (!promos.length) {
      listEl.innerHTML = `<li class="promo-empty">등록된 프로모션이 없습니다.</li>`;
      return;
    }

    listEl.innerHTML = promos.map(p => `
      <li class="promo-item"
          data-promo-id="${p.promo_id}"
          data-resno="${p.resno}"
          data-kicker="${escapeHtml(p.kicker || "")}"
          data-title="${escapeHtml(p.title || "")}"
          data-sub="${escapeHtml(p.sub || "")}"
          data-cta="${escapeHtml(p.cta_text || "")}"
          data-img="${p.img}"
          data-link="${p.link}">
        <div class="promo-item__thumb">
          <img src="${p.img}" alt="">
        </div>
        <div class="promo-item__meta">
          <div class="promo-item__name">${escapeHtml(p.res_name)}</div>
          <div class="promo-item__desc">${escapeHtml(p.title || "")}</div>
        </div>
        <button type="button" class="promo-del-mini" data-del="${p.promo_id}" aria-label="삭제">🗑️</button>
      </li>
    `).join("");
  }

  async function loadList() {
    const res = await fetch(API_LIST, { credentials: "same-origin" });
    const json = await res.json();
    if (!json.ok) throw new Error("list failed");
    renderList(json.promos);
  }

  async function savePromo() {
    const fd = new FormData();
    fd.append("promo_id", promoIdEl.value.trim());
    fd.append("resno", resnoEl.value);
    fd.append("kicker", kickerEl.value);
    fd.append("title", titleEl.value);
    fd.append("sub", subEl.value);
    fd.append("cta_text", ctaTextEl.value);

    const res = await fetch(API_SAVE, {
      method: "POST",
      body: fd,
      credentials: "same-origin",
      headers: { "X-CSRFToken": csrftoken },
    });
    const json = await res.json();
    if (!json.ok) throw new Error("save failed");

    await loadList();
    promoIdEl.value = json.promo_id;  // 저장 후 수정모드 유지
    setFormMode(true);
    alert("저장 완료!");
  }

  async function deletePromo(promoId) {
    const res = await fetch(API_DELETE(promoId), {
      method: "POST",
      credentials: "same-origin",
      headers: { "X-CSRFToken": csrftoken },
    });
    const json = await res.json();
    if (!json.ok) throw new Error("delete failed");

    await loadList();
    resetForm();
    alert("삭제 완료!");
  }

  // --- 이벤트
  resnoEl.addEventListener("change", setPreviewFromSelect);

  // 목록 클릭(수정모드) + 목록의 삭제(휴지통)
  listEl.addEventListener("click", (e) => {
    const delId = e.target?.dataset?.del;
    if (delId) {
      if (confirm("이 프로모션을 삭제할까요?")) {
        deletePromo(delId).catch((err) => {
          console.error(err);
          alert("삭제 실패(콘솔 확인)");
        });
      }
      return;
    }

    const item = e.target.closest(".promo-item");
    if (!item) return;

    promoIdEl.value = item.dataset.promoId || "";
    resnoEl.value = item.dataset.resno || "";
    kickerEl.value = item.dataset.kicker || "";
    titleEl.value = item.dataset.title || "";
    subEl.value = item.dataset.sub || "";
    ctaTextEl.value = item.dataset.cta || "";

    previewImgEl.src = item.dataset.img || "/static/images/common/noimage.png";
    ctaLinkEl.href = item.dataset.link || "#";

    setFormMode(true);
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    savePromo().catch((err) => {
      console.error(err);
      alert("저장 실패(콘솔 확인)");
    });
  });

  // 폼의 삭제 버튼
  deleteBtn.addEventListener("click", () => {
    const id = promoIdEl.value.trim();
    if (!id) return;
    if (confirm("현재 선택된 프로모션을 삭제할까요?")) {
      deletePromo(id).catch((err) => {
        console.error(err);
        alert("삭제 실패(콘솔 확인)");
      });
    }
  });

  resetBtn.addEventListener("click", resetForm);

  // 초기
  resetForm();
  setPreviewFromSelect();
  loadList().catch((err) => {
    console.error(err);
    listEl.innerHTML = `<li class="promo-empty">목록을 불러오지 못했습니다(콘솔 확인)</li>`;
  });
});
