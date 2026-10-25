'use strict';
(() => {
 // Report 11: the status and the sentence of each AI Agents scene. A scene's 9 s clock is its CSS animation
 // r11-clock (it starts when the scene appears and pauses in a hidden tab), so the texts stay in step with the
 // gestures: start 0-2 s, work 2-6 s (the sentence is typed), result 6-9 s. The texts come from one dictionary in
 // the page's language; without a clock (off screen, reduced motion) the scene shows its result.
 const data=document.getElementById('r11-copy');if(!data)return;
 const copy=JSON.parse(data.textContent),stages=[...document.querySelectorAll('.r11-stage[data-scene]')];
 const reduce=matchMedia('(prefers-reduced-motion: reduce)'),shown=new Map(),rhythm=new Map();
 let lang=document.documentElement.lang;
 const words=()=>copy[lang]||copy.sq;
 // When each letter appears: 45-85 ms apart, a little longer after a space or a comma, so typing is not mechanical.
 const times=s=>{if(!rhythm.has(s)){let t=0;rhythm.set(s,[...s].map((ch,i)=>t+=45+(i*37)%41+(/[ ,.?!’]/.test(ch)?55:0)));}return rhythm.get(s);};
 function show(stage,state,text,typing){
  const key=state+'\n'+text+'\n'+typing;if(shown.get(stage)===key)return;shown.set(stage,key);
  stage.querySelector('[data-r11-state]').textContent=state;stage.querySelector('[data-r11-msg]').textContent=text;stage.classList.toggle('is-typing',typing);
 }
 function frame(){
  const w=words(),gated=document.documentElement.classList.contains('motion-ready');
  for(const stage of stages){
   const c=w[stage.dataset.scene];
   // Off screen (report10.js keeps the scene at rest) the scene shows its result and its animations are not read.
   if(reduce.matches||(gated&&!stage.classList.contains('is-live'))){show(stage,c.state_result,c.message_done,false);continue;}
   const clock=stage.getAnimations().find(a=>a.animationName==='r11-clock');
   if(!clock){show(stage,c.state_result,c.message_done,false);continue;}
   const t=(clock.effect.getComputedTiming().progress||0)*9000;
   if(t<2000)show(stage,c.state_start,w.demo,false);
   else if(t<6000){const s=[...c.message_work],n=times(c.message_work).filter(x=>x<=t-2300).length;show(stage,c.state_work,s.slice(0,n).join(''),n<s.length);}
   else show(stage,c.state_result,c.message_done,false);
  }
  requestAnimationFrame(frame);
 }
 // If the page language changes, every scene starts again from its beginning in the new language: the old
 // sentence is cleared at once, nothing half-typed is kept.
 new MutationObserver(()=>{
  if(document.documentElement.lang===lang)return;lang=document.documentElement.lang;shown.clear();
  for(const stage of stages){stage.querySelector('[data-r11-panel]').textContent=words()[stage.dataset.scene].panel;
   if(stage.classList.contains('is-live')){stage.classList.remove('is-live');void stage.offsetWidth;stage.classList.add('is-live');}}
 }).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
 requestAnimationFrame(frame);
})();
