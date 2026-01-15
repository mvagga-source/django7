function searchBtn(){
    searchFrm.submit();
}//searchBtn()

document.addEventListener('DOMContentLoaded', () => {
  const track = document.getElementById('promoTrack');
  if (!track) return;

  const slides = Array.from(track.querySelectorAll('.promo-slide'));
  const prevBtn = document.getElementById('promoPrev');
  const nextBtn = document.getElementById('promoNext');
  const dotsWrap = document.getElementById('promoDots');

  if (!slides.length || !prevBtn || !nextBtn || !dotsWrap) return;

  let index = 0;
  let timer = null;
  const AUTOPLAY_MS = 10000;

  const dots = slides.map((_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'promo-dot';
    b.setAttribute('role', 'tab');
    b.setAttribute('aria-label', `${i + 1}번 배너`);
    b.addEventListener('click', () => goTo(i, true));
    dotsWrap.appendChild(b);
    return b;
  });

  function render() {
    slides.forEach((s, i) => s.classList.toggle('is-active', i === index));
    dots.forEach((d, i) => d.classList.toggle('is-active', i === index));
  }

  function goTo(i, userAction = false) {
    index = (i + slides.length) % slides.length;
    render();
    if (userAction) restartAutoplay();
  }
  function next(userAction = false) { goTo(index + 1, userAction); }
  function prev(userAction = false) { goTo(index - 1, userAction); }

  function startAutoplay() {
    stopAutoplay();
    timer = setInterval(() => next(false), AUTOPLAY_MS);
  }
  function stopAutoplay() {
    if (timer) clearInterval(timer);
    timer = null;
  }
  function restartAutoplay() { startAutoplay(); }

  prevBtn.addEventListener('click', () => prev(true));
  nextBtn.addEventListener('click', () => next(true));

  let startX = 0;
  let dragging = false;
  const THRESHOLD = 40;

  function onDown(x) { dragging = true; startX = x; stopAutoplay(); }
  function onUp(x) {
    if (!dragging) return;
    dragging = false;
    const dx = x - startX;
    if (Math.abs(dx) >= THRESHOLD) dx < 0 ? next(true) : prev(true);
    else restartAutoplay();
  }

  track.addEventListener('touchstart', (e) => onDown(e.touches[0].clientX), { passive: true });
  track.addEventListener('touchend', (e) => onUp(e.changedTouches[0].clientX));
  track.addEventListener('mousedown', (e) => onDown(e.clientX));
  window.addEventListener('mouseup', (e) => onUp(e.clientX));

  render();
  startAutoplay();

  document.addEventListener('visibilitychange', () => {
    document.hidden ? stopAutoplay() : startAutoplay();
  });
});
