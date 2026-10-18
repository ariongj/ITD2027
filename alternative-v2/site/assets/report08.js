'use strict';
// Report 08: the orientation map on Contact (Google Maps loads only after a click) and the WhatsApp button on
// every page (it steps aside while the menu or a dialog is open, rises above a cookie panel, and never covers
// the form's send button or the footer text).
(() => {
 const frame=document.querySelector('[data-map]');
 const load=frame&&frame.querySelector('[data-map-load]');
 if(load)load.addEventListener('click',()=>{
  const iframe=document.createElement('iframe');
  iframe.src=frame.dataset.map;iframe.title=frame.dataset.mapTitle;iframe.loading='lazy';
  iframe.referrerPolicy='no-referrer-when-downgrade';iframe.allowFullscreen=true;
  frame.classList.add('is-loaded');frame.replaceChildren(iframe);iframe.focus({preventScroll:true});
 });

 const wa=document.querySelector('[data-wa-float]');if(!wa)return;
 // Away while the form's send row or the bottom of the footer is on screen.
 const watch=[...document.querySelectorAll('.form-submit,.footer-bottom,.r7-social-phone')];
 const near=new Set();
 if('IntersectionObserver' in window&&watch.length){
  const io=new IntersectionObserver(entries=>{
   entries.forEach(en=>{if(en.isIntersecting)near.add(en.target);else near.delete(en.target);});
   wa.classList.toggle('is-away',near.size>0);
  },{rootMargin:'0px 0px -8px 0px'});
  watch.forEach(el=>io.observe(el));
 }
 // Above a cookie panel (shown only when measurement is enabled on the final domain).
 const lift=()=>{
  const panel=document.querySelector('.consent-panel');
  const h=panel&&!panel.hidden&&panel.offsetParent!==null?panel.getBoundingClientRect().height:0;
  wa.style.setProperty('--wa-lift',h?`${Math.round(h)+16}px`:'0px');
 };
 lift();new MutationObserver(lift).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']});
 addEventListener('resize',lift);
})();
