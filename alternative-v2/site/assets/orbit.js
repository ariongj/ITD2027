'use strict';
// Report 07: the four service banners on an orbit. Every 6 s the card on the right comes forward to the
// centre and grows, the centre card moves to the left and shrinks, the left card goes to the back and the
// back card comes in on the right — position, size and depth change in one 900 ms transition (CSS).
// The 6 s progress bar is a CSS animation; when it ends the next card comes, so pausing the animation pauses
// the timer. The indicators choose a card and the 6 s rhythm continues from there. There is no visible pause
// button (report 07): the orbit stops while a mouse is over it, while keyboard focus is inside and during a
// touch; keyboard users meet a pause button when they tab into it; with reduced motion it never turns by itself.
(() => {
 const root=document.querySelector('[data-orbit]');if(!root)return;
 const cards=[...root.querySelectorAll('[data-slide]')],dots=[...root.querySelectorAll('.slider-dot')];
 const n=cards.length;if(n<2)return;
 const stage=root.querySelector('.orbit-stage'),pause=root.querySelector('.orbit-pause'),caption=root.querySelector('[data-caption]');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const PLACES=['is-center','is-right','is-back','is-left'];
 let index=0,stopped=reduced,hover=false,focus=false,touch=false;
 root.querySelector('.orbit-controls').hidden=false;root.classList.add('is-ready');
 if(reduced)pause.hidden=true;
 function place(i){const d=(i-index+n)%n;return d===0?'is-center':d===1?'is-right':d===n-1?'is-left':'is-back';}
 function update(){
  const paused=stopped||hover||focus||touch;
  root.classList.toggle('is-paused',paused);
  // Announce card changes only when the visitor is in control.
  stage.setAttribute('aria-live',paused?'polite':'off');
  pause.textContent=stopped?pause.dataset.play:pause.dataset.pause;
 }
 function show(next){
  index=(next+n)%n;
  cards.forEach((c,i)=>{
   const p=place(i);PLACES.forEach(x=>c.classList.toggle(x,x===p));
   // Only the centre card is a link for keyboard and screen readers; the others turn the orbit on click.
   if(p==='is-center'){c.removeAttribute('aria-hidden');c.removeAttribute('tabindex');}
   else{c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');}
  });
  dots.forEach((d,i)=>{if(i===index)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});
  const fill=dots[index].querySelector('.slider-fill');
  fill.classList.remove('is-running');void fill.offsetWidth;fill.classList.add('is-running');
  if(caption)caption.textContent=cards[index].dataset.label;
 }
 dots.forEach((d,i)=>{
  d.addEventListener('click',()=>show(i));
  d.querySelector('.slider-fill').addEventListener('animationend',()=>{if(i===index)show(index+1);});
 });
 cards.forEach((c,i)=>c.addEventListener('click',e=>{if(i!==index){e.preventDefault();show(i);}}));
 pause.addEventListener('click',()=>{stopped=!stopped;update();});
 root.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'){hover=true;update();}});
 root.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse'){hover=false;update();}});
 root.addEventListener('focusin',e=>{if(e.target.matches(':focus-visible')){focus=true;update();}});
 root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){focus=false;update();}});
 let startX=0,startY=0,moved=false;
 root.addEventListener('touchstart',e=>{startX=e.touches[0].clientX;startY=e.touches[0].clientY;moved=false;touch=true;update();},{passive:true});
 root.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-startX,dy=e.changedTouches[0].clientY-startY;
  touch=false;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)){moved=true;show(index+(dx<0?1:-1));}update();
 },{passive:true});
 root.addEventListener('touchcancel',()=>{touch=false;update();},{passive:true});
 // A swipe must not also open the card under the finger.
 stage.addEventListener('click',e=>{if(moved){e.preventDefault();moved=false;}},true);
 update();show(0);
})();
