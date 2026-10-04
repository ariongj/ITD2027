'use strict';
(() => {
 const config=window.ITD_MEASUREMENT||{enabled:false},lang=document.documentElement.lang;
 const page=document.body.dataset.page,canonical=document.querySelector('link[rel=canonical]').href;
 const allowedEvents=new Set(['book_meeting','generate_lead','request_demo','click_whatsapp','click_phone','click_email']);
 const services={ 'web-software':['Web & softuer','Web & software','Web & Software','Faqe interneti & softuer','Websites & software','Websites & Software'], 'ai-automation':['AI automation','Automatizim me AI','KI-Automatisierung','AI Agents','KI-Agenten','Ari','Dita','Nora','Leo','Mira','Fin'], 'it-support':['IT & siguri','IT & security','IT & Sicherheit','Starter €99','Business €299','Enterprise €779'], creative:['Kreativa','Creative','Kreativ','Branding','Social Media','Video & Motion','Fushatë','Campaign','Kampagne'] };
 const products={'KrakenOS':'kraken-os','Kraken OS':'kraken-os','Kraken Communications':'kraken-communications'};
 // Catalogue CTAs, sector chips and form options use many labels (in SQ/EN/DE), so after the exact lists
 // above, a selection is classified by keywords, then by the page it was sent from.
 const keywords=[['ai-automation',/\b(AI|KI)\b|automat|agent|\b(Ari|Dita|Nora|Leo|Mira|Fin)\b/i],['web-software',/web|softuer|software|aplikacion|application|applikation|sistem|system/i],['it-support',/\bIT\b|support|mbështetje|outsourc|jashtëm|extern|cyber|kibernet|siguri|sicherheit|audit/i],['creative',/brand|kreativ|creative|marketing|social|video|motion|fushat|campaign|kampagn|identit|foto|photo/i]];
 const pageService={'web-software':'web-software','ai-automation':'ai-automation','ai-agents':'ai-automation','creative':'creative'};
 function classify(selection){
  const s=String(selection||'').trim();
  const product=products[s]||(/^kraken\s?os\b/i.test(s)?'kraken-os':/^kraken communications\b/i.test(s)?'kraken-communications':'');
  const service=Object.keys(services).find(k=>services[k].includes(s))||(s&&(keywords.find(([,re])=>re.test(s))||[])[0])||pageService[page]||'';
  return {product,service};
 }
 const locale={sq:['Matja e vizitave','Me lejen tënde, Google Analytics mat vizitat dhe veprimet e kontaktit. Emri, emaili, telefoni dhe mesazhi nuk përfshihen në eventet tona.','Lejo matjen','Pa analytics','Cilësimet e privatësisë'],en:['Visit measurement','With your permission, Google Analytics measures visits and contact actions. Names, emails, phone numbers and messages are excluded from our events.','Allow analytics','No analytics','Privacy settings'],de:['Besuchsmessung','Mit Ihrer Erlaubnis misst Google Analytics Besuche und Kontaktaktionen. Namen, E-Mails, Telefonnummern und Nachrichten werden nicht in unsere Ereignisse aufgenommen.','Analytics erlauben','Ohne Analytics','Datenschutzeinstellungen']}[lang];
 let consent=false,loaded=false;const key='itd-analytics-consent-v1';
 const enabled=config.enabled===true && location.origin===new URL(config.origin).origin && navigator.doNotTrack!=='1';
 try{consent=enabled && localStorage.getItem(key)==='granted';}catch{}
 function start(){
  if(!consent||!enabled)return;
  window['ga-disable-'+config.id]=false;
  if(loaded){gtag('consent','update',{analytics_storage:'granted'});return;}loaded=true;
  window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments);};
  gtag('consent','default',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
  gtag('js',new Date());gtag('config',config.id,{send_page_view:false,page_location:canonical,page_referrer:document.referrer?new URL(document.referrer).origin:'',allow_google_signals:false,allow_ad_personalization_signals:false});
  const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(config.id);document.head.append(s);
  gtag('event','page_view',{page_location:canonical,page_title:document.title,language:lang});
 }
 function record(name,selection='',intent=''){
  if(!allowedEvents.has(name))return;
  if(name==='book_meeting'&&intent!=='calendly-confirmed')return;
  const {product,service}=classify(selection);
  if(name==='request_demo'&&(!product||intent!=='demo'))return;
  const data={language:lang,page,service:service||'general',product:product||'none'};
  // Local, non-persistent diagnostic signal. No visitor data or network request.
  document.dispatchEvent(new CustomEvent('itd:measurement',{detail:{name,...data}}));
  if(enabled&&consent&&loaded)gtag('event',name,{...data,page_location:canonical});
 }
 window.ITDTracking=Object.freeze({record});
 document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a)return;const u=new URL(a.href);if(u.protocol==='tel:')record('click_phone');else if(u.protocol==='mailto:')record('click_email');else if(u.hostname==='wa.me')record('click_whatsapp');});
 // booking.js accepts confirmed events only from the active Calendly embed.
 if(enabled){
  const panel=document.createElement('section');panel.className='consent-panel';panel.setAttribute('aria-labelledby','consent-title');panel.hidden=true;
  const title=document.createElement('h2');title.id='consent-title';title.textContent=locale[0];const p=document.createElement('p');p.textContent=locale[1];
  const actions=document.createElement('div');actions.className='actions';
  for(const [label,value] of [[locale[2],true],[locale[3],false]]){const b=document.createElement('button');b.type='button';b.className='button'+(value?'':' outline');b.textContent=label;b.onclick=()=>{consent=value;try{localStorage.setItem(key,value?'granted':'denied');}catch{}if(value)start();else{window['ga-disable-'+config.id]=true;if(window.gtag)gtag('consent','update',{analytics_storage:'denied'});for(const cookie of document.cookie.split(';')){const name=cookie.trim().split('=')[0];if(name.startsWith('_ga')){for(const domain of ['',location.hostname,'.'+location.hostname])document.cookie=name+'=; Max-Age=0; Path=/'+(domain?'; Domain='+domain:'')+'; SameSite=Lax';}}}panel.hidden=true;settings.focus();};actions.append(b);}
  panel.append(title,p,actions);document.body.append(panel);
  const settings=document.createElement('button');settings.type='button';settings.className='consent-settings';settings.textContent=locale[4];settings.onclick=()=>{panel.hidden=false;panel.querySelector('button').focus();};document.querySelector('.footer-bottom').append(settings);
  try{panel.hidden=localStorage.getItem(key)!==null;}catch{panel.hidden=false;}
 }
 start();
})();
