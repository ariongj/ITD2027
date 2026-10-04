'use strict';
(() => {
 const lang=document.documentElement.lang;
 const text={sq:['Cakto një takim','Po hapet kalendari…','Nëse kalendari nuk hapet, vazhdo në Calendly.','Hap në Calendly','Mbyll','Takimi u konfirmua nga Calendly.'],en:['Book a meeting','Opening the calendar…','If the calendar does not open, continue on Calendly.','Open Calendly','Close','Your meeting was confirmed by Calendly.'],de:['Termin vereinbaren','Kalender wird geöffnet…','Falls der Kalender nicht lädt, öffnen Sie Calendly direkt.','Calendly öffnen','Schließen','Ihr Termin wurde von Calendly bestätigt.']}[lang];
 let loader=null,trigger=null,timer,initialized=false,initializing=false,confirmed=false;const seen=new Set();
 const dialog=document.createElement('dialog');dialog.className='booking-dialog';dialog.setAttribute('aria-labelledby','booking-title');
 const bar=document.createElement('div');bar.className='booking-toolbar';const title=document.createElement('h2');title.id='booking-title';title.textContent=text[0];const close=document.createElement('button');close.type='button';close.className='button outline';close.textContent=text[4];close.onclick=()=>dialog.close();bar.append(title,close);
 const status=document.createElement('p');status.className='booking-status';status.setAttribute('role','status');const host=document.createElement('div');host.className='booking-host';
 const fallback=document.createElement('a');fallback.className='text-link booking-fallback';fallback.target='_blank';fallback.rel='noopener noreferrer';fallback.dataset.bookingExternal='true';fallback.textContent=text[3]+' ↗';
 dialog.append(bar,status,host,fallback);document.body.append(dialog);dialog.addEventListener('close',()=>{clearTimeout(timer);trigger?.focus({preventScroll:true});});
 function load(){if(window.Calendly)return Promise.resolve();if(loader)return loader;loader=new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='https://assets.calendly.com/assets/external/widget.js';s.async=true;s.onload=()=>window.Calendly?resolve():reject(new Error('Unavailable'));s.onerror=()=>{s.remove();loader=null;reject(new Error('Unavailable'));};document.head.append(s);});return loader;}
 document.addEventListener('click',async e=>{
  const a=e.target.closest('a[href]');if(!a||a.dataset.bookingExternal||new URL(a.href).hostname!=='calendly.com'||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
  // Browsers without <dialog> keep the plain link to Calendly.
  if(typeof dialog.showModal!=='function')return;
  e.preventDefault();trigger=a;fallback.href=a.href;dialog.showModal();close.focus();if(!confirmed)status.textContent=initialized?text[2]:text[1];
  // One calendar per page, also when the dialog is reopened while widget.js is still loading.
  if(initialized||initializing)return;
  initializing=true;
  timer=setTimeout(()=>{if(dialog.open&&!confirmed)status.textContent=text[2];},15000);
  try{await load();if(!dialog.open||host.querySelector('iframe'))return;window.Calendly.initInlineWidget({url:a.href,parentElement:host});initialized=true;host.querySelector('iframe')?.setAttribute('title',text[0]);}
  catch{clearTimeout(timer);status.textContent=text[2];}
  finally{initializing=false;}
 });
 window.addEventListener('message',e=>{
  const frame=host.querySelector('iframe');if(e.origin!=='https://calendly.com'||!frame||e.source!==frame.contentWindow||!dialog.open)return;
  if(typeof e.data?.event!=='string'||!e.data.event.startsWith('calendly.'))return;
  clearTimeout(timer);
  if(e.data.event==='calendly.event_scheduled'){
   const uri=e.data.payload?.event?.uri;if(typeof uri!=='string'||!uri.startsWith('https://api.calendly.com/scheduled_events/')||seen.has(uri))return;
   seen.add(uri);confirmed=true;status.textContent=text[5];
   // No invitee identifiers or payload fields pass into analytics.
   window.ITDTracking?.record('book_meeting','','calendly-confirmed');
  }else if(!confirmed)status.textContent=text[2];
 });
})();
