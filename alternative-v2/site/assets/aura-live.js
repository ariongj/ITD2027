'use strict';
// Report 09: the AURA emblem on ITD Labs moves as in the AURA app (ribbons, pulse and halo in report09.css) and
// "Consider it handled." is typed under the static "Say it.": a short wait with the cursor, about 60 ms per letter,
// the full phrase for 3 s, a 300 ms fade, then again. It runs only while the box is on screen and the tab is active;
// with reduced motion the emblem stands still and the full phrase shows, without a cursor.
(() => {
 const fig=document.querySelector('[data-aura-live]');if(!fig)return;
 const out=fig.querySelector('[data-typed]'),phrase='Consider it handled.';
 const WAIT=700,CHAR=60,HOLD=3000,FADE=300;
 if(matchMedia('(prefers-reduced-motion: reduce)').matches){out.textContent=phrase;fig.classList.add('is-static','is-full');return;}
 let onScreen=false,timer=null,i=0,phase='wait';
 const active=()=>onScreen&&!document.hidden;
 function step(){
  timer=null;if(!active())return;
  if(phase==='wait'){fig.classList.remove('is-fading','is-full');out.textContent='';i=0;phase='type';timer=setTimeout(step,WAIT);return;}
  if(phase==='type'){
   i+=1;out.textContent=phrase.slice(0,i);
   if(i<phrase.length){timer=setTimeout(step,CHAR);return;}
   fig.classList.add('is-full');phase='hold';timer=setTimeout(step,HOLD);return;
  }
  if(phase==='hold'){fig.classList.add('is-fading');phase='wait';timer=setTimeout(step,FADE);}
 }
 function sync(){
  fig.classList.toggle('is-running',active());
  if(active()&&!timer)step();
  if(!active()&&timer){clearTimeout(timer);timer=null;}
 }
 out.textContent='';phase='wait';
 if('IntersectionObserver' in window){
  new IntersectionObserver(entries=>{onScreen=entries.some(e=>e.isIntersecting);sync();},{threshold:.2}).observe(fig);
 }else{onScreen=true;}
 document.addEventListener('visibilitychange',sync);
 sync();
})();
