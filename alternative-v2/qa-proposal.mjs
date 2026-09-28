import {chromium} from 'file:///C:/Users/A/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {readdir,readFile,writeFile} from 'node:fs/promises';import {createHash} from 'node:crypto';import {fileURLToPath} from 'node:url';
const root=new URL('./',import.meta.url),site=new URL('./site/',root),origin='http://127.0.0.1:8790/';const report={routes:[],layouts:[],interactions:[],errors:[],external:[],logoHashes:[],sourceChanges:[]};
const browser=await chromium.launch({headless:true,channel:'chrome'});const page=await browser.newPage();page.on('pageerror',e=>report.errors.push(String(e)));page.on('request',r=>{if(!r.url().startsWith(origin))report.external.push(r.url());});const targets=new Set();
const files=(await readdir(site)).filter(f=>f.endsWith('.html'));
for(const width of [1440,768,390,320]){
 await page.setViewportSize({width,height:900});
 for(const file of files){
  const response=await page.goto(origin+file);await page.evaluate(()=>document.fonts.ready);
  const state=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,h1:document.querySelectorAll('h1').length,title:document.title,lang:document.documentElement.lang,broken:[...document.images].filter(i=>i.complete&&i.getAttribute('src')&&!i.naturalWidth).map(i=>i.getAttribute('src')),overflow:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left< -1)&&getComputedStyle(e).position!=='fixed';}).slice(0,6).map(e=>({tag:e.tagName,cls:e.className,right:e.getBoundingClientRect().right,left:e.getBoundingClientRect().left})),links:[...document.querySelectorAll('a[href],img[src],script[src],link[href]')].map(e=>e.href||e.src).filter(Boolean),logo:document.querySelector('.brand img').getAttribute('src')}));
  report.layouts.push({file,width,overflow:state.scroll>width+1,offenders:state.scroll>width+1?state.overflow:[],broken:state.broken});
  if(width===1440){report.routes.push({file,status:response.status(),h1:state.h1,lang:state.lang,title:state.title,logo:state.logo});state.links.forEach(url=>{if(url.startsWith(origin))targets.add(url);});}
 }
 console.log('Checked width '+width);
}
for(const url of targets){const u=new URL(url);const response=await page.request.get(url);if(response.status()!==200)report.errors.push('Local target failed '+url+' '+response.status());if(u.hash&&u.pathname.endsWith('.html')){const html=await response.text();const hash=decodeURIComponent(u.hash.slice(1));if(!html.includes('id="'+hash+'"'))report.errors.push('Anchor missing '+url);}}
const hashes=async(path)=>createHash('sha256').update(await readFile(path)).digest('hex');
for(const [src,dst] of [['logo-lockup-tight-480.png','logo-original.png'],['logo-lockup-creative-480.png','logo-creative.png'],['logo-lockup-ai-480.png','logo-ai.png']])report.logoHashes.push({file:src,equal:await hashes(new URL('../'+src,root))===await hashes(new URL('assets/brand/'+dst,site))});
const baseline=JSON.parse(await readFile(new URL('proposal-source-manifest.json',root),'utf8'));for(const [file,hash] of Object.entries(baseline))if(await hashes(new URL('../'+file,root))!==hash)report.sourceChanges.push(file);
await writeFile(new URL('qa/proposal/route-report.json',root),JSON.stringify(report,null,2));console.log(JSON.stringify({routes:report.routes.length,layouts:report.layouts.length,overflow:report.layouts.filter(x=>x.overflow),broken:report.layouts.filter(x=>x.broken.length),errors:report.errors,external:[...new Set(report.external)],logoHashes:report.logoHashes,sourceChanges:report.sourceChanges}));await browser.close();
