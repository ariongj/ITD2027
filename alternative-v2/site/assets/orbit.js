'use strict';
// Report 08: the four service banners on an orbit, timed by JavaScript (not by the progress animation).
// Each step lasts 5 s: the centre card is read for 4 s, then the cards change place, size and depth in 1 s,
// so a new card arrives in the centre at 5, 10, 15 and 20 s. The progress bar and the countdown ("05 s" … "01 s")
// under the card read the same clock. Indicators, a click on a side card and dragging (Pointer Events, about
// 40 px; on phones a horizontal swipe that leaves vertical scrolling alone) start a new 5 s cycle; a drag never
// opens a card, a click on the centre card opens its service. Hovering does not stop the orbit; it waits while
// the visitor drags or has keyboard focus inside it, and a hidden tab does not pile up changes. Keyboard users
// also meet a pause button when they tab into it. With reduced motion it never turns by itself.
(() => {
 const root=document.querySelector('[data-orbit]');if(!root)return;
 const cards=[...root.querySelectorAll('[data-slide]')],dots=[...root.querySelectorAll('.slider-dot')];
 const n=cards.length;if(n<2)return;
 const stage=root.querySelector('.orbit-stage'),pause=root.querySelector('.orbit-pause');
 const caption=root.querySelector('[data-caption]'),count=root.querySelector('[data-countdown]');
 const STEP=5000,MOVE=1000,READ=STEP-MOVE,DRAG=40;
 const PLACES=['is-center','is-right','is-back','is-left'];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let index=0,shown=0,start=performance.now(),held=0,wasPaused=false;
 let stopped=reduced,focus=false,dragging=false,hidden=document.hidden;
 root.querySelector('.orbit-controls').hidden=false;root.classList.add('is-ready');
 if(reduced){pause.hidden=true;root.classList.add('is-static');}

 function place(i,center){const d=(i-center+n)%n;return d===0?'is-center':d===1?'is-right':d===n-1?'is-left':'is-back';}
 // Position, size and depth (CSS classes, 1 s transition).
 function layout(center){
  shown=center;
  cards.forEach((c,i)=>{
   const p=place(i,center);PLACES.forEach(x=>c.classList.toggle(x,x===p));
   if(p==='is-center'){c.removeAttribute('aria-hidden');c.removeAttribute('tabindex');}
   else{c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');}
  });
 }
 // The card that is now the one being read: indicator, caption.
 function mark(i){
  index=i;
  dots.forEach((d,k)=>{if(k===i)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});
  if(caption)caption.textContent=cards[i].dataset.label;
 }
 const isPaused=()=>stopped||focus||dragging||hidden;
 function update(){
  const p=isPaused(),now=performance.now();
  if(p&&!wasPaused)held=Math.min(now-start,STEP);
  if(!p&&wasPaused)start=now-held;
  wasPaused=p;
  root.classList.toggle('is-paused',p);
  stage.setAttribute('aria-live',p?'polite':'off');
  pause.textContent=stopped?pause.dataset.play:pause.dataset.pause;
 }
 function render(now){
  const e=Math.max(0,Math.min(isPaused()?held:now-start,STEP));
  dots.forEach((d,k)=>{d.querySelector('.slider-fill').style.transform=`scaleX(${k===index?e/STEP:0})`;});
  if(count)count.textContent=String(Math.max(1,Math.ceil((STEP-e)/1000))).padStart(2,'0')+' s';
 }
 function tick(now){
  if(!isPaused()){
   const e=now-start;
   if(e>=READ&&shown===index)layout((index+1)%n);              // the move begins at 4 s
   if(e>=STEP){mark((index+1)%n);start=e>=2*STEP?now:start+STEP;} // the new card has arrived at 5 s
  }
  render(now);requestAnimationFrame(tick);
 }
 // A manual choice shows that card at once and starts a new 5 s cycle.
 function goTo(i){
  i=(i+n)%n;layout(i);mark(i);start=performance.now();held=0;
 }

 dots.forEach((d,i)=>d.addEventListener('click',()=>goTo(i)));
 pause.addEventListener('click',()=>{stopped=!stopped;update();});
 root.addEventListener('focusin',e=>{if(e.target.matches(':focus-visible')){focus=true;update();}});
 root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){focus=false;update();}});
 document.addEventListener('visibilitychange',()=>{hidden=document.hidden;update();});

 // Dragging and swiping (the stage has touch-action: pan-y, so vertical scrolling stays with the browser).
 let px=null,py=0,suppress=false;
 stage.addEventListener('pointerdown',e=>{if(e.button!==0)return;px=e.clientX;py=e.clientY;});
 stage.addEventListener('pointermove',e=>{
  if(px===null)return;
  const dx=e.clientX-px,dy=e.clientY-py;
  if(!dragging&&Math.abs(dx)>8&&Math.abs(dx)>Math.abs(dy)){dragging=true;root.classList.add('is-dragging');update();}
 });
 function release(e,cancel){
  if(px===null)return;
  const dx=e.clientX-px;px=null;
  if(!dragging)return;
  dragging=false;root.classList.remove('is-dragging');
  suppress=true;setTimeout(()=>{suppress=false;},60);
  if(!cancel&&Math.abs(dx)>=DRAG)goTo(index+(dx<0?1:-1));
  update();
 }
 stage.addEventListener('pointerup',e=>release(e,false));
 stage.addEventListener('pointercancel',e=>release(e,true));
 stage.addEventListener('dragstart',e=>e.preventDefault());
 // After a drag no card opens; a click on a side card brings it to the centre; the centre card opens.
 cards.forEach((c,i)=>c.addEventListener('click',e=>{
  if(suppress){e.preventDefault();suppress=false;return;}
  if(i!==index||shown!==index){e.preventDefault();goTo(i);}
 }));

 layout(0);mark(0);update();
 if(reduced)render(performance.now());else requestAnimationFrame(tick);
})();
