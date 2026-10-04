/* IT Department chat launcher — loads the Kraken assistant in an iframe on demand.
   Same behaviour as before; the button is restyled to match the new design. */
(() => {
  if (window.__ITDKrakenChat) return;
  window.__ITDKrakenChat = true;
  const origin = 'https://assistant.krakenos.cloud';
  const lang = document.documentElement.lang || 'sq';
  const label = lang.startsWith('sq') ? 'Bisedo me ITD' : lang.startsWith('de') ? 'Mit ITD chatten' : 'Chat with ITD';
  const root = document.createElement('div');
  root.id = 'itd-kraken-chat';
  const button = document.createElement('button');
  button.type = 'button';
  button.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12Z"/></svg><span>' + label + '</span>';
  button.setAttribute('aria-expanded', 'false');
  button.setAttribute('aria-controls', 'itd-kraken-frame');
  const frame = document.createElement('iframe');
  frame.id = 'itd-kraken-frame';
  frame.title = 'IT Department chat';
  frame.hidden = true;
  frame.referrerPolicy = 'no-referrer';
  const style = document.createElement('style');
  style.textContent =
    '#itd-kraken-chat{position:fixed;right:16px;bottom:max(16px,env(safe-area-inset-bottom));z-index:90;font-family:var(--font-sans,system-ui,sans-serif)}' +
    '#itd-kraken-chat button{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:0 16px 0 14px;border:1px solid rgba(255,255,255,.12);border-radius:999px;background:var(--text,#141417);color:var(--bg,#fff);font:600 14px var(--font-sans,system-ui,sans-serif);box-shadow:0 12px 30px -12px rgba(0,0,0,.5);cursor:pointer;transition:transform .18s}' +
    '#itd-kraken-chat button:hover{transform:translateY(-1px)}' +
    '#itd-kraken-chat button:focus-visible{outline:2px solid #e00000;outline-offset:3px}' +
    '#itd-kraken-frame{position:fixed;right:16px;bottom:76px;width:390px;height:min(640px,calc(100dvh - 100px));max-width:calc(100vw - 32px);border:1px solid var(--line-strong,#dbe1e9);border-radius:18px;background:#fff;box-shadow:0 24px 70px -20px rgba(0,0,0,.45)}' +
    '#itd-kraken-frame[hidden]{display:none}' +
    '@media(max-width:560px){#itd-kraken-chat button{width:52px;height:52px;min-height:52px;padding:0;justify-content:center}' +
    '#itd-kraken-chat button span{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}' +
    '#itd-kraken-chat[data-open="true"]{bottom:14px}#itd-kraken-chat[data-open="true"] iframe{left:10px;right:10px;bottom:76px;width:auto;max-width:none;height:calc(100dvh - 92px)}}';
  function close() {
    frame.hidden = true;
    root.dataset.open = 'false';
    button.setAttribute('aria-expanded', 'false');
    button.focus();
  }
  button.onclick = () => {
    if (!frame.hidden) return close();
    if (!frame.src) frame.src = origin + '/chat?lang=' + encodeURIComponent(lang);
    frame.hidden = false;
    root.dataset.open = 'true';
    button.setAttribute('aria-expanded', 'true');
    frame.focus();
  };
  window.addEventListener('message', (e) => {
    if (e.origin === origin && e.source === frame.contentWindow && e.data?.type === 'itd-chat-close') close();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !frame.hidden) close();
  });
  root.append(frame, button);
  document.head.append(style);
  document.body.append(root);
})();
