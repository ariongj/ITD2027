"""Security and bug audit of 25 October 2026 (itdks_security_and_bug_audit.pdf): the fixes made in the generator.

BUG-05: the Creative form offers the same six services as the cards above it, so choosing a card selects its
option instead of adding a near-duplicate. BUG-07: the illustrative project page stays out of the sitemap and the
index (NOINDEX in proposal.py) and no longer links to itself. The script fixes are in assets/orbit.js (BUG-03),
booking.js (BUG-04), measurement.js (BUG-02), site.js (BUG-06) and report11.js (BUG-08); BUG-01, security.txt
and the headers are in proposal.py and production.htaccess."""

_audit_creative=creative
def creative(l,t):
 html=_audit_creative(l,t)
 cards=list(dict.fromkeys(re.findall(r'data-creative-service="([^"]*)"',html)))
 form=re.search(r'(<form class="enquiry-form" data-form="creative".*?<select name="service"><option value="">[^<]*</option>)(.*?)(</select>)',html,re.S)
 if not cards or not form: return html
 return html[:form.start(2)]+''.join(f'<option>{x}</option>' for x in cards)+html[form.end(2):]

_audit_case_detail=case_detail
def case_detail(l,t):
 # The page's own case card: no link back to the same page, no filter attributes without a filter bar.
 html=_audit_case_detail(l,t)
 html=re.sub(rf'<a class="text-link" href="{re.escape(route("project-detail",l))}">.*?</a>','',html,count=1,flags=re.S)
 return html.replace(' data-filter-item="projects" data-category="software ai"','',1)
