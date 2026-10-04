"""Check both preview and isolated production SEO output without publishing."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET,hashlib,runpy,os,csv
BASE=Path(__file__).resolve().parent
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__();self.canonical=[];self.alt={};self.robots='';self.title='';self.desc='';self.h1=0;self.lang='';self.refs=[];self.in_title=False;self.feed(path.read_text(encoding='utf-8-sig'))
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if tag=='title':self.in_title=True
  if tag=='h1':self.h1+=1
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='link' and a.get('rel')=='alternate':self.alt[a['hreflang']]=a['href']
  if tag=='meta' and a.get('name')=='robots':self.robots=a['content']
  if tag=='meta' and a.get('name')=='description':self.desc=a['content']
  for k in ['src','href']:
   if k in a:self.refs.append(a[k])
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
 def handle_data(self,s):
  if self.in_title:self.title+=s
results=[]
for production in [False,True]:
 os.environ['ITD_INDEXABLE']='1'
 os.environ['ITD_PRODUCTION']='1' if production else '0';os.environ['ITD_SITE_URL']='https://itdks.tech' if production else 'https://ariongj.github.io/ITD2027';os.environ['ITD_ANALYTICS']='1' if production else '0'
 runpy.run_path(str(BASE/'build.py'),run_name='__main__')
 root=BASE/('qa/production' if production else 'site');pages={p.name:Page(p) for p in root.glob('*.html')};assert len(pages)==51
 urls=[e.find('{*}loc').text for e in ET.parse(root/'sitemap.xml').getroot()];assert len(urls)==48 and len(set(urls))==48
 titles=[];canonical=set()
 for name,p in pages.items():
  assert p.h1==1 and p.desc and len(p.canonical)==1,name
  titles.append(p.title);canonical.add(p.canonical[0]);assert set(p.alt)=={'sq','en','de','x-default'},name
  assert p.canonical[0]==p.alt[p.lang],name
  assert p.canonical[0].startswith(os.environ['ITD_SITE_URL']+'/'),name
  assert ('noindex' in p.robots)==(not production or name.startswith('404')),name
  if not name.startswith('404'):assert p.canonical[0] in urls,name
  for ref in p.refs:
   u=urlsplit(ref)
   if u.scheme or u.netloc:continue
   target=unquote(u.path)
   if not target:continue
   if production and target in ['./','en','de']:target={'./':'index.html','en':'index-en.html','de':'index-de.html'}[target]
   elif production and '.' not in Path(target).name:target+='.html'
   assert (root/target).is_file(),(name,ref)
 assert len(canonical)==51
 assert len(set(titles))==51 # Every page has a distinct, translated title.
 for name,source in [('logo-original.png','logo-lockup-tight-480.png'),('logo-creative.png','logo-lockup-creative-480.png'),('logo-ai.png','logo-lockup-ai-480.png')]:assert (root/'assets/brand'/name).read_bytes()==(BASE.parent/source).read_bytes()
 results.append({'mode':'production' if production else 'preview','pages':len(pages),'sitemap':len(urls),'unique_canonicals':len(canonical),'errors':[]})
# Current sitemap inventory: stable URLs are retained in the production site.
# The public live sitemap snapshot is tracked (seo-live-sitemap.xml); reference/ is private and git-ignored.
# Without it the inventory would silently shrink, so stop before writing anything.
live=next((p for p in [BASE/'seo-live-sitemap.xml',BASE/'reference/20261003/live-sitemap.xml'] if p.exists()),None);inventory=[]
if live is None: raise SystemExit('seo-live-sitemap.xml is missing: the URL inventory cannot be checked, seo-url-map.csv was not changed.')
for u in ET.parse(live).getroot().findall('{*}url'):
 url=u.find('{*}loc').text;inventory.append({'old_url':url,'new_url':url,'action':'retained' if url in urls else 'review_required'})
for old,new in [('https://itdks.tech/index-en.html','https://itdks.tech/en'),('https://itdks.tech/creative.html','https://itdks.tech/creative'),('https://itdks.tech/index','https://itdks.tech/'),('https://itdks.tech/index-en','https://itdks.tech/en'),('https://itdks.tech/index-de','https://itdks.tech/de')]:inventory.append({'old_url':old,'new_url':new,'action':'existing_301_retained'})
inventory += [{'old_url':'https://itdks.tech/teams/','new_url':'','action':'retain_404_no_equivalent_provided'},{'old_url':'https://itdks.tech/?optech_footer=footer','new_url':'https://itdks.tech/','action':'prepared_301_remove_legacy_parameter'}]
assert not any(r['action']=='review_required' for r in inventory),inventory
with (BASE/'seo-url-map.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=['old_url','new_url','action']);w.writeheader();w.writerows(inventory)
(BASE/'qa/proposal').mkdir(parents=True,exist_ok=True)
(BASE/'qa/proposal/seo-report.json').write_text(json.dumps({'builds':results,'inventory':inventory,'live_redirects':'prepared; Apache deployment not performed'},indent=2),encoding='utf-8')
print(json.dumps(results));print('All '+str(len(inventory))+' inventoried URLs mapped without a blanket homepage redirect.')
