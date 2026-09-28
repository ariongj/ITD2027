import { chromium } from 'file:///C:/Users/A/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {readdir,writeFile,readFile} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url));
const base='http://127.0.0.1:8790';
const pages=(await readdir(resolve(root,'site'))).filter(n=>n.endsWith('.html'));
const browser=await chromium.launch({headless:true,channel:"chrome"});
const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce',permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage();
const failures=[],errors=[],external=[],checks=[],shots=[];
page.on('pageerror',e=>errors.push(e.message));
page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
await context.route('**/*',route=>{if(!route.request().url().startsWith(base)){external.push(route.request().url());return route.abort();}return route.continue();});
const localLinks=new Set();
for(const file of pages){
 await page.goto(base+'/'+file);
 await page.locator('body').waitFor();
 const d=await page.evaluate(()=>({
  h1:document.querySelectorAll('h1').length,
  emptyHeadings:[...document.querySelectorAll('h1,h2,h3')].filter(e=>!e.textContent.trim()).length,
  links:[...document.querySelectorAll('a[href],link[href],script[src],img[src]')].map(e=>e.href||e.src),
  duplicateIDs:[...document.querySelectorAll('[id]')].map(e=>e.id).filter((x,i,a)=>a.indexOf(x)!==i),
  brokenImages:[...document.images].filter(e=>e.getAttribute('src')&&e.complete&&!e.naturalWidth).map(e=>e.src),
  details:document.querySelectorAll('details').length
 }));
 if(d.h1!==1||d.emptyHeadings||d.duplicateIDs.length||d.brokenImages.length)failures.push({file,semantics:d});
 for(const link of d.links)if(link?.startsWith(base))localLinks.add(link);
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:width===1440?1000:844});
  const over=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,items:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return getComputedStyle(e).display!=='none'&&r.width>0&&(r.right>innerWidth+1||r.left< -1)&&!e.closest('dialog')&&e.className!=='skip';}).map(e=>e.tagName+'.'+e.className).slice(0,12)}));
  if(over.scroll>width+1)failures.push({file,overflow:over});
  checks.push({file,width,overflow:over.scroll>width+1});
 }
 if(!file.includes('-en')&&!file.includes('-de')){
  for(const width of [1440,390]){
   await page.setViewportSize({width,height:width===1440?1000:844});
   const shot='qa/'+file.replace('.html','')+'-'+width+'.png';
   await page.screenshot({path:resolve(root,shot),fullPage:true});
   shots.push(shot);
  }
 }
}
for(const href of localLinks){
 const url=new URL(href);const response=await context.request.get(url.origin+url.pathname);
 if(response.status()!==200)failures.push({href,status:response.status()});
 if(url.hash&&url.pathname.endsWith('.html')){
  const body=await response.text();const id=decodeURIComponent(url.hash.slice(1));
  if(!body.includes('id="'+id+'"'))failures.push({href,missingAnchor:id});
 }
}
const homeRoute=base+'/index.html';
await page.setViewportSize({width:390,height:844});
await page.goto(homeRoute);
await page.locator('.menu-toggle').click();assert.equal(await page.locator('#mobile-nav').isVisible(),true);
await page.keyboard.press('Escape');assert.equal(await page.locator('#mobile-nav').isVisible(),false);assert.equal(await page.locator('.menu-toggle').evaluate(e=>e===document.activeElement),true);
await page.locator('.menu-toggle').click();await page.locator('#mobile-nav a').first().click();assert.match(page.url(),/services/);
await page.locator('.service-detail summary').first().click();assert.equal(await page.locator('.service-detail').first().getAttribute('open'),'');
await page.locator('.service-detail .text-link').first().click();assert.ok(await page.locator('select').inputValue());
await page.locator('#brief-form button').click();assert.equal(await page.locator('#draft-result').isVisible(),false);
await page.locator('[name=name]').fill('Test User');
await page.locator('[name=email]').fill('review@example.invalid');
await page.locator('[name=message]').fill('Preview QA only. No message should be sent. <script>alert(1)</script>');
await page.locator('#brief-form button').click();assert.equal(await page.locator('#draft-result').isVisible(),true);
const draft=await page.locator('#draft-text').textContent();
assert.match(draft,/<script>alert\(1\)<\/script>/);
assert.equal(await page.locator('#draft-text script').count(),0);
assert.match(await page.locator('#draft-email').getAttribute('href'),/^mailto:info@itdks.tech/);
const whats=new URL(await page.locator('#draft-whatsapp').getAttribute('href'));assert.equal(whats.hostname,'wa.me');assert.equal(whats.searchParams.get('text'),draft);
await page.locator('#copy-draft').click();await page.waitForFunction(()=>document.querySelector('#copy-status').textContent.length>0);assert.equal((await page.evaluate(()=>navigator.clipboard.readText())).replaceAll("\r\n","\n"),draft);
await page.locator('#edit-draft').click();assert.match(await page.locator('[name=message]').inputValue(),/Preview QA/);
await page.reload();assert.match(await page.locator('[name=message]').inputValue(),/Preview QA/);assert.equal(await page.locator('[name=name]').inputValue(),'Test User');
await page.locator('[name=message]').fill('   ');await page.locator('#brief-form button').click();assert.equal(await page.locator('#draft-result').isVisible(),false);
await page.goto(homeRoute);
const opener=page.locator('[data-lightbox]').first();await opener.click();assert.equal(await page.locator('dialog').isVisible(),true);assert.equal(await page.locator('body').evaluate(e=>getComputedStyle(e).overflow),'hidden');
await page.screenshot({path:resolve(root,'qa/lightbox-mobile.png')});
await page.keyboard.press('Escape');assert.equal(await page.locator('dialog').isVisible(),false);assert.equal(await opener.evaluate(e=>e===document.activeElement),true);
await page.goto(base+'/services-de.html');await page.locator('.price-card .text-link').nth(1).click();assert.equal(await page.locator('select').inputValue(),'Business €299');
await page.locator('.languages a[lang=en]').click();assert.match(page.url(),/contact-en.html/);assert.equal(await page.locator('html').getAttribute('lang'),'en');
const notfound=await context.request.get(base+'/missing-page');assert.equal(notfound.status(),404);
for(const path of ['/.env.local','/../build.py','/build.py','/assets/../../source-manifest.json']){const r=await context.request.get(base+path);assert.equal(r.status(),404);}
await page.setViewportSize({width:1440,height:1000});await page.goto(homeRoute);await page.screenshot({path:resolve(root,'qa/home-desktop-viewport.png')});
await page.setViewportSize({width:390,height:844});await page.screenshot({path:resolve(root,'qa/home-mobile-viewport.png')});
await writeFile(resolve(root,'qa/report.json'),JSON.stringify({time:new Date().toISOString(),pages:pages.length,layouts:checks.length,links:localLinks.size,failures,errors,external,shots,flows:['mobile menu and Escape focus','service accordion and query handoff','required fields','whitespace rejection','literal user text','email draft encoding','WhatsApp draft encoding','clipboard copy','edit preserves text','draft survives reload','portfolio dialog and scroll lock','dialog Escape focus restoration','package handoff','language continuity','404','private path denial']},null,2));
console.log(JSON.stringify({pages:pages.length,layouts:checks.length,links:localLinks.size,failures,errors,external,flows:'passed'},null,2));
await browser.close();
if(failures.length||errors.length||external.length)process.exitCode=1;



