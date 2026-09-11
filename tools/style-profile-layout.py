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

external='''## Identity & External Services

<p align="center">
  <img width="100%" src="assets/profile/external-services.svg" alt="Animated Microsoft, Xbox, Minecraft and Leviathan identity service boundary map">
</p>

Microsoft account services, Xbox Live, XSTS, Minecraft Services and Mojang/Minecraft platform systems remain external trust boundaries. Leviathan owns only its own account mapping, session/permission state, product state, device/Cast state, telemetry, licensing and other platform data required for Leviathan functionality.'''
if 'assets/profile/external-services.svg' not in t:
    anchor='## Leviathan Data Platform'
    if anchor in t:
        t=t.replace(anchor,external+'\n\n'+anchor,1)

platform_pattern=re.compile(r'## Platform Areas\n\n<table width="100%">.*?</table>',re.S)
ecosystem='''## Leviathan Ecosystem

<p align="center">
  <img width="100%" src="assets/profile/ecosystem-overview.svg" alt="Animated Leviathan ecosystem overview">
</p>'''
if platform_pattern.search(t):
    t=platform_pattern.sub(ecosystem,t,count=1)
elif 'assets/profile/ecosystem-overview.svg' not in t:
    anchor='## Public Developer Repositories'
    t=t.replace(anchor,ecosystem+'\n\n'+anchor,1)

experience='''## Experience & Commerce Flows

<p align="center">
  <img width="100%" src="assets/profile/experience-commerce.svg" alt="Animated Leviathan website, mobile, launcher, client, cosmetics, LeviCoins and commerce flow">
</p>

The public model separates player-facing experiences from the commerce and entitlement path: website and mobile account/store surfaces, launcher/client consumption, external payment processing, verified orders, Leviathan entitlements, cosmetics ownership, LeviCoins ledger state, referrals and creator/campaign attribution. Payment credentials remain with the payment provider.'''
if 'assets/profile/experience-commerce.svg' not in t:
    anchor='## Public Developer Repositories'
    if anchor in t:
        t=t.replace(anchor,experience+'\n\n'+anchor,1)

if '## Leviathan Data Platform' in t:
    duplicate=re.compile(r'\n## Data Platform\n\n<p align="center">\n  <img width="100%" src="assets/profile/data-platform\.svg".*?</p>\n\nThe data layer is planned.*?(?=\n## Public Developer Repositories)',re.S)
    t=duplicate.sub('',t,count=1)

p.write_text(t,encoding='utf-8',newline='\n')
