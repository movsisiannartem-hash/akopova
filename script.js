/**
 * HELEN AKOPOVA MAKEUP ACADEMY — Client Interactions
 * Header, Hero Section, Lookbook & Enrollment Modal
 */

// -----------------------------------------------------------------------------
// 1. Toast Notification for In-Progress Sections
// -----------------------------------------------------------------------------
let toastTimeout = null;

function showInProgressToast(sectionName) {
  const toast = document.getElementById('in-progress-toast');
  const messageEl = document.getElementById('toast-message');
  
  if (!toast) return;

  if (messageEl && sectionName) {
    messageEl.textContent = `Раздел «${sectionName}» находится в разработке. Запишитесь на обучение прямо сейчас:`;
  }

  // Clear previous timer
  if (toastTimeout) {
    clearTimeout(toastTimeout);
  }

  toast.classList.add('show');
  toast.setAttribute('aria-hidden', 'false');

  // Auto-dismiss after 6 seconds
  toastTimeout = setTimeout(() => {
    closeInProgressToast();
  }, 6000);
}

function closeInProgressToast() {
  const toast = document.getElementById('in-progress-toast');
  if (toast) {
    toast.classList.remove('show');
    toast.setAttribute('aria-hidden', 'true');
  }
  if (toastTimeout) {
    clearTimeout(toastTimeout);
    toastTimeout = null;
  }
}

// Close toast on outside click
document.addEventListener('click', (e) => {
  const toast = document.getElementById('in-progress-toast');
  if (toast && toast.classList.contains('show')) {
    const toastCard = toast.querySelector('.toast-card');
    const isNavLink = e.target.closest('.nav-link') || e.target.closest('.mobile-nav-link');
    if (toastCard && !toastCard.contains(e.target) && !isNavLink) {
      closeInProgressToast();
    }
  }
});

// -----------------------------------------------------------------------------
// 2. Mobile Menu Toggle
// -----------------------------------------------------------------------------
function toggleMobileMenu() {
  const drawer = document.getElementById('mobile-drawer');
  const btn = document.getElementById('mobile-menu-btn');
  
  if (!drawer || !btn) return;

  const isOpen = drawer.classList.contains('open');
  if (isOpen) {
    drawer.classList.remove('open');
    btn.classList.remove('active');
    btn.setAttribute('aria-expanded', 'false');
    drawer.setAttribute('aria-hidden', 'true');
  } else {
    drawer.classList.add('open');
    btn.classList.add('active');
    btn.setAttribute('aria-expanded', 'true');
    drawer.setAttribute('aria-hidden', 'false');
  }
}

// -----------------------------------------------------------------------------
// 3. Enrollment Dialog Modal
// -----------------------------------------------------------------------------
function openEnrollmentModal() {
  const modal = document.getElementById('enroll-modal');
  if (modal) {
    if (typeof modal.showModal === 'function') {
      modal.showModal();
    } else {
      modal.setAttribute('open', '');
    }
    document.body.style.overflow = 'hidden';
  }
}

function openEnrollmentModalWithProgram(programKey) {
  const select = document.getElementById('client-program');
  if (select && programKey) {
    select.value = programKey;
  }
  closeLookbookModal();
  openEnrollmentModal();
}

function closeEnrollmentModal() {
  const modal = document.getElementById('enroll-modal');
  if (modal) {
    if (typeof modal.close === 'function') {
      modal.close();
    } else {
      modal.removeAttribute('open');
    }
    document.body.style.overflow = '';
  }
}

// Close modal on backdrop click
document.getElementById('enroll-modal')?.addEventListener('click', (e) => {
  const dialogCard = document.querySelector('.dialog-card');
  if (dialogCard && !dialogCard.contains(e.target)) {
    closeEnrollmentModal();
  }
});

// -----------------------------------------------------------------------------
// 4. Form Submit handler
// -----------------------------------------------------------------------------
function handleEnrollSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('client-name')?.value || '';
  const phone = document.getElementById('client-phone')?.value || '';
  const submitBtn = event.target.querySelector('button[type="submit"]');
  const originalText = submitBtn.innerHTML;

  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span>Заявка отправлена ✓</span>`;
  submitBtn.style.backgroundColor = '#16a34a';

  setTimeout(() => {
    alert(`Спасибо, ${name}! Ваша заявка на обучение в Helen Akopova Makeup Academy принята. Мы свяжемся с вами по номеру ${phone}.`);
    closeEnrollmentModal();
    event.target.reset();
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
    submitBtn.style.backgroundColor = '';
  }, 600);
}

// -----------------------------------------------------------------------------
// 5. Lookbook Modal & Interactive Carousel (Feature 5)
// -----------------------------------------------------------------------------
const lookbookData = [
  {
    counter: '01 / 04',
    title: 'Editorial Smoky Bronze',
    desc: 'Выпускная дипломная работа студента базового курса. Постановка чистой авторской растушёвки, многослойный градиент и естественное сияние бархатной кожи.',
    course: 'Базовый курс визажиста с нуля',
    programKey: 'basic'
  },
  {
    counter: '02 / 04',
    title: 'Glass Skin & Sculpted Cheeks',
    desc: 'Техника анатомической коррекции лица на курсе "Pro". Идеальная текстура сияющей кожи без эффекта маски, подчёркивающая природную красоту.',
    course: 'Повышение квалификации Pro',
    programKey: 'pro'
  },
  {
    counter: '03 / 04',
    title: 'Modern Hollywood Red',
    desc: 'Кутюрный вечерний образ: выверенная графичная стрелка, идеальная симметрия контура губ и стойкие матовые текстуры.',
    course: 'Макияж для себя',
    programKey: 'self'
  },
  {
    counter: '04 / 04',
    title: 'Soft Glam Bridal',
    desc: 'Коммерческий свадебный макияж. Ультрастойкость 24 часа, естественное свечение при студийном свете и на фотокамере.',
    course: 'Индивидуальный мастер-класс',
    programKey: 'consult'
  }
];

let currentLookIndex = 0;

function openLookbookModal() {
  const modal = document.getElementById('lookbook-modal');
  if (modal) {
    if (typeof modal.showModal === 'function') {
      modal.showModal();
    } else {
      modal.setAttribute('open', '');
    }
    document.body.style.overflow = 'hidden';
    updateLookbookView();
  }
}

function closeLookbookModal() {
  const modal = document.getElementById('lookbook-modal');
  if (modal) {
    if (typeof modal.close === 'function') {
      modal.close();
    } else {
      modal.removeAttribute('open');
    }
    document.body.style.overflow = '';
  }
}

function nextLookbookSlide() {
  currentLookIndex = (currentLookIndex + 1) % lookbookData.length;
  updateLookbookView();
}

function prevLookbookSlide() {
  currentLookIndex = (currentLookIndex - 1 + lookbookData.length) % lookbookData.length;
  updateLookbookView();
}

function goToLookbookSlide(index) {
  if (index >= 0 && index < lookbookData.length) {
    currentLookIndex = index;
    updateLookbookView();
  }
}

function updateLookbookView() {
  const data = lookbookData[currentLookIndex];
  if (!data) return;

  const counterEl = document.getElementById('lookbook-counter');
  const titleEl = document.getElementById('lookbook-title');
  const descEl = document.getElementById('lookbook-desc');
  const courseEl = document.getElementById('lookbook-meta-course');

  if (counterEl) counterEl.textContent = data.counter;
  if (titleEl) titleEl.textContent = data.title;
  if (descEl) descEl.textContent = data.desc;
  if (courseEl) courseEl.textContent = data.course;

  // Update dots
  const dots = document.querySelectorAll('#lookbook-dots .lookbook-dot');
  dots.forEach((dot, idx) => {
    dot.classList.toggle('active', idx === currentLookIndex);
  });

  // Update slide visuals
  for (let i = 0; i < lookbookData.length; i++) {
    const slide = document.getElementById(`look-slide-${i}`);
    if (slide) {
      slide.classList.toggle('active', i === currentLookIndex);
    }
  }
}

function enrollFromLookbook() {
  const data = lookbookData[currentLookIndex];
  closeLookbookModal();
  openEnrollmentModalWithProgram(data ? data.programKey : 'basic');
}

// Close lookbook on backdrop click
document.getElementById('lookbook-modal')?.addEventListener('click', (e) => {
  const card = document.querySelector('.lookbook-card');
  if (card && !card.contains(e.target)) {
    closeLookbookModal();
  }
});

// -----------------------------------------------------------------------------
// 6. Global Keyboard handler (Escape key)
// -----------------------------------------------------------------------------
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeEnrollmentModal();
    closeLookbookModal();
    closeInProgressToast();
    const drawer = document.getElementById('mobile-drawer');
    if (drawer?.classList.contains('open')) {
      toggleMobileMenu();
    }
  }
});
