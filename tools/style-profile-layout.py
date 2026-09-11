from pathlib import Path
import re

p=Path('README.md')
t=p.read_text(encoding='utf-8')

def replace_marked(text,start,end,body):
    pattern=re.compile(re.escape(start)+r'.*?'+re.escape(end),re.S)
    updated,count=pattern.subn(start+'\n'+body.rstrip()+'\n'+end,text,count=1)
    if count!=1: raise RuntimeError(f'missing marker {start}')
    return updated

analytics='''<h3 align="center">Public Development Analytics</h3>

<p align="center">
  <img width="100%" src="assets/profile/analytics-overview.svg" alt="Leviathan public development telemetry dashboard">
</p>'''
activity='''<p align="center">
  <img width="100%" src="assets/profile/activity-feed.svg" alt="Live public GitHub activity feed">
</p>'''
repos='''<p align="center">
  <img width="100%" src="assets/profile/repository-health.svg" alt="Public repository health dashboard">
</p>'''

t=replace_marked(t,'<!-- PUBLIC_ANALYTICS_START -->','<!-- PUBLIC_ANALYTICS_END -->',analytics)
t=replace_marked(t,'<!-- RECENT_ACTIVITY_START -->','<!-- RECENT_ACTIVITY_END -->',activity)
t=replace_marked(t,'<!-- REPOSITORY_FRESHNESS_START -->','<!-- REPOSITORY_FRESHNESS_END -->',repos)

t=t.replace('<h3 align="center">Recent Public Activity</h3>','<h3 align="center">Live Public Activity</h3>')
t=t.replace('<h3 align="center">Repository Freshness</h3>','<h3 align="center">Public Repository Health</h3>')

# Replace the plain Platform Areas table with a single visual system map.
platform_pattern=re.compile(r'## Platform Areas\n\n<table width="100%">.*?</table>',re.S)
platform_visual='''## Leviathan Ecosystem

<p align="center">
  <img width="100%" src="assets/profile/ecosystem-overview.svg" alt="Animated Leviathan ecosystem overview">
</p>

## Data Platform

<p align="center">
  <img width="100%" src="assets/profile/data-platform.svg" alt="Animated Leviathan database and data platform architecture">
</p>

The data layer is planned around a relational core with separate ephemeral caching, object storage and event processing. Public diagrams stay intentionally high-level while schemas, hosts, credentials and sensitive implementation details remain private.'''
if platform_pattern.search(t):
    t=platform_pattern.sub(platform_visual,t,count=1)
elif 'assets/profile/ecosystem-overview.svg' not in t:
    anchor='## Public Developer Repositories'
    t=t.replace(anchor,platform_visual+'\n\n'+anchor,1)

# Keep the page visually coherent by ensuring the analytics dashboard follows commit activity,
# then live feed and repository health, rather than detached cards or plain tables.
p.write_text(t,encoding='utf-8',newline='\n')
