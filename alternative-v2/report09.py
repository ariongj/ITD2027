"""Change report 09 (19 October 2026): the last changes before going live, main version only.

The home orbit turns every 2.5 s without a countdown (orbit.js, report08.py). On ITD Labs, the AURA box's emblem
moves as in the AURA app's active state, and "Consider it handled." is typed letter by letter under the static
"Say it." (assets/aura-live.js, assets/report09.css). The title, text, button and layout of the box stay as they are;
the Labs hero and catalogue are unchanged."""
_r8_labs=labs

# The emblem as inline SVG from the original geometry (the three ribbons of assets/labs/aura-emblem.svg, which is
# the static rebuild of the AURA app's drawing), so each ribbon can turn on its own and the lines stay sharp.
def aura_live_svg():
 src=(OUT/'assets/labs/aura-emblem.svg').read_text(encoding='utf-8')
 paths=re.findall(r'<path d="([^"]+)" stroke="url\(#(auraPink|auraTeal|auraIce)\)"',src)
 assert len(paths)==3, len(paths)
 grads=''.join(g.replace(f'id="{n}"',f'id="live{n[4:]}"') for n in ('auraPink','auraTeal','auraIce') for g in re.findall(rf'<linearGradient id="{n}".*?</linearGradient>',src,re.S))
 ribbons=''.join(f'<path class="orb-ribbon ribbon-{k}" d="{d}" stroke="url(#live{n[4:]})"/>' for k,(d,n) in zip(('one','two','three'),paths))
 return (f'<svg class="aura-orb-svg" viewBox="0 0 200 200" width="150" height="150" aria-hidden="true" focusable="false"><defs>{grads}'
  '<filter id="liveGlow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="0" stdDeviation="2.7" flood-color="#93C5FD" flood-opacity=".45"/></filter></defs>'
  f'<g fill="none" stroke-width="4.7" stroke-linejoin="round" filter="url(#liveGlow)">{ribbons}</g></svg>')

def aura_live():
 # "Say it." stays; "Consider it handled." is typed in a box that already holds the full phrase, so nothing moves.
 # Screen readers get the phrase once (the typed copy is hidden from them); no new controls, no sound, no microphone.
 return ('<figure class="aura-phone aura-live" data-aura-live>'
  f'<span class="aura-orb"><span class="orb-halo" aria-hidden="true"></span>{aura_live_svg()}</span>'
  '<figcaption>AURA</figcaption>'
  '<p class="aura-line" lang="en"><span class="aura-say">Say it.</span>'
  '<span class="aura-type"><span class="aura-type-full" aria-hidden="true">Consider it handled.</span>'
  '<span class="aura-type-live" aria-hidden="true"><span data-typed>Consider it handled.</span><i class="aura-caret"></i></span>'
  '<span class="sr-only">Consider it handled.</span></span></p></figure>')

# Going live on itdks.tech: the server's Content-Security-Policy allows styles from stylesheets only, so the agent
# characters' pivot points live in report09.css instead of style attributes.
_r7_agent_bot=agent_bot
def agent_bot(name):
 return re.sub(r' style="transform-origin:[^"]*"','',_r7_agent_bot(name))

# With Google Analytics enabled at launch (production build), the privacy page describes that configuration, as
# report 08 asks, together with its paragraphs on forms, external services and fonts.
PRIVACY_GA={
 'sq':'Google Analytics aktivizohet vetëm me pëlqimin tënd dhe mund të çaktivizohet te Cilësimet e privatësisë në fund të faqes. Matim faqen, gjuhën, shërbimin ose produktin dhe veprimin; nuk përfshijmë emër, email, telefon apo mesazh në eventet tona.',
 'en':'Google Analytics activates only with your consent and can be disabled through Privacy settings in the footer. We measure page, language, service or product and action; our events exclude names, emails, phone numbers and messages.',
 'de':'Google Analytics wird nur mit Ihrer Einwilligung aktiviert und kann über die Datenschutzeinstellungen im Footer deaktiviert werden. Wir messen Seite, Sprache, Leistung oder Produkt und Aktion; unsere Ereignisse enthalten keine Namen, E-Mails, Telefonnummern oder Nachrichten.'}
_r8_finalize=finalize
def finalize(html,page,l):
 html=_r8_finalize(html,page,l)
 if page=='privacy' and PRODUCTION and os.environ.get('ITD_ANALYTICS')=='1':
  paras=[PRIVACY_GA[l]]+PRIVACY[l][:3]+PRIVACY[l][4:]
  body=''.join(f'<p>{p}</p>' for p in paras)+f'<a class="text-link" href="mailto:{cfg["email"]}">{cfg["email"]}</a>'
  html,n=re.subn(r'<div class="wrap legal">.*?</div>',f'<div class="wrap legal">{body}</div>',html,count=1,flags=re.S)
  assert n==1
 return html

def labs(l,t):
 html=_r8_labs(l,t)
 if THEME=='m': return html
 old=aura_phone(l)
 assert html.count(old)==1
 return html.replace(old,aura_live()+'<script src="assets/aura-live.js" defer></script>',1)
