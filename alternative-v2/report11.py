"""Change report 11 (21 October 2026): the AI Agents scenes, main version only.

Each agent card opens with a scene: the character and its work object (phone, laptop, chat, task board, document,
calculator and chart) on one 9 s task: start 0-2 s, work 2-6 s, result 6-9 s (pages 5-12). The status above the scene
and the sentence below it come from one dictionary in SQ / EN / DE (pages 13-17); assets/report11.js types them in
the language of the page. The AI character's box shows the flow Request / Agent / Approval / Action beside the
character, lit in time with its gestures (page 6). Everything visual is SVG and CSS (assets/report11.css)."""

# The hero's old flow boxes (with their small step numbers) are replaced below, so that report 10 rule has nothing to do.
for _i in [i for i,(p,_) in enumerate(DECOR) if p.startswith('<div><small>')][::-1]: del DECOR[_i]; del DECOR_USED[_i]

# Texts of pages 14-16: panel, the three states and the two messages, per agent; "demo" marks the scene as a demo.
AGENT_COPY={
 'ari':{'panel':('Telefonatë','Phone call','Telefonat'),'state_start':('Lidhje...','Connecting...','Verbindung...'),'state_work':('Në bisedë','In conversation','Im Gespräch'),
  'state_result':('Për ekipin','For the team','Für das Team'),'message_work':('Po ju dëgjoj.','I am listening.','Ich höre zu.'),'message_done':('Kërkesa u shënua.','Request recorded.','Anfrage erfasst.')},
 'dita':{'panel':('Të dhëna','Data','Daten'),'state_start':('Hap tabelën','Open table','Tabelle öffnen'),'state_work':('Duke shkruar...','Typing...','Eingabe...'),
  'state_result':('U përmbledh','Summarised','Zusammengefasst'),'message_work':('Po organizoj të dhënat.','Organising the data.','Ich ordne die Daten.'),'message_done':('Përmbledhja është gati.','The summary is ready.','Die Übersicht ist fertig.')},
 'nora':{'panel':('Mbështetje','Support','Support'),'state_start':('Lexon mesazhin','Reading message','Nachricht lesen'),'state_work':('Duke u përgjigjur...','Replying...','Antwort wird erstellt...'),
  'state_result':('Hapat u dërguan','Steps sent','Schritte gesendet'),'message_work':('Si mund t’ju ndihmoj?','How can I help?','Wie kann ich helfen?'),'message_done':('Ju dërgova hapat.','I sent you the steps.','Die Schritte sind gesendet.')},
 'leo':{'panel':('Detyra','Tasks','Aufgaben'),'state_start':('Zgjedh detyrën','Select task','Aufgabe wählen'),'state_work':('E organizon','Organising','Wird geordnet'),
  'state_result':('Për miratim','For approval','Zur Freigabe'),'message_work':('Po organizoj detyrën.','Organising the task.','Ich ordne die Aufgabe.'),'message_done':('Gati për miratim.','Ready for approval.','Bereit zur Freigabe.')},
 'mira':{'panel':('Dokumente','Documents','Dokumente'),'state_start':('Hap dokumentin','Open document','Dokument öffnen'),'state_work':('Duke kërkuar...','Searching...','Suche läuft...'),
  'state_result':('Pjesa u gjet','Section found','Abschnitt gefunden'),'message_work':('Po kërkoj në dokument.','Searching the document.','Ich suche im Dokument.'),'message_done':('E gjeta pjesën.','I found the section.','Der Abschnitt ist gefunden.')},
 'fin':{'panel':('Raport','Report','Bericht'),'state_start':('Lexon shifrat','Read figures','Zahlen lesen'),'state_work':('Duke llogaritur...','Calculating...','Berechnung läuft...'),
  'state_result':('Raporti është gati','Report ready','Bericht fertig'),'message_work':('Po përmbledh shifrat.','Summarising the figures.','Ich fasse die Zahlen zusammen.'),'message_done':('Raporti është përgatitur.','The report is prepared.','Der Bericht ist erstellt.')}}
DEMO=('Pamje demonstrimi','Demo view','Demo-Ansicht')
# One full sentence per scene for screen readers (the animated scene itself is hidden from them).
SCENE_TEXT={'ari':('Ari merr një telefonatë dhe e shënon kërkesën për ekipin.','Ari takes a phone call and records the request for the team.','Ari nimmt einen Anruf entgegen und erfasst die Anfrage für das Team.'),
 'dita':('Dita shkruan në tastierë, organizon të dhënat dhe përgatit përmbledhjen.','Dita types, organises the data and prepares the summary.','Dita tippt, ordnet die Daten und erstellt die Übersicht.'),
 'nora':('Nora lexon mesazhin e klientit dhe i dërgon hapat.','Nora reads the customer’s message and sends the steps.','Nora liest die Nachricht des Kunden und sendet die Schritte.'),
 'leo':('Leo e vendos detyrën në rrjedhë dhe e përcjell për miratim.','Leo moves the task through the board and passes it on for approval.','Leo ordnet die Aufgabe ein und gibt sie zur Freigabe weiter.'),
 'mira':('Mira kërkon në dokument dhe gjen pjesën e duhur.','Mira searches the document and finds the right section.','Mira durchsucht das Dokument und findet den passenden Abschnitt.'),
 'fin':('Fin llogarit shifrat dhe përgatit raportin.','Fin calculates the figures and prepares the report.','Fin berechnet die Zahlen und erstellt den Bericht.')}
HERO_TEXT=('Pamje demonstrimi: agjenti merr kërkesën, e përpunon dhe e përcjell për miratim; veprimi vjen pas kontrollit njerëzor.',
 'Demo view: the agent takes the request, works on it and passes it on for approval; the action follows human review.',
 'Demo-Ansicht: Der Agent nimmt die Anfrage auf, bearbeitet sie und gibt sie zur Freigabe weiter; die Aktion folgt nach menschlicher Prüfung.')

def copy_json():
 data={l:{'demo':tr(l,*DEMO),**{n:{k:tr(l,*v) for k,v in AGENT_COPY[n].items()} for n in AGENT_COPY}} for l in ('sq','en','de')}
 return '<script type="application/json" id="r11-copy">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>'

# Work objects. In the hand: drawn in the character's canvas, inside the hand's group, so they turn with the arm.
HELD={'ari':('hand-r','<svg class="r11-held r11-phone" viewBox="0 0 30 58" aria-hidden="true" focusable="false"><rect x="2" y="2" width="26" height="54" rx="7" class="r11-device"/><rect x="6.5" y="8" width="17" height="34" rx="3" class="r11-screen"/><circle cx="15" cy="49" r="2.6" class="r11-acc-fill"/></svg>'
  '<svg class="r11-held r11-voice" viewBox="0 0 16 40" aria-hidden="true" focusable="false"><path d="M4 12v16M11 6v28" class="r11-acc-line"/></svg>'),
 'fin':('hand-r','<svg class="r11-held r11-calc" viewBox="0 0 40 44" aria-hidden="true" focusable="false"><rect x="2" y="2" width="36" height="40" rx="7" class="r11-device r11-acc-edge"/>'
  +''.join(f'<rect x="{9+r*9.5:.1f}" y="{10+c*9.5:.1f}" width="5" height="5" rx="1.4" class="r11-key r11-key-{c*3+r}"/>' for c in range(3) for r in range(3))+'</svg>')}

# On the panel beside the character (shapes only: real sentences stay outside the scene, in HTML).
def panel_svg(name):
 if name=='ari':
  bars=''.join(f'<rect x="{12+i*13}" y="{38-h/2}" width="5" height="{h}" rx="2.5" class="r11-acc-fill r11-bar r11-bar-{i}"/>' for i,h in enumerate([8,16,24,14,20,10,18,8,12]))
  return ('<svg viewBox="0 0 140 72" aria-hidden="true" focusable="false"><circle cx="14" cy="12" r="8" class="r11-shape"/><rect x="28" y="7" width="58" height="5" rx="2.5" class="r11-shape"/><rect x="28" y="15" width="36" height="4" rx="2" class="r11-shape r11-dim"/>'
   f'<g class="r11-wave">{bars}</g><g class="r11-done"><circle cx="14" cy="61" r="7" class="r11-acc-ring"/><path d="m10.6 61 2.4 2.4 4.4-4.8" class="r11-acc-line"/><rect x="28" y="58" width="74" height="6" rx="3" class="r11-acc-soft"/></g></svg>')
 if name=='dita':
  cells=''.join(f'<rect x="{8+c*44}" y="{8+r*17}" width="36" height="8" rx="4" class="r11-cell r11-cell-r{r}{" r11-cell-hi" if (r,c)==(1,1) else ""}"/>' for r in range(3) for c in range(3))
  return f'<svg viewBox="0 0 140 72" aria-hidden="true" focusable="false">{cells}<g class="r11-done"><circle cx="126" cy="62" r="7" class="r11-acc-ring"/><path d="m122.6 62 2.4 2.4 4.4-4.8" class="r11-acc-line"/></g></svg>'
 if name=='nora':
  return ('<svg viewBox="0 0 140 72" aria-hidden="true" focusable="false"><g class="r11-ask"><rect x="4" y="4" width="98" height="24" rx="9" class="r11-bubble"/><rect x="13" y="11" width="64" height="4" rx="2" class="r11-shape r11-light"/><rect x="13" y="18" width="40" height="4" rx="2" class="r11-shape r11-light"/></g>'
   '<rect x="34" y="40" width="102" height="26" rx="9" class="r11-bubble r11-bubble-out"/>'
   '<g class="r11-typing"><circle cx="50" cy="53" r="3" class="r11-acc-fill r11-dot-0"/><circle cx="61" cy="53" r="3" class="r11-acc-fill r11-dot-1"/><circle cx="72" cy="53" r="3" class="r11-acc-fill r11-dot-2"/></g>'
   '<g class="r11-reply"><rect x="44" y="47" width="70" height="4" rx="2" class="r11-acc-fill"/><rect x="44" y="55" width="46" height="4" rx="2" class="r11-acc-fill r11-dim"/><path d="m119 53 3 3 6-6.5" class="r11-acc-line"/></g></svg>')
 if name=='leo':
  cols=''.join(f'<rect x="{4+i*46}" y="4" width="40" height="64" rx="6" class="r11-col"/><rect x="{11+i*46}" y="11" width="22" height="3" rx="1.5" class="r11-shape r11-light"/>' for i in range(3))
  return (f'<svg viewBox="0 0 140 72" aria-hidden="true" focusable="false">{cols}<g class="r11-task"><rect x="9" y="22" width="30" height="24" rx="5" class="r11-acc-fill"/><rect x="14" y="29" width="18" height="3" rx="1.5" class="r11-ink"/><rect x="14" y="36" width="12" height="3" rx="1.5" class="r11-ink"/>'
   '<g class="r11-done"><circle cx="36" cy="22" r="6" class="r11-badge"/><path d="m33 22 2 2 3.6-4" class="r11-acc-line r11-ink-line"/></g></g></svg>')
 if name=='mira':
  lines=''.join(f'<rect x="16" y="{14+i*13}" width="{[100,108,92,104][i]}" height="3" rx="1.5" class="r11-shape r11-light"/>' for i in range(4))
  return (f'<svg viewBox="0 0 140 72" aria-hidden="true" focusable="false"><g class="r11-doc"><rect x="6" y="4" width="128" height="64" rx="6" class="r11-col"/><rect x="11" y="22" width="118" height="12" rx="4" class="r11-acc-soft r11-found"/>{lines}</g>'
   '<g class="r11-lens"><circle cx="0" cy="0" r="9" class="r11-acc-ring r11-lens-glass"/><path d="m6.5 6.5 7 7" class="r11-acc-line r11-thick"/></g></svg>')
 if name=='fin':
  bars=''.join(f'<rect x="{18+i*30}" y="{62-h}" width="18" height="{h}" rx="3" class="r11-acc-fill r11-col-bar r11-col-bar-{i}"/>' for i,h in enumerate([22,38,28,50]))
  return f'<svg viewBox="0 0 140 72" aria-hidden="true" focusable="false"><path d="M8 63h124" class="r11-axis"/>{bars}</svg>'

def scene_bot(name):
 # The report 07 layers, with each hand (and what it holds) in a group that turns around the shoulder.
 rig=AGENT_RIG[name]; held=HELD.get(name)
 parts=''
 for x in rig['layers']:
  img=f'<img class="ab ab-{x}" src="assets/ai/agents/{name}/{x}.webp" width="216" height="150" alt="" loading="lazy" decoding="async">'
  if x.startswith('hand-'): parts+=f'<span class="r11-arm r11-{x}">{img}{held[1] if held and held[0]==x else ""}</span>'
  else: parts+=img
 return f'<span class="r11-actor"><span class="agent-bot" data-agent-bot="{name}"><span class="ab-rig">{parts}</span></span></span>'

def stage(name,l):
 c={k:tr(l,*v) for k,v in AGENT_COPY[name].items()}
 keyboard='<svg class="r11-keyboard" viewBox="0 0 190 26" aria-hidden="true" focusable="false"><rect x="1" y="1" width="188" height="24" rx="6" class="r11-col"/>'+''.join(f'<rect x="{8+i*15}" y="{6+r*8}" width="11" height="5" rx="1.5" class="r11-key r11-key-{(i*7+r*3)%9}"/>' for r in range(2) for i in range(12))+'</svg>' if name=='dita' else ''
 # The HTML holds the result (the still view with reduced motion); report11.js runs the task in the page's language.
 return (f'<div class="r11-stage" data-scene="{name}" data-motion aria-hidden="true">'
  f'<div class="r11-top"><span class="r11-state" data-r11-state>{c["state_result"]}</span><span class="r11-phase"><i></i><i></i><i></i></span></div>'
  f'<div class="r11-scene">{scene_bot(name)}<div class="r11-panel"><p class="r11-panel-head"><span class="r11-ddd"><i></i><i></i><i></i></span><span data-r11-panel>{c["panel"]}</span></p>{panel_svg(name)}</div>{keyboard}</div>'
  f'<p class="r11-status"><span data-r11-msg>{c["message_done"]}</span><i class="r11-caret"></i></p>'
  '<div class="r11-progress"><i></i><i></i><i></i></div></div>'
  f'<p class="sr-only">{tr(l,*DEMO)}: {tr(l,*SCENE_TEXT[name])}</p>')

def hero_box(l):
 layers=''.join(f'<img class="ac ac-{x}" src="assets/ai/character/{x}.webp" width="360" height="311" alt="" decoding="async">' for x in CHARACTER_LAYERS)
 steps=tr(l,['Kërkesë','Agjent','Miratim','Veprim'],['Request','Agent','Approval','Action'],['Anfrage','Agent','Freigabe','Aktion'])
 return ('<div class="ai-flow-card r11-hero" data-motion><div class="r11-hero-grid">'
  f'<div class="r11-hero-actor" aria-hidden="true"><div class="agent-character"><div class="ac-rig">{layers}</div></div></div>'
  '<ol class="r11-steps">'+''.join(f'<li>{s}</li>' for s in steps)+'</ol></div>'
  f'<p class="r11-hero-caption" aria-hidden="true">{tr(l,*DEMO)}</p><div class="r11-progress" aria-hidden="true"><i></i><i></i><i></i></div>'
  f'<p class="sr-only">{tr(l,*HERO_TEXT)}</p></div>')

_r10_ai=ai
def ai(l,t):
 html=_r10_ai(l,t)
 if THEME=='m': return html
 html,n=re.subn(r'<div class="ai-flow-card" data-motion>.*?<div class="ai-flow">.*?</div><p>[^<]*</p></div>',lambda m:hero_box(l),html,count=1,flags=re.S)
 assert n==1
 for name in AGENT_NAMES:
  html,n=re.subn(rf'(<article class="agent-card card" id="agent-{name}">)<div class="agent-heading">.*?</div>',lambda m:m.group(1)+stage(name,l),html,count=1,flags=re.S)
  assert n==1, name
 return html.replace('<section class="wrap section" id="agents">',copy_json()+'<section class="wrap section" id="agents">',1)
