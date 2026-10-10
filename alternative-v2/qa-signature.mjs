import {chromium} from 'file:///C:/Users/A/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.mjs';
import {writeFile,readFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const root=dirname(fileURLToPath(import.meta.url)),base='http://127.0.0.1:8790';
const browser=await chromium.launch({headless:true,channel:'chrome'});
const context=await browser.newContext({reducedMotion:'reduce'});
const page=await context.newPage();
const checks=[];
for(const lang of ['sq','en','de']){
 const path='index'+(lang==='sq'?'':'-'+lang)+'.html';
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:900});await page.goto(base+'/'+path);
  for(let i=0;i<3;i++){
   await page.locator('[role=tab]').nth(i).click();
   assert.equal(await page.locator('[role=tabpanel]:visible').count(),1);
   assert.equal(await page.locator('[role=tab]').nth(i).getAttribute('aria-selected'),'true');
   assert.equal(await page.locator('[role=tabpanel]:visible a').getAttribute('href'),'services'+(lang==='sq'?'':'-'+lang)+'.html#'+['presence','operations','support'][i]);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);
   checks.push({lang,width,panel:i,verified:true});
  }
  await page.locator('[role=tab]').first().focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('[role=tab]').nth(1).evaluate(e=>e===document.activeElement),true);
  await page.keyboard.press('End');assert.equal(await page.locator('[role=tab]').nth(2).getAttribute('aria-selected'),'true');
  await page.keyboard.press('Home');assert.equal(await page.locator('[role=tab]').first().getAttribute('aria-selected'),'true');
  if([1440,390].includes(width)){await page.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0)});await page.screenshot({path:resolve(root,'qa/signature-'+lang+'-'+width+'.png'),fullPage:true});}
 }
}
await page.setViewportSize({width:390,height:844});await page.goto(base+'/index.html');await page.locator('[data-lightbox]').first().click();
await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.closest('dialog')!==null),true);
await page.keyboard.press('Shift+Tab');assert.equal(await page.evaluate(()=>document.activeElement.closest('dialog')!==null),true);
await page.keyboard.press('Escape');
await page.goto(base+'/contact.html');await page.locator('[name=name]').fill('Draft test');await page.locator('[name=email]').fill('preview@example.invalid');await page.locator('[name=message]').fill('Keep my text across a language change.');
await page.locator('.languages [lang=en]').click();assert.equal(await page.locator('[name=message]').inputValue(),'Keep my text across a language change.');
await page.locator('#brief-form button').click();
await page.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('Denied for QA'))}})});
await page.locator('#copy-draft').click();await page.waitForFunction(()=>document.querySelector('#copy-status').textContent.length>0);
assert.match(await page.locator('#copy-status').textContent(),/not allowed/);
const sourceManifest=JSON.parse(await readFile(resolve(root,'source-manifest.json'),'utf8'));
const changed=[];
for(const [name,expected] of Object.entries(sourceManifest)){
 const actual=createHash('sha256').update(await readFile(resolve(root,'..',name))).digest('hex');if(actual!==expected)changed.push(name);
}
// chat.php changed outside this preview during the session; retain the initial baseline and report the difference.
assert.deepEqual(changed.filter(name=>name!=='chat.php'),[]);
const originalLogo=await readFile(resolve(root,'../logo-lockup-tight-480.png'));
const previewLogo=await readFile(resolve(root,'site/assets/brand/logo-original.png'));
assert.equal(createHash('sha256').update(previewLogo).digest('hex'),createHash('sha256').update(originalLogo).digest('hex'));
const htmlFiles=(await readdir(resolve(root,'site'))).filter(n=>n.endsWith('.html'));
for(const name of htmlFiles){
 const html=await readFile(resolve(root,'site',name),'utf8');
 assert.equal((html.match(/src="assets\/brand\/logo-original.png"/g)||[]).length,2,name+' original header and footer logo');
 assert.ok(!/shield-sculpture|signature-art|logo-shield.png/.test(html),name+' has no replacement logo');
}
await page.goto(base+'/index.html');await page.evaluate(()=>document.fonts.ready);
assert.equal(await page.evaluate(()=>document.fonts.check('600 16px Manrope')),true);
const fontResponse=await page.request.get(base+'/assets/fonts/manrope-latin-wght-normal.woff2');assert.equal(fontResponse.status(),200);assert.match(fontResponse.headers()['content-type'],/font\/woff2/);
const report={logoVerified:true,logoPages:htmlFiles.length,time:new Date().toISOString(),servicePanels:checks.length,checks,extra:['Arrow navigation','Home and End navigation','modal focus trap','language switch preserves draft','clipboard rejection fallback'],sourceFilesUnchanged:Object.keys(sourceManifest).length-changed.length,originalChanged:changed};
await writeFile(resolve(root,'qa/signature-report.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({servicePanelLayouts:checks.length,extra:report.extra,sourceFilesUnchanged:report.sourceFilesUnchanged,originalChanged:changed}));
await browser.close();


