/* Focacceria — Dashboard JS */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initModals();
  initLangTabs();
  initSortable();
  initToasts();
  initImagePreview();
  initConfirmDelete();
});

// ── Theme ────────────────────────────────────────────────
function initTheme() {
  const saved = localStorage.getItem('db-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);

  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('db-theme', next);
      updateDbThemeIcon();
    });
  });
  updateDbThemeIcon();
}

function updateDbThemeIcon() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.querySelectorAll('[data-theme-icon]').forEach(el => {
    el.textContent = isDark ? '☀' : '🌙';
  });
}

// ── Sidebar ──────────────────────────────────────────────
function initSidebar() {
  const sidebar  = document.querySelector('.db-sidebar');
  const overlay  = document.querySelector('.sidebar-overlay');
  const toggles  = document.querySelectorAll('[data-sidebar-toggle]');

  if (!sidebar) return;

  function open()  { sidebar.classList.add('open'); overlay?.classList.add('open'); }
  function close() { sidebar.classList.remove('open'); overlay?.classList.remove('open'); }

  toggles.forEach(t => t.addEventListener('click', () => {
    sidebar.classList.contains('open') ? close() : open();
  }));
  overlay?.addEventListener('click', close);

  // Collapsible nav groups
  document.querySelectorAll('.nav-group-toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      const items = toggle.nextElementSibling;
      items?.classList.toggle('open');
    });
  });

  // Auto-open active group
  document.querySelectorAll('.nav-group-items .nav-link.active').forEach(link => {
    const items  = link.closest('.nav-group-items');
    const toggle = items?.previousElementSibling;
    items?.classList.add('open');
    toggle?.classList.add('open');
  });
}

// ── Modals ───────────────────────────────────────────────
function initModals() {
  document.querySelectorAll('[data-modal-open]').forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = document.querySelector(btn.dataset.modalOpen);
      modal?.classList.add('open');
    });
  });

  document.querySelectorAll('.modal-close, [data-modal-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.modal-backdrop')?.classList.remove('open');
    });
  });

  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', e => {
      if (e.target === backdrop) backdrop.classList.remove('open');
    });
  });

  // ESC key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.open').forEach(m => m.classList.remove('open'));
    }
  });
}

// ── Language Tabs ─────────────────────────────────────────
function initLangTabs() {
  document.querySelectorAll('.lang-tabs').forEach(tabs => {
    const buttons = tabs.querySelectorAll('.lang-tab-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        const container = tabs.closest('.lang-tab-group') || tabs.parentElement;

        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        container.querySelectorAll('.lang-tab-content').forEach(c => {
          c.classList.toggle('active', c.dataset.lang === lang);
        });
      });
    });
    // activate first
    buttons[0]?.click();
  });
}

// ── Sortable Drag & Drop ─────────────────────────────────
function initSortable() {
  document.querySelectorAll('[data-sortable]').forEach(list => {
    if (typeof Sortable === 'undefined') return;

    const url = list.dataset.reorderUrl;
    Sortable.create(list, {
      handle: '.drag-handle',
      animation: 150,
      ghostClass: 'sortable-ghost',
      dragClass: 'sortable-drag',
      onEnd() {
        if (!url) return;
        const items = [...list.querySelectorAll('[data-id]')].map((el, i) => ({
          id: el.dataset.id,
          order: i,
        }));
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrf(),
          },
          body: JSON.stringify(items),
        }).then(r => r.json()).then(() => showToast('რიგი შენახულია', 'success'));
      },
    });
  });
}

// ── Toast Notifications ──────────────────────────────────
function initToasts() {
  // Auto-dismiss Django messages
  document.querySelectorAll('.toast').forEach(toast => {
    setTimeout(() => toast.remove(), 4000);
  });
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  const icon = type === 'success' ? '✓' : '✕';
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// ── Image Preview ─────────────────────────────────────────
function initImagePreview() {
  document.querySelectorAll('.image-upload-area input[type="file"]').forEach(input => {
    input.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => {
        let preview = input.closest('.image-upload-area').querySelector('.image-preview');
        if (!preview) {
          preview = document.createElement('img');
          preview.className = 'image-preview';
          input.closest('.image-upload-area').prepend(preview);
        }
        preview.src = ev.target.result;
      };
      reader.readAsDataURL(file);
    });
  });
}

// ── Confirm Delete ────────────────────────────────────────
function initConfirmDelete() {
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', e => {
      const msg = el.dataset.confirm || 'დარწმუნებული ხართ?';
      if (!confirm(msg)) e.preventDefault();
    });
  });
}

// ── CSRF Helper ───────────────────────────────────────────
function getCsrf() {
  return document.cookie.split('; ')
    .find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}
