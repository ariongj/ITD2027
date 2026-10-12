'use strict';
// ITD2027 · opus: phone menu, header shadow, the projects rail, the enquiry form. No inline code, no tracking.
(() => {
 const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
 const header = document.querySelector('[data-header]');
 const button = document.querySelector('[data-menu]'), nav = document.getElementById('nav');
 if (button && nav) {
  const set = open => { button.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); };
  button.addEventListener('click', () => set(button.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', e => { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { set(false); button.focus(); } });
  matchMedia('(min-width:1001px)').addEventListener('change', e => { if (e.matches) set(false); });
 }
 const onScroll = () => header && header.classList.toggle('is-scrolled', scrollY > 8);
 addEventListener('scroll', onScroll, { passive: true }); onScroll();

 // Projects rail: arrows move one card; they switch off at either end.
 document.querySelectorAll('[data-rail]').forEach(rail => {
  const track = rail.querySelector('[data-rail-track]'), prev = rail.querySelector('[data-rail-prev]'), next = rail.querySelector('[data-rail-next]');
  const step = () => { const card = track.firstElementChild; return card ? card.getBoundingClientRect().width + 20 : 320; };
  const update = () => { prev.disabled = track.scrollLeft <= 4; next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4; };
  const go = dir => track.scrollBy({ left: dir * step(), behavior: reduce ? 'auto' : 'smooth' });
  prev.addEventListener('click', () => go(-1)); next.addEventListener('click', () => go(1));
  track.addEventListener('scroll', update, { passive: true }); addEventListener('resize', update); update();
 });

 // A service chosen elsewhere (?service=...) is preselected in the form.
 const select = document.querySelector('[data-service]');
 const wanted = new URLSearchParams(location.search).get('service');
 if (select && wanted) {
  const value = wanted.slice(0, 120);
  if (![...select.options].some(o => o.value === value)) select.add(new Option(value, value));
  select.value = value;
 }

 // Enquiry form: sent to Formspree; success is shown only when Formspree confirms it. Without JavaScript the form posts normally.
 document.querySelectorAll('[data-form]').forEach(form => {
  const status = form.querySelector('.form-status'), submit = form.querySelector('[type=submit]');
  form.addEventListener('submit', async e => {
   e.preventDefault();
   if (!form.reportValidity()) return;
   submit.disabled = true; status.dataset.state = ''; status.textContent = form.dataset.sending;
   try {
    const response = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
    const result = await response.json().catch(() => ({}));
    if (!response.ok || result.ok !== true) throw new Error('unconfirmed');
    status.textContent = form.dataset.success; status.dataset.state = 'success'; form.reset();
   } catch {
    status.textContent = form.dataset.failure; status.dataset.state = 'error';
   } finally { submit.disabled = false; }
  });
 });
})();
