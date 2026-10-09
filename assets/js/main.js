// Skrypty strony. Po zmianie uruchom: python _narzedzia/buduj.py (odświeża ?v= w HTML).
(() => {
  'use strict';

  // Tarcza w tle hero: znaczniki skali
  const ticks = document.querySelector('.dial__ticks');
  if (ticks) {
    let html = '';
    for (let i = 0; i < 60; i++) {
      const a = (i / 60) * Math.PI * 2;
      const r1 = 290, r2 = i % 5 === 0 ? 268 : 280;
      html += `<line x1="${300 + Math.cos(a) * r1}" y1="${300 + Math.sin(a) * r1}" x2="${300 + Math.cos(a) * r2}" y2="${300 + Math.sin(a) * r2}"/>`;
    }
    ticks.innerHTML = html;
  }


  // Menu mobilne
  const burger = document.querySelector('.burger');
  const menu = document.getElementById('menu');
  if (burger && menu) {
    const ustaw = (otwarte) => {
      burger.setAttribute('aria-expanded', otwarte ? 'true' : 'false');
      burger.setAttribute('aria-label', otwarte ? 'Zamknij menu' : 'Otwórz menu');
      menu.classList.toggle('is-open', otwarte);
    };
    burger.addEventListener('click', () => ustaw(burger.getAttribute('aria-expanded') !== 'true'));
    menu.addEventListener('click', (ev) => { if (ev.target.closest('a')) ustaw(false); });
    document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape') ustaw(false); });
  }

  // Lightbox zdjęć
  const lb = document.getElementById('lightbox');
  const linki = [...document.querySelectorAll('[data-lightbox]')];
  if (lb && linki.length && typeof lb.showModal === 'function') {
    const img = lb.querySelector('img');
    let idx = 0;
    const pokaz = (i) => {
      idx = (i + linki.length) % linki.length;
      img.src = linki[idx].getAttribute('href');
      img.alt = linki[idx].querySelector('img').alt;
    };
    linki.forEach((a, i) => a.addEventListener('click', (ev) => {
      ev.preventDefault();
      pokaz(i);
      lb.showModal();
    }));
    lb.querySelector('.lightbox__x').addEventListener('click', () => lb.close());
    lb.querySelector('.lightbox__n--p').addEventListener('click', () => pokaz(idx - 1));
    lb.querySelector('.lightbox__n--n').addEventListener('click', () => pokaz(idx + 1));
    lb.addEventListener('click', (ev) => { if (ev.target === lb) lb.close(); });
    lb.addEventListener('keydown', (ev) => {
      if (ev.key === 'ArrowLeft') pokaz(idx - 1);
      if (ev.key === 'ArrowRight') pokaz(idx + 1);
    });
  }

  const rok = document.getElementById('rok');
  if (rok) rok.textContent = new Date().getFullYear();

  // Pojawianie się sekcji przy przewijaniu
  const rev = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver((wpisy) => {
      wpisy.forEach((w) => { if (w.isIntersecting) { w.target.classList.add('is-in'); io.unobserve(w.target); } });
    }, { threshold: 0.12 });
    rev.forEach((el) => io.observe(el));
  } else {
    rev.forEach((el) => el.classList.add('is-in'));
  }

  // Status otwarcia: godziny z dane.json (blok #godziny-dane, czas polski). Bez godzin status się nie pokazuje.
  const status = document.getElementById('status');
  const godz = document.getElementById('godziny-dane');
  if (status && godz) {
    let okna = [];
    try { okna = JSON.parse(godz.textContent); } catch (_) { okna = []; }
    if (okna.length) {
      const dzien = ['niedz.', 'pon.', 'wt.', 'śr.', 'czw.', 'pt.', 'sob.'];
      const minuty = (t) => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };
      const teraz = new Date(new Date().toLocaleString('en-US', { timeZone: 'Europe/Warsaw' }));
      const d = teraz.getDay();
      const min = teraz.getHours() * 60 + teraz.getMinutes();
      const dzis = okna.find((o) => o.d.includes(d) && min >= minuty(o.od) && min < minuty(o.do));
      let tekst;
      if (dzis) {
        tekst = `Teraz otwarte · do ${dzis.do}`;
      } else {
        tekst = 'Teraz zamknięte';
        for (let przes = 0; przes <= 7; przes++) {
          const dt = (d + przes) % 7;
          const kandydaci = okna.filter((o) => o.d.includes(dt) && (przes > 0 || minuty(o.od) > min))
            .sort((x, y) => minuty(x.od) - minuty(y.od));
          if (kandydaci.length) {
            const kiedy = przes === 0 ? 'dziś' : przes === 1 ? 'jutro' : dzien[dt];
            tekst += ` · otwarcie ${kiedy} o ${kandydaci[0].od}`;
            break;
          }
        }
      }
      document.getElementById('status-tekst').textContent = tekst;
      status.classList.toggle('is-open', Boolean(dzis));
      status.hidden = false;
    }
  }

  // Formularz: walidacja w przeglądarce; wysyłka dopiero po wpisaniu endpointu w dane.json (formularz.endpoint)
  const form = document.getElementById('formularz');
  if (form) {
    const msg = document.getElementById('form-msg');
    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      let ok = true;
      form.querySelectorAll('[required]').forEach((el) => {
        const zle = el.type === 'checkbox' ? !el.checked : !el.value.trim();
        el.closest('.pole').classList.toggle('is-invalid', zle);
        el.setAttribute('aria-invalid', zle ? 'true' : 'false');
        if (zle) ok = false;
      });
      msg.classList.remove('is-err');
      if (!ok) { msg.textContent = 'Uzupełnij wszystkie pola i zaznacz zgodę.'; msg.classList.add('is-err'); return; }
      const cel = form.getAttribute('action');
      const tel = form.dataset.tel;
      const zapas = tel ? ` Zadzwoń: ${tel}.` : '';
      if (!cel) {
        msg.textContent = 'Formularz nie jest jeszcze aktywny.' + zapas;
        msg.classList.add('is-err');
        return;
      }
      msg.textContent = 'Wysyłanie…';
      try {
        const r = await fetch(cel, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!r.ok) throw new Error(r.status);
        form.reset();
        msg.textContent = 'Dziękujemy, wiadomość została wysłana.';
      } catch (_) {
        msg.textContent = 'Nie udało się wysłać wiadomości. Spróbuj ponownie później.' + zapas;
        msg.classList.add('is-err');
      }
    });
  }
})();
