import {chromium} from 'file:///C:/Users/A/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {mkdir,writeFile,readdir,readFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const base=new URL('./',import.meta.url).pathname.replace(/^\/(\w:)/,'$1');
const out=new URL('./qa/proposal/',import.meta.url);await mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true,channel:'chrome'});const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(String(e)));const external=[];page.on('request',r=>{if(!r.url().startsWith('http://127.0.0.1:8790/'))external.push(r.url());});
const names=['index','services','projects','partners','creative','ai-agents','about','contact','krakenos'];
for(const name of names){await page.goto('http://127.0.0.1:8790/'+name+'.html');await page.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');await Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>i.decode().catch(()=>{})));});await page.screenshot({path:fileURLToPath(new URL(name+'-desktop.png',out)),fullPage:true});}
await page.setViewportSize({width:390,height:844});
for(const name of names){await page.goto('http://127.0.0.1:8790/'+name+'.html');await page.evaluate(async()=>{await document.fonts.ready;document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager');await Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>i.decode().catch(()=>{})));});await page.screenshot({path:fileURLToPath(new URL(name+'-mobile.png',out)),fullPage:true});}
await page.setViewportSize({width:1440,height:950});await page.goto('http://127.0.0.1:8790/');await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:fileURLToPath(new URL('preview-desktop.png',out))});await page.setViewportSize({width:390,height:844});await page.reload();await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:fileURLToPath(new URL('preview-mobile.png',out))});console.log(JSON.stringify({errors,external}));await browser.close();
