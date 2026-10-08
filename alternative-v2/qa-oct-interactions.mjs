import {chromium} from 'file:///C:/Users/A/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {writeFile} from 'node:fs/promises';import assert from 'node:assert/strict';
const b=await chromium.launch({headless:true,channel:'chrome'});const c=await b.newContext({viewport:{width:1440,height:900},reducedMotion:'reduce'});const p=await c.newPage();const results=[],errors=[];p.on('pageerror',e=>errors.push(String(e)));p.setDefaultTimeout(8000);const base='http://127.0.0.1:8791/';const check=(n,v)=>{assert(v,n);results.push(n);};
for(const lang of ['sq','en','de'])for(const width of [1440,390,320]){
 await p.setViewportSize({width,height:844});await p.goto(base+'itd-labs'+(lang==='sq'?'':'-'+lang)+'.html');await p.evaluate(()=>document.fonts.ready);
 check(lang+width+' single font',await p.locator('h1').evaluate(e=>getComputedStyle(e).fontFamily.includes('Plus Jakarta Sans')));
 check(lang+width+' product order',JSON.stringify(await p.locator('[data-product]').evaluateAll(es=>es.map(e=>e.dataset.product)))===JSON.stringify(['krakenos','kraken-communications','aura']));
 check(lang+width+' AURA product link',(await p.locator('[data-product=aura] a').getAttribute('href'))==='aura'+(lang==='sq'?'':'-'+lang)+'.html');
 if(width<1121)await p.locator('.menu-toggle').click();
 await p.locator('.labs-toggle').click();check(lang+width+' Labs opens',await p.locator('#labs-menu').isVisible());check(lang+width+' four links',await p.locator('#labs-menu a').count()===4);
 check(lang+width+' menu contained',await p.locator('#labs-menu').evaluate(e=>e.getBoundingClientRect().right<=innerWidth));
 await p.keyboard.press('Escape');check(lang+width+' Labs Escape restores',await p.locator('.labs-toggle').evaluate(e=>e===document.activeElement)&&await p.locator('#labs-menu').isHidden());
 if(width<1121){check(lang+width+' parent stays open',await p.locator('.menu-toggle').getAttribute('aria-expanded')==='true');await p.keyboard.press('Escape');check(lang+width+' parent closes',await p.locator('.menu-toggle').getAttribute('aria-expanded')==='false');}
 await p.locator(width<1121?'.menu-toggle':'.labs-toggle').click();if(width<1121)await p.locator('.labs-toggle').click();await p.locator('#labs-menu a').nth(2).click();check(lang+width+' Communications navigation',await p.locator('body').getAttribute('data-page')==='kraken-communications');
}
let success=false,requests=0;await p.route('https://formspree.io/**',r=>{requests++;return r.fulfill({status:success?200:503,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify({ok:success})});});
for(const lang of ['sq','en','de']){
 await p.goto(base+'contact'+(lang==='sq'?'':'-'+lang)+'.html?service=Kraken%20Communications&intent=demo');
 await p.evaluate(()=>{window.testEvents=[];document.addEventListener('itd:measurement',e=>testEvents.push(e.detail));});
 await p.locator('[name=name]').fill('Private QA Name');await p.locator('[name=email]').fill('private@example.invalid');await p.locator('[name=message]').fill('Private QA message');success=false;await p.locator('[type=submit]').click();await p.waitForFunction(()=>document.querySelector('.form-status').dataset.state==='error');check(lang+' no failure conversion',await p.evaluate(()=>testEvents.length===0));
 success=true;await p.locator('[type=submit]').click();await p.waitForFunction(()=>document.querySelector('.form-status').dataset.state==='success');const events=await p.evaluate(()=>testEvents);
 check(lang+' confirmed lead and demo',events.map(e=>e.name).join(',')==='generate_lead,request_demo');check(lang+' metadata',events.every(e=>e.language===lang&&e.product==='kraken-communications'));check(lang+' no personal data',!JSON.stringify(events).includes('Private')&&!JSON.stringify(events).includes('@'));
 await p.evaluate(()=>{document.addEventListener('click',e=>{if(e.target.closest('a'))e.preventDefault();},{capture:true});for(const sel of ['a[href^="mailto:"]','a[href^="tel:"]','a[href*="wa.me"]'])document.querySelector(sel).click();});
 const names=await p.evaluate(()=>testEvents.map(e=>e.name));check(lang+' contact click events',names.slice(2).join(',')==='click_email,click_phone,click_whatsapp');check(lang+' no false booking',!names.includes('book_meeting'));
 check(lang+' preview analytics disabled',await p.evaluate(()=>window.ITD_MEASUREMENT.enabled===false&&!window.gtag));
}
// Consent behavior tested using intercepted tag bootstrap; nothing reaches Google.
const consent=await b.newContext({bypassCSP:true});const q=await consent.newPage();let tags=0;
await q.route('**/measurement-config.js',r=>r.fulfill({contentType:'application/javascript',body:'window.ITD_MEASUREMENT={enabled:true,id:"G-B0S3HLRPWD",origin:"http://127.0.0.1:8791"}'}));
await q.route('https://www.googletagmanager.com/**',r=>{tags++;return r.fulfill({contentType:'application/javascript',body:'/* Intercepted QA tag; no collection. */'});});
await q.goto(base+'contact.html?service=private@example.invalid');check('no analytics before consent',tags===0);await q.locator('.consent-panel button').last().click();check('denied no tag',tags===0);await q.reload();check('denial persists',await q.locator('.consent-panel').isHidden());await q.locator('.consent-settings').click();await q.locator('.consent-panel button').first().click();await q.waitForFunction(()=>window.dataLayer?.length>0);await q.waitForLoadState('networkidle');check('consent loads one tag',tags===1);
const layer=await q.evaluate(()=>dataLayer.map(a=>Array.from(a)));check('no query in analytics',!JSON.stringify(layer).includes('private@example.invalid'));await q.locator('.consent-settings').click();await q.locator('.consent-panel button').last().click();check('revocation disables GA',await q.evaluate(()=>window['ga-disable-G-B0S3HLRPWD']===true));
await q.locator('.consent-settings').click();await q.locator('.consent-panel button').first().click();check('renewed consent enables GA',await q.evaluate(()=>window['ga-disable-G-B0S3HLRPWD']===false));check('renewed consent does not duplicate tag',tags===1);
await writeFile('alternative-v2/qa/proposal/october-interactions.json',JSON.stringify({checks:results.length,results,errors,requests,realProviderCalls:0},null,2));console.log(JSON.stringify({checks:results.length,errors,interceptedForms:requests,interceptedTags:tags}));await b.close();
