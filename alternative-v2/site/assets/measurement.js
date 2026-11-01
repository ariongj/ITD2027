'use strict';
(() => {
 const config=window.ITD_MEASUREMENT||{enabled:false},lang=document.documentElement.lang;
 const page=document.body.dataset.page,canonical=document.querySelector('link[rel=canonical]').href;
 const allowedEvents=new Set(['book_meeting','request_demo','click_whatsapp','click_phone','click_email']);
 const services={ 'web-software':['Web & softuer','Web & software','Web & Software','Faqe interneti & softuer','Websites & software','Websites & Software'], 'ai-automation':['AI automation','Automatizim me AI','KI-Automatisierung','AI Agents','KI-Agenten','Ari','Dita','Nora','Leo','Mira','Fin'], 'it-support':['IT & siguri','IT & security','IT & Sicherheit','Starter €99','Business €299','Enterprise €779'], creative:['Kreativa','Creative','Kreativ','Branding','Social Media','Video & Motion','Fushatë','Campaign','Kampagne'] };
 const products={'KrakenOS':'kraken-os','Kraken OS':'kraken-os','Kraken Assistant':'kraken-communications','Kraken Communications':'kraken-communications','AURA':'aura'};
 // Catalogue CTAs, sector chips and form options use many labels (in SQ/EN/DE), so after the exact lists
 // above, a selection is classified by keywords, then by the page it was sent from.
 const keywords=[['ai-automation',/\b(AI|KI)\b|automat|agent|\b(Ari|Dita|Nora|Leo|Mira|Fin)\b/i],['web-software',/web|softuer|software|aplikacion|application|applikation|sistem|system/i],['it-support',/\bIT\b|support|mbështetje|outsourc|jashtëm|extern|cyber|kibernet|siguri|sicherheit|audit/i],['creative',/brand|kreativ|creative|marketing|social|video|motion|fushat|campaign|kampagn|identit|foto|photo/i]];
 const pageService={'web-software':'web-software','ai-automation':'ai-automation','ai-agents':'ai-automation','creative':'creative'};
 function classify(selection){
  const s=String(selection||'').trim();
  const product=products[s]||(/^kraken\s?os\b/i.test(s)?'kraken-os':/^kraken communications\b/i.test(s)?'kraken-communications':/^aura\b/i.test(s)?'aura':'');
  const service=Object.keys(services).find(k=>services[k].includes(s))||(s&&(keywords.find(([,re])=>re.test(s))||[])[0])||pageService[page]||'';
  return {product,service};
 }
 const locale={
  sq:{title:'Privatësia dhe matja',text:'Me lejen tënde, Google Analytics mat vizitat dhe Google Ads mat nëse një kërkesë erdhi nga reklamat tona. Zgjidh çfarë lejon; mund ta ndryshosh kurdo te “Cilësimet e privatësisë”.',analytics:['Statistika (Google Analytics)','Faqet, gjuha dhe veprimet e kontaktit, pa emër, email, telefon apo mesazh.'],ads:['Reklama (Google Ads)','Sa kërkesa vijnë nga reklamat tona; nga formulari Google merr emailin ose telefonin vetëm të koduar (hash). Pa reklama të personalizuara.'],all:'Lejo të gjitha',save:'Ruaj zgjedhjen',none:'Refuzo të gjitha',settings:'Cilësimet e privatësisë'},
  en:{title:'Privacy and measurement',text:'With your permission, Google Analytics measures visits and Google Ads measures whether an enquiry came from our ads. Choose what you allow; you can change it at any time under “Privacy settings”.',analytics:['Statistics (Google Analytics)','Pages, language and contact actions, without names, emails, phone numbers or messages.'],ads:['Advertising (Google Ads)','How many enquiries come from our ads; from the form, Google receives your email or phone only in hashed form. No personalised advertising.'],all:'Allow all',save:'Save choice',none:'Reject all',settings:'Privacy settings'},
  de:{title:'Datenschutz und Messung',text:'Mit Ihrer Erlaubnis misst Google Analytics Besuche und Google Ads, ob eine Anfrage über unsere Anzeigen kam. Wählen Sie, was Sie erlauben; Sie können es jederzeit unter „Datenschutzeinstellungen“ ändern.',analytics:['Statistik (Google Analytics)','Seiten, Sprache und Kontaktaktionen, ohne Namen, E-Mail-Adressen, Telefonnummern oder Nachrichten.'],ads:['Werbung (Google Ads)','Wie viele Anfragen über unsere Anzeigen kommen; aus dem Formular erhält Google E-Mail oder Telefon nur gehasht. Keine personalisierte Werbung.'],all:'Alle erlauben',save:'Auswahl speichern',none:'Alle ablehnen',settings:'Datenschutzeinstellungen'}}[lang];
 // Google Consent Mode v2, basic mode: the Google tag (G-B0S3HLRPWD, which also carries the Google Ads destination
 // AW-18460710310) is not loaded at all until the visitor allows a category. Statistics sets analytics_storage;
 // advertising sets ad_storage and ad_user_data. ad_personalization always stays denied: the site measures enquiries
 // from ads and does no remarketing.
 const key='itd-consent-v2',legacy='itd-analytics-consent-v1';
 // The configured site, with or without "www." (the server redirects www to the bare domain; this keeps the
 // consent choice working even if a page is ever served on www).
 const site=u=>u.protocol+'//'+u.hostname.replace(/^www\./,'')+(u.port?':'+u.port:'');
 const enabled=config.enabled===true && site(location)===site(new URL(config.origin)) && navigator.doNotTrack!=='1';
 let choice=null,decided=false,loaded=false;
 if(enabled)try{
  const saved=JSON.parse(localStorage.getItem(key)||'null');
  if(saved&&typeof saved.analytics==='boolean'&&typeof saved.ads==='boolean'){choice={analytics:saved.analytics,ads:saved.ads};decided=true;}
  else if(localStorage.getItem(legacy)==='denied'){choice={analytics:false,ads:false};decided=true;}
  // An earlier "allow" covered Google Analytics only: it stays, and the panel asks again because advertising is new.
  else if(localStorage.getItem(legacy)==='granted')choice={analytics:true,ads:false};
 }catch{}
 // Of the address, only ad click and campaign parameters reach Google, so a visit from an ad can be attributed;
 // any other query parameter (a chosen service, for example) is never sent.
 const campaign=['gclid','gbraid','wbraid','gad_source','gad_campaignid','dclid','utm_source','utm_medium','utm_campaign','utm_term','utm_content','utm_id'];
 const carried=new URLSearchParams();
 for(const [k,v] of new URLSearchParams(location.search))if(campaign.includes(k)&&v&&v.length<=300&&!carried.has(k))carried.set(k,v);
 const query=carried.toString(),pageLocation=canonical+(query?'?'+query:'');
 const signals=c=>({analytics_storage:c.analytics?'granted':'denied',ad_storage:c.ads?'granted':'denied',ad_user_data:c.ads?'granted':'denied',ad_personalization:'denied'});
 function gtag(){window.gtag.apply(null,arguments);}
 function apply(){
  if(!enabled||!choice)return;
  // Statistics off: Google Analytics sends nothing (its documented opt-out), also while the tag runs for advertising.
  window['ga-disable-'+config.id]=!choice.analytics;
  if(loaded){gtag('consent','update',signals(choice));return;}
  if(!choice.analytics&&!choice.ads)return;
  loaded=true;
  window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments);};
  // The denied defaults come first, then the visitor's choice, then the tag configuration and the events.
  gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});
  gtag('set','ads_data_redaction',true);
  gtag('consent','update',signals(choice));
  gtag('js',new Date());
  gtag('config',config.id,{send_page_view:false,page_location:pageLocation,page_referrer:document.referrer?new URL(document.referrer).origin:'',allow_google_signals:false,allow_ad_personalization_signals:false});
  const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(config.id);document.head.append(s);
  // Without advertising consent the page view goes to Google Analytics only, so the Ads destination stays silent.
  gtag('event','page_view',{page_location:pageLocation,page_title:document.title,language:lang,...(choice.ads?{}:{send_to:config.id})});
 }
 function record(name,selection='',intent=''){
  if(!allowedEvents.has(name))return;
  if(name==='book_meeting'&&intent!=='calendly-confirmed')return;
  const {product,service}=classify(selection);
  if(name==='request_demo'&&(!product||intent!=='demo'))return;
  const data={language:lang,page,service:service||'general',product:product||'none'};
  // Local, non-persistent diagnostic signal. No visitor data or network request.
  document.dispatchEvent(new CustomEvent('itd:measurement',{detail:{name,...data}}));
  if(loaded&&choice.analytics)gtag('event',name,{...data,page_location:pageLocation,send_to:config.id});
 }
 // A lead counts once, and only after the form service has confirmed that it received the enquiry: site.js calls
 // this from its success branch with the id it generated for that one submission (Google Ads deduplicates on it too).
 const leads=new Set();
 function lead(id,selection=''){
  if(typeof id!=='string'||!id||leads.has(id))return;leads.add(id);
  const {product,service}=classify(selection);
  const data={form_name:'contact_form',form_location:location.pathname,language:lang,page,service:service||'general',product:product||'none'};
  document.dispatchEvent(new CustomEvent('itd:measurement',{detail:{name:'generate_lead',...data}}));
  if(!loaded)return;
  if(choice.analytics)gtag('event','generate_lead',{...data,page_location:pageLocation,send_to:config.id});
  if(choice.ads&&config.conversion)gtag('event','conversion',{send_to:config.conversion,transaction_id:id});
 }
 window.ITDTracking=Object.freeze({record,lead});
 document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a)return;const u=new URL(a.href);if(u.protocol==='tel:')record('click_phone');else if(u.protocol==='mailto:')record('click_email');else if(u.hostname==='wa.me')record('click_whatsapp');});
 // Until a choice is made, the ad click and campaign parameters travel with internal links (in the address only,
 // nothing is stored), so a visit from an ad can still be attributed when consent is given on a later page.
 if(enabled&&query)document.addEventListener('click',e=>{
  if(decided)return;const a=e.target.closest('a[href]');if(!a)return;const u=new URL(a.href,location.href);
  if(u.origin!==location.origin||(u.pathname===location.pathname&&u.hash)||/\.(?!html$)[a-z0-9]+$/i.test(u.pathname))return;
  for(const [k,v] of carried)if(!u.searchParams.has(k))u.searchParams.set(k,v);
  a.href=u.href;
 },true);
 // booking.js accepts confirmed events only from the active Calendly embed.
 if(enabled){
  const panel=document.createElement('section');panel.className='consent-panel';panel.setAttribute('aria-labelledby','consent-title');panel.hidden=true;
  const title=document.createElement('h2');title.id='consent-title';title.textContent=locale.title;const p=document.createElement('p');p.textContent=locale.text;
  const options=document.createElement('div');options.className='consent-options';const boxes={};
  for(const name of ['analytics','ads']){
   const row=document.createElement('label');row.className='consent-option';
   const box=document.createElement('input');box.type='checkbox';box.name=name;boxes[name]=box;
   const text=document.createElement('span'),strong=document.createElement('strong'),note=document.createElement('small');
   [strong.textContent,note.textContent]=locale[name];text.append(strong,note);row.append(box,text);options.append(row);
  }
  const actions=document.createElement('div');actions.className='actions';const settings=document.createElement('button');
  function save(next){
   choice=next;decided=true;
   try{localStorage.setItem(key,JSON.stringify({analytics:next.analytics,ads:next.ads,date:new Date().toISOString().slice(0,10)}));localStorage.removeItem(legacy);}catch{}
   apply();
   // Withdrawing a category also removes the cookies it had set on this domain.
   for(const cookie of document.cookie.split(';')){const name=cookie.trim().split('=')[0];if((!next.analytics&&name.startsWith('_ga'))||(!next.ads&&name.startsWith('_gcl_'))){for(const domain of ['',location.hostname,'.'+location.hostname])document.cookie=name+'=; Max-Age=0; Path=/'+(domain?'; Domain='+domain:'')+'; SameSite=Lax';}}
   panel.hidden=true;settings.focus();
  }
  for(const [label,kind] of [[locale.all,'all'],[locale.none,'none'],[locale.save,'save']]){
   const b=document.createElement('button');b.type='button';b.className='button'+(kind==='all'?'':' outline');b.dataset.consent=kind;b.textContent=label;
   b.onclick=()=>save(kind==='all'?{analytics:true,ads:true}:kind==='none'?{analytics:false,ads:false}:{analytics:boxes.analytics.checked,ads:boxes.ads.checked});
   actions.append(b);
  }
  panel.append(title,p,options,actions);document.body.append(panel);
  const open=()=>{boxes.analytics.checked=!!choice?.analytics;boxes.ads.checked=!!choice?.ads;panel.hidden=false;};
  settings.type='button';settings.className='consent-settings';settings.textContent=locale.settings;settings.onclick=()=>{open();boxes.analytics.focus();};document.querySelector('.footer-bottom').append(settings);
  if(!decided)open();
 }
 apply();
})();
