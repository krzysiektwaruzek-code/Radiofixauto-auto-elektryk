(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  /* ---------- Menu mobilne ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('menu');

  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Zamknij menu' : 'Otwórz menu');
    nav.classList.toggle('is-open', open);
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });
    window.matchMedia('(min-width: 721px)').addEventListener('change', function () { setMenu(false); });
  }

  /* ---------- Reveal on scroll ---------- */
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Rok w stopce ---------- */
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- Formularz kontaktowy ---------- */
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('form-status');

  function setStatus(msg, state) {
    status.textContent = msg;
    if (state) status.setAttribute('data-state', state); else status.removeAttribute('data-state');
  }

  function validate() {
    var valid = true;
    form.querySelectorAll('[required]').forEach(function (input) {
      var ok = input.type === 'checkbox' ? input.checked : input.value.trim() !== '';
      var field = input.closest('.field');
      var err = form.querySelector('.error[data-for="' + input.id + '"]');
      if (field) { if (ok) field.removeAttribute('data-invalid'); else field.setAttribute('data-invalid', ''); }
      if (err) err.hidden = ok;
      input.setAttribute('aria-invalid', String(!ok));
      if (err) input.setAttribute('aria-describedby', err.id || (err.id = input.id + '-err'));
      if (!ok) valid = false;
    });
    return valid;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    setStatus('', null);

    if (!validate()) {
      var firstBad = form.querySelector('[aria-invalid="true"]');
      if (firstBad) firstBad.focus();
      return;
    }
    if (form.elements.website && form.elements.website.value) return; // honeypot

    var endpoint = form.getAttribute('data-endpoint');
    if (!endpoint) {
      // Backend nie został jeszcze podłączony – nie udajemy wysłania wiadomości.
      setStatus('Formularz nie jest jeszcze aktywny. Skorzystaj proszę z mapy i danych kontaktowych na tej stronie.', 'error');
      return;
    }

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    setStatus('Wysyłanie…', null);

    fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        form.reset();
        setStatus('Dziękujemy, wiadomość została wysłana.', 'ok');
      })
      .catch(function () {
        setStatus('Nie udało się wysłać wiadomości. Spróbuj ponownie później.', 'error');
      })
      .then(function () { btn.disabled = false; });
  });

  form.addEventListener('input', function (e) {
    if (e.target.getAttribute('aria-invalid') === 'true') validate();
  });
})();
