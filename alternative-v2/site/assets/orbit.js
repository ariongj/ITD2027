'use strict';
// Report 09: a new card every 2.5 s (1.5 s reading + the same 1 s turn), and no seconds on screen: the
// indicators and the service name remain. Everything else below is the movement approved in report 08.
// Report 08: the four service banners on a continuous orbit, timed by JavaScript.
// The cards sit on one ellipse: the centre card in front, the neighbours at the sides, the fourth behind.
// The orbit position is a continuous number, so place, size and depth change together in one movement and
// the cards travel round (the card on the left passes behind to the right); the text is never turned round.
// Each step lasts 2.5 s: the centre card is read for 1.5 s, then the orbit turns one place in 1 s, so a new card
// arrives in the centre at 2.5, 5, 7.5 and 10 s. The progress bar in the active indicator reads the same clock.
// Indicators, a click on a side card and dragging (the cards follow the pointer; at
// about 40 px the orbit turns, on phones by swiping, vertical scrolling stays free) start a new cycle; a drag
// never opens a card, a click on the centre card opens its service. Hovering does not stop the orbit; it waits
// while the visitor drags or has keyboard focus inside it, and a hidden tab does not pile up changes. Keyboard
// users meet a pause button when they tab in. With reduced motion it never turns by itself and does not glide.
(() => {
 const root=document.querySelector('[data-orbit]');if(!root)return;
 const cards=[...root.querySelectorAll('[data-slide]')],dots=[...root.querySelectorAll('.slider-dot')];
 const n=cards.length;if(n<2)return;
 const stage=root.querySelector('.orbit-stage'),pause=root.querySelector('.orbit-pause');
 const caption=root.querySelector('[data-caption]');
 const STEP=2500,MOVE=1000,READ=STEP-MOVE,DRAG=40;
 const PLACES=['is-center','is-right','is-back','is-left'];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches,narrow=matchMedia('(max-width:800px)');
 const mod=k=>((k%n)+n)%n;
 const wrap=k=>{k=mod(k);return k>n/2?k-n:k;};
 const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
 let target=0,index=0,pos=0,anim=null,moving=false;
 let start=performance.now(),held=0,wasPaused=false;
 let stopped=reduced,focus=false,dragging=false,hidden=document.hidden,drag=null,suppress=false;
 root.querySelector('.orbit-controls').hidden=false;root.classList.add('is-ready','is-js');
 if(reduced){pause.hidden=true;root.classList.add('is-static');}

 // Where a card stands for a given offset from the centre (k = 0 front, ±1 sides, 2 behind).
 function draw(){
  cards.forEach((c,i)=>{
   const k=wrap(i-pos),a=k*Math.PI/2,s=Math.sin(a),d=Math.cos(a);
   let x,y,sc,op,ry,rz;
   if(narrow.matches){            // phones: one whole banner; the next one glides in from the side
    x=s*104;y=0;sc=1-.08*Math.abs(s);op=d>=0?1:Math.max(0,1+d*3);ry=0;rz=0;
    if(Math.abs(k)>=.999){x=0;op=0;}  // waiting cards stay hidden in place, not off the edge of the screen
   }else{                         // the orbit of page 4: large centre, smaller turned side cards, one behind
    x=s*66;y=d>=0?10*(1-d):10-4*(-d);sc=d>=0?.58+.42*d:.58-.18*(-d);op=Math.min(1,Math.max(0,(d+1)/.8));ry=14*s;rz=-3*s;
   }
   c.style.transform=`translate(-50%,-50%) translate(${x.toFixed(2)}%,${y.toFixed(2)}%) scale(${sc.toFixed(4)}) rotateY(${ry.toFixed(2)}deg) rotate(${rz.toFixed(2)}deg)`;
   c.style.opacity=op.toFixed(3);c.style.zIndex=String(Math.round(10+d*10));
   c.style.visibility=op<.02?'hidden':'visible';
  });
 }
 // Classes and accessibility follow the card the orbit is heading to.
 function places(){
  cards.forEach((c,i)=>{
   const k=mod(i-target),p=k===0?'is-center':k===1?'is-right':k===n-1?'is-left':'is-back';
   PLACES.forEach(x=>c.classList.toggle(x,x===p));
   if(p==='is-center'){c.removeAttribute('aria-hidden');c.removeAttribute('tabindex');}
   else{c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');}
  });
 }
 // The card now being read: indicator and caption.
 function mark(){
  index=mod(target);
  dots.forEach((d,k)=>{if(k===index)d.setAttribute('aria-current','true');else d.removeAttribute('aria-current');});
  if(caption)caption.textContent=cards[index].dataset.label;
 }
 function glide(to,dur){
  if(reduced||dur<=0){pos=to;anim=null;return;}
  anim={from:pos,to,t0:performance.now(),dur};
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
 }
 function tick(now){
  if(anim){const t=Math.min(1,(now-anim.t0)/anim.dur);pos=anim.from+(anim.to-anim.from)*ease(t);if(t>=1){pos=anim.to;anim=null;}}
  if(!isPaused()){
   const e=now-start;
   if(e>=READ&&!moving){moving=true;target+=1;places();glide(target,MOVE);}   // the turn begins at 1.5 s
   if(e>=STEP){moving=false;mark();start=e>=2*STEP?now:start+STEP;}          // the new card has arrived at 2.5 s
  }
  draw();render(now);requestAnimationFrame(tick);
 }
 // A manual choice turns the orbit the short way to that card and starts a new 5 s cycle.
 function goTo(i,dur=MOVE){
  target+=wrap(i-mod(target));moving=false;places();mark();glide(target,dur);
  start=performance.now();held=0;
 }

 dots.forEach((d,i)=>d.addEventListener('click',()=>goTo(i)));
 pause.addEventListener('click',()=>{stopped=!stopped;update();});
 root.addEventListener('focusin',e=>{if(e.target.matches(':focus-visible')){focus=true;update();}});
 root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){focus=false;update();}});
 document.addEventListener('visibilitychange',()=>{hidden=document.hidden;update();});

 // Dragging and swiping: the orbit follows the pointer and settles on the nearest card when released.
 const span=()=>Math.max(1,stage.clientWidth*(narrow.matches?1:.47)*.9);
 stage.addEventListener('pointerdown',e=>{if(e.button!==0)return;drag={x:e.clientX,y:e.clientY,pos0:pos,target0:target,active:false};});
 stage.addEventListener('pointermove',e=>{
  if(!drag)return;
  const dx=e.clientX-drag.x,dy=e.clientY-drag.y;
  if(!drag.active&&Math.abs(dx)>8&&Math.abs(dx)>Math.abs(dy)){drag.active=true;dragging=true;anim=null;root.classList.add('is-dragging');update();}
  if(drag.active&&!reduced)pos=drag.pos0-Math.max(-1,Math.min(1,dx/span()));
 });
 function release(e,cancel){
  if(!drag)return;
  const d=drag,dx=e.clientX-d.x;drag=null;
  if(!d.active)return;
  dragging=false;root.classList.remove('is-dragging');
  suppress=true;setTimeout(()=>{suppress=false;},60);
  if(!cancel&&Math.abs(dx)>=DRAG){target=d.target0+(dx<0?1:-1);}else{target=d.target0;}
  moving=false;places();mark();glide(target,Math.max(250,MOVE*Math.min(1,Math.abs(target-pos))));
  start=performance.now();held=0;update();
 }
 stage.addEventListener('pointerup',e=>release(e,false));
 stage.addEventListener('pointercancel',e=>release(e,true));
 stage.addEventListener('dragstart',e=>e.preventDefault());
 // After a drag no card opens; a click on a side card brings it to the centre; the centre card opens.
 cards.forEach((c,i)=>c.addEventListener('click',e=>{
  if(suppress){e.preventDefault();suppress=false;return;}
  if(i!==mod(target)||anim){e.preventDefault();if(i!==mod(target))goTo(i);}
 }));

 places();mark();draw();update();
 if(reduced)render(performance.now());
 requestAnimationFrame(tick);
})();
