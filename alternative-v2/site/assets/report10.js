'use strict';
(() => {
 // Report 10: each character ([data-motion]) moves only while it is on screen and the tab is visible. Its loop
 // starts from the beginning when it appears; characters that appear together start 1.1 s apart (--s), so on a
 // wide screen the six agents begin one after another and on a phone each starts as soon as its card is in view.
 // Without this script (or IntersectionObserver) the CSS loops simply run.
 const figures=document.querySelectorAll('[data-motion]'),root=document.documentElement;
 if(figures.length&&'IntersectionObserver' in window){
  const io=new IntersectionObserver(entries=>{
   let k=0;
   for(const e of entries.sort((a,b)=>a.target.compareDocumentPosition(b.target)&Node.DOCUMENT_POSITION_FOLLOWING?-1:1)){
    if(e.isIntersecting&&!e.target.classList.contains('is-live')){e.target.style.setProperty('--s',(k++*1.1).toFixed(1)+'s');e.target.classList.add('is-live');}
    else if(!e.isIntersecting)e.target.classList.remove('is-live');
   }
  },{threshold:.2});
  figures.forEach(f=>io.observe(f));
  const sync=()=>root.classList.toggle('motion-hidden',document.hidden);
  document.addEventListener('visibilitychange',sync);sync();
  root.classList.add('motion-ready');
 }
 // Terms and Privacy: the topic menu marks the section being read.
 const toc=document.querySelector('[data-toc]');
 if(toc&&'IntersectionObserver' in window){
  const links=[...toc.querySelectorAll('a[href^="#"]')],visible=new Set();
  const mark=()=>{const a=links.find(x=>visible.has(x.hash.slice(1)));if(!a)return;links.forEach(x=>x===a?x.setAttribute('aria-current','location'):x.removeAttribute('aria-current'));};
  const io=new IntersectionObserver(entries=>{for(const e of entries)e.isIntersecting?visible.add(e.target.id):visible.delete(e.target.id);mark();},{rootMargin:'-110px 0px -55% 0px'});
  links.forEach(a=>{const s=document.getElementById(a.hash.slice(1));if(s)io.observe(s);});
 }
})();
