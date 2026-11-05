/* ===================== CUSTOM CURSOR ===================== */
const dot  = document.getElementById('cursor-dot');
const ring = document.getElementById('cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
(function animate() {
  rx += (mx - rx) * 0.18;
  ry += (my - ry) * 0.18;
  if (dot)  { dot.style.left  = mx + 'px'; dot.style.top  = my + 'px'; }
  if (ring) { ring.style.left = rx + 'px'; ring.style.top = ry + 'px'; }
  requestAnimationFrame(animate);
})();

/* ===================== MOBILE HAMBURGER ===================== */
const hamburger  = document.getElementById('hamburger');
const mobileNav  = document.getElementById('mobile-nav');
const mobileLinks = document.querySelectorAll('.mobile-link');

function toggleMobileMenu(forceClose) {
  const isOpen = mobileNav.classList.contains('open');
  if (forceClose || isOpen) {
    mobileNav.classList.remove('open');
    hamburger.children[0].style.transform = '';
    hamburger.children[1].style.opacity   = '';
    hamburger.children[2].style.transform = '';
  } else {
    mobileNav.classList.add('open');
    hamburger.children[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
    hamburger.children[1].style.opacity   = '0';
    hamburger.children[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
  }
}
if (hamburger) hamburger.addEventListener('click', () => toggleMobileMenu());
mobileLinks.forEach(link => link.addEventListener('click', () => toggleMobileMenu(true)));

/* ===================== SCROLL REVEAL ===================== */
const revealEls = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); } });
}, { threshold: 0.08, rootMargin: '0px 0px -60px 0px' });
revealEls.forEach(el => revealObs.observe(el));

/* ===================== STAT COUNTERS ===================== */
function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'));
  const start  = performance.now();
  const dur    = 2000;
  function tick(now) {
    const p = Math.min((now - start) / dur, 1);
    const ease = 1 - Math.pow(1 - p, 4);
    el.textContent = Math.floor(ease * target);
    if (p < 1) requestAnimationFrame(tick);
    else el.textContent = target;
  }
  requestAnimationFrame(tick);
}
const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('[data-target]').forEach(animateCounter);
      counterObs.unobserve(e.target);
    }
  });
}, { threshold: 0.4 });
document.querySelectorAll('.intro-stats').forEach(el => counterObs.observe(el));

/* ===================== SMOOTH ANCHOR SCROLL ===================== */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
      toggleMobileMenu(true);
    }
  });
});

/* ===================== CONTACT FORM ===================== */
const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('.submit-btn');
    const orig = btn.innerHTML;
    btn.innerHTML = '✓ Message Sent!';
    btn.style.background = '#3be2a1';
    setTimeout(() => {
      btn.innerHTML = orig;
      btn.style.background = '';
      form.reset();
    }, 3000);
  });
}

/* ===================== HERO SLIDE-UP (fallback) ===================== */
document.querySelectorAll('.hero-name span').forEach((span, i) => {
  span.style.animationDelay = (0.3 + i * 0.15) + 's';
});

/* ===================== PROJECT CARD TILT ===================== */
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width  - 0.5;
    const y = (e.clientY - rect.top)  / rect.height - 0.5;
    card.style.transform = `perspective(800px) rotateY(${x * 5}deg) rotateX(${-y * 5}deg) scale(1.01)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});

/* ===================== SECTION HEADER PARALLAX ===================== */
window.addEventListener('scroll', () => {
  const hero = document.getElementById('hero');
  if (hero) {
    const img = hero.querySelector('.hero-photo img');
    if (img) img.style.transform = `translateY(${window.scrollY * 0.25}px)`;
  }
});

/* ===================== CERTIFICATIONS FILTER ===================== */
const certFilters = document.querySelectorAll('.cert-filter');
const certCards = document.querySelectorAll('.cert-card');

certFilters.forEach(btn => {
  btn.addEventListener('click', () => {
    // Update active tab
    certFilters.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.getAttribute('data-filter');

    certCards.forEach(card => {
      if (filter === 'all' || card.getAttribute('data-issuer') === filter) {
        card.classList.remove('hidden');
        card.style.animation = 'certFadeIn 0.4s ease forwards';
      } else {
        card.classList.add('hidden');
        card.style.animation = '';
      }
    });
  });
});

// Add fadeIn animation
const certStyle = document.createElement('style');
certStyle.textContent = `
  @keyframes certFadeIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }
`;
document.head.appendChild(certStyle);



// ===== KOMIT AI AGENT MODAL =====
function openModal(id) {
  if (id === 'komit') {
    document.getElementById('komit-modal').classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(id) {
  if (id === 'komit') {
    document.getElementById('komit-modal').classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Close on overlay click
document.addEventListener('DOMContentLoaded', function () {
  const komitModal = document.getElementById('komit-modal');
  if (komitModal) {
    komitModal.addEventListener('click', function (e) {
      if (e.target === komitModal) closeModal('komit');
    });
  }
});

// Close on Escape key
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeModal('komit');
});
