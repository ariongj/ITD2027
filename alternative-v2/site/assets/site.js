'use strict';
const $=(s,root=document)=>root.querySelector(s);
const $$=(s,root=document)=>[...root.querySelectorAll(s)];
const copy=JSON.parse($('#site-copy').textContent);
const menu=$('.menu-toggle'),nav=$('#main-nav');
const labsButton=$('.labs-toggle'),labsMenu=$('#labs-menu');
function closeLabs(restore=false){labsButton.setAttribute('aria-expanded','false');labsMenu.hidden=true;if(restore)labsButton.focus();}
labsButton.addEventListener('click',()=>{const open=labsButton.getAttribute('aria-expanded')!=='true';labsButton.setAttribute('aria-expanded',String(open));labsMenu.hidden=!open;});
document.addEventListener('click',e=>{if(!e.target.closest('.labs-nav'))closeLabs();});
document.addEventListener('focusin',e=>{if(!e.target.closest('.labs-nav'))closeLabs();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!labsMenu.hidden){e.stopImmediatePropagation();closeLabs(true);}});

function closeMenu(restore=false){closeLabs();menu.setAttribute('aria-expanded','false');nav.classList.remove('is-open');if(restore)menu.focus();}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true')closeMenu(true);});
document.addEventListener('click',e=>{if(!e.target.closest('.header'))closeMenu();});
$$('a',nav).forEach(a=>a.addEventListener('click',()=>closeMenu()));
matchMedia('(min-width:1121px)').addEventListener('change',e=>{if(e.matches)closeMenu();});

$$('[data-filter-group]').forEach(group=>{
 const name=group.dataset.filterGroup,buttons=$$('button',group),items=$$(`[data-filter-item="${name}"]`);
 function filter(key){let count=0;items.forEach(item=>{const show=key==='all'||item.dataset.category.split(' ').includes(key);item.hidden=!show;if(show)count++;});buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===key)));const status=$(`[data-filter-status="${name}"]`);if(status)status.textContent=`${count} ${copy.count}`;}
 buttons.forEach(b=>b.addEventListener('click',()=>filter(b.dataset.filter)));
});
function revealHash(){
 let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
 if(!id)return;const target=document.getElementById(id);if(!target)return;
 const filtered=target.closest('[data-filter-item]');if(filtered?.hidden){const all=$(`[data-filter-group="${filtered.dataset.filterItem}"] [data-filter="all"]`);all?.click();}
 if(target.tagName==='DETAILS')target.open=true;
 const parent=target.closest('details');if(parent)parent.open=true;
 requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
}
window.addEventListener('hashchange',revealHash);if(location.hash)revealHash();

const modal=$('#lightbox'),modalImage=$('#lightbox-image');let modalTrigger=null;
$$('[data-lightbox]').forEach(a=>a.addEventListener('click',e=>{
 e.preventDefault();modalTrigger=a;$('#lightbox-title').textContent=a.dataset.lightbox;modalImage.src=a.getAttribute('href');modalImage.alt=a.dataset.lightbox;modal.showModal();$('.lightbox-close').focus();
}));
$('.lightbox-close').addEventListener('click',()=>modal.close());
modal.addEventListener('click',e=>{const r=modal.getBoundingClientRect();if(e.target===modal&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))modal.close();});
modal.addEventListener('close',()=>{modalImage.removeAttribute('src');modalTrigger?.focus({preventScroll:true});});
modal.addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();$('.lightbox-close').focus();}});

const fields=['name','email','company','phone','service','message'];
$$('.enquiry-form').forEach(form=>{
 const key='itd-proposal-v1-'+form.dataset.form,status=$('.form-status',form),submit=$('[type="submit"]',form),recovery=$('.form-recovery',form);let pending=false;
 const field=name=>form.elements.namedItem(name);
 function addService(value){const select=field('service');if(value&&!Array.from(select.options).some(o=>o.value===value)){select.add(new Option(value,value));}select.value=value;}
 function save(){try{const draft={};fields.forEach(n=>draft[n]=field(n).value);sessionStorage.setItem(key,JSON.stringify(draft));}catch{}}
 try{const draft=JSON.parse(sessionStorage.getItem(key)||'null');if(draft&&typeof draft==='object'){fields.forEach(n=>{if(typeof draft[n]!=='string')return;if(n==='service')addService(draft[n].slice(0,200));else field(n).value=draft[n].slice(0,field(n).maxLength>0?field(n).maxLength:3000);});}}catch{}
 const service=new URLSearchParams(location.search).get('service');if(service){addService(service.slice(0,200));save();}
 form.addEventListener('input',e=>{if(e.target.setCustomValidity)e.target.setCustomValidity('');save();if(status.dataset.state==='success'){status.textContent='';delete status.dataset.state;}});
 form.addEventListener('change',save);
 $$('[data-agent]').forEach(a=>a.addEventListener('click',()=>{if(form.dataset.form!=='ai')return;addService(a.dataset.agent);save();requestAnimationFrame(()=>field('name').focus({preventScroll:true}));}));
 $$('[data-creative-service]').forEach(a=>a.addEventListener('click',()=>{if(form.dataset.form!=='creative')return;addService(a.dataset.creativeService);save();requestAnimationFrame(()=>field('name').focus({preventScroll:true}));}));
 form.addEventListener('submit',async e=>{
  e.preventDefault();if(pending)return;
  for(const n of ['name','email','message']){const el=field(n);el.setCustomValidity(el.value.trim()?'':copy.invalid);}
  if(!form.reportValidity())return;
  save();const data=new FormData(form);for(const n of fields)data.set(n,field(n).value.trim());
  pending=true;form.setAttribute('aria-busy','true');submit.textContent=copy.sending;status.textContent=copy.sending;status.dataset.state='pending';recovery.hidden=true;
  const inputs=$$('input,select,textarea,button',form);inputs.forEach(el=>el.disabled=true);
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),20000);
  try{
   const response=await fetch(form.action,{method:'POST',body:data,headers:{Accept:'application/json'},signal:controller.signal});
   const result=await response.json();if(!response.ok||result.ok!==true)throw new Error('Unconfirmed delivery');
   const selected=data.get('service')||'';window.ITDTracking?.record('generate_lead',selected);
   if(new URLSearchParams(location.search).get('intent')==='demo')window.ITDTracking?.record('request_demo',selected,'demo');
   status.textContent=copy.success;status.dataset.state='success';form.reset();try{sessionStorage.removeItem(key);}catch{}
  }catch{
   status.textContent=copy.failure;status.dataset.state='error';recovery.hidden=false;
  }finally{
   clearTimeout(timer);pending=false;inputs.forEach(el=>el.disabled=false);form.removeAttribute('aria-busy');submit.textContent=copy.send;status.focus({preventScroll:true});
  }
 });
});
// Carry selected service through language changes without carrying personal data in URLs.
const requestedService=new URLSearchParams(location.search).get('service');
if(requestedService)$$('.languages a').forEach(a=>{const url=new URL(a.href);url.searchParams.set('service',requestedService.slice(0,200));if(new URLSearchParams(location.search).get('intent')==='demo')url.searchParams.set('intent','demo');a.href=url.href;});
