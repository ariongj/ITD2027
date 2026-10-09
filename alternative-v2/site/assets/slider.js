'use strict';
// Home banner (Report 02). The 10-second progress bar is a CSS animation: when it ends, the next slide
// shows, so pausing the animation pauses the timer. With reduced motion the stylesheets switch animations
// off, so the banner never turns by itself; arrows, dots and swipe still work.
(() => {
 const root=document.querySelector('[data-slider]');if(!root)return;
 const slides=[...root.querySelectorAll('[data-slide]')],dots=[...root.querySelectorAll('.slider-dot')];
 if(slides.length<2)return;
 const list=root.querySelector('.slides'),pause=root.querySelector('.slider-pause');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let index=0,stopped=reduced,hover=false,focus=false,touch=false;
 root.querySelector('.slider-controls').hidden=false;root.classList.add('is-ready');
 if(reduced)pause.hidden=true;
 function update(){
  const paused=stopped||hover||focus||touch;
  root.classList.toggle('is-paused',paused);
  // Announce slide changes only when the visitor is in control.
  list.setAttribute('aria-live',paused?'polite':'off');
  pause.setAttribute('aria-label',stopped?pause.dataset.play:pause.dataset.pause);
  pause.classList.toggle('is-stopped',stopped);
 }
 function show(next){
  index=(next+slides.length)%slides.length;
  slides.forEach((s,i)=>s.classList.toggle('is-active',i===index));
  dots.forEach((d,i)=>{if(i===index)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});
  const fill=dots[index].querySelector('.slider-fill');
  fill.classList.remove('is-running');void fill.offsetWidth;fill.classList.add('is-running');
  // Optional "01 / 03" counter (ITD2027/M).
  const counter=root.querySelector('[data-counter]');if(counter)counter.textContent=String(index+1).padStart(2,'0');
 }
 dots.forEach((d,i)=>{
  d.addEventListener('click',()=>show(i));
  d.querySelector('.slider-fill').addEventListener('animationend',()=>{if(i===index)show(index+1);});
 });
 root.querySelector('.slider-prev').addEventListener('click',()=>show(index-1));
 root.querySelector('.slider-next').addEventListener('click',()=>show(index+1));
 pause.addEventListener('click',()=>{stopped=!stopped;update();});
 // Pause while a mouse is over the banner, while keyboard focus is inside it, and during a touch.
 root.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'){hover=true;update();}});
 root.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse'){hover=false;update();}});
 root.addEventListener('focusin',e=>{if(e.target.matches(':focus-visible')){focus=true;update();}});
 root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){focus=false;update();}});
 let startX=0,startY=0;
 root.addEventListener('touchstart',e=>{startX=e.touches[0].clientX;startY=e.touches[0].clientY;touch=true;update();},{passive:true});
 root.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-startX,dy=e.changedTouches[0].clientY-startY;
  touch=false;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy))show(index+(dx<0?1:-1));update();
 },{passive:true});
 root.addEventListener('touchcancel',()=>{touch=false;update();},{passive:true});
 update();show(0);
})();
