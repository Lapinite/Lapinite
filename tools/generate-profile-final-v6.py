from pathlib import Path
from html import escape as esc

ROOT = Path("assets")
P = ROOT / "profile"
P.mkdir(parents=True, exist_ok=True)

C = {
    "cyan": "#35e9ff",
    "blue": "#00a8ff",
    "violet": "#8b7cff",
    "green": "#55e4ae",
    "amber": "#ffb44e",
    "white": "#effcff",
    "muted": "#7f9fb1",
    "panel": "#061722",
    "line": "#173d52",
}

DEFS = r'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
  <stop stop-color="#020811"/><stop offset=".55" stop-color="#061723"/><stop offset="1" stop-color="#020a12"/>
</linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
  <stop stop-color="#087dff"/><stop offset=".5" stop-color="#35e9ff"/><stop offset="1" stop-color="#00a5ff"/>
</linearGradient>
<radialGradient id="energy">
  <stop stop-color="#a4fbff" stop-opacity=".54"/><stop offset=".25" stop-color="#21dfff" stop-opacity=".17"/><stop offset="1" stop-color="#02101a" stop-opacity="0"/>
</radialGradient>
<filter id="glow" x="-120%" y="-120%" width="340%" height="340%">
  <feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
  <path d="M28 0H0V28" fill="none" stroke="#12374d" opacity=".14"/>
</pattern>
</defs>'''

def write(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")

def start(w, h, title, subtitle):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        DEFS,
        f'<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>',
        f'<rect width="{w}" height="{h}" rx="24" fill="url(#grid)"/>',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="none" stroke="#173d52"/>',
        f'<text x="42" y="43" fill="#58eaff" font-family="ui-monospace,Consolas,monospace" font-size="14" letter-spacing="2.8">{esc(title)}</text>',
        f'<text x="42" y="67" fill="#7e9caf" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(subtitle)}</text>',
        f'<path d="M42 86H{w-42}" stroke="#14384a"/>',
        '<path d="M42 84H162" stroke="#35e9ff" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>',
    ]

def end(lines, w, h, footer="PUBLIC-SAFE SYSTEM VIEW // PRIVATE SOURCE, SECRETS AND SENSITIVE IMPLEMENTATION EXCLUDED"):
    lines += [
        f'<text x="42" y="{h-22}" fill="#557b8f" font-family="ui-monospace,Consolas,monospace" font-size="8.5">{esc(footer)}</text>',
        f'<path d="M6 6H{w-6}V{h-6}H6Z" fill="none" stroke="url(#edge)" stroke-width="2" stroke-dasharray="170 2500" filter="url(#glow)" opacity=".78">'
        '<animate attributeName="stroke-dashoffset" from="0" to="-2670" dur="22s" repeatCount="indefinite"/></path>',
        '</svg>',
    ]
    return "\n".join(lines)

def card(x, y, w, h, title, rows, color, eyebrow=""):
    a = ['<g>']
    a.append(f'<path d="M{x} {y}H{x+w-14}L{x+w} {y+14}V{y+h}H{x}Z" fill="{C["panel"]}" stroke="{color}" stroke-opacity=".52"/>')
    yy = y + 23
    if eyebrow:
        a.append(f'<text x="{x+18}" y="{yy}" fill="{color}" font-family="ui-monospace,Consolas,monospace" font-size="8.5">{esc(eyebrow)}</text>')
        yy += 24
    a.append(f'<text x="{x+18}" y="{yy}" fill="{C["white"]}" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700">{esc(title)}</text>')
    yy += 22
    for row in rows:
        a.append(f'<text x="{x+20}" y="{yy}" fill="#cae5ed" font-family="ui-monospace,Consolas,monospace" font-size="8.4">{esc(row)}</text>')
        yy += 18
    a.append(f'<path d="M{x+18} {y+h-17}H{x+w-24}" stroke="{color}" stroke-opacity=".22" stroke-dasharray="18 10"/>')
    a.append('</g>')
    return "".join(a)

def connector(d, color, dur="5s", begin="0s", packet=True, opacity=.70):
    s = [f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.45" stroke-opacity="{opacity}"/>']
    if packet:
        s.append(
            f'<circle r="4" fill="#d4fdff" filter="url(#glow)" opacity="0">'
            f'<animateMotion dur="{dur}" begin="{begin}" repeatCount="indefinite" calcMode="linear" keyPoints="0;1" keyTimes="0;1" path="{d}"/>'
            f'<animate attributeName="opacity" dur="{dur}" begin="{begin}" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.06;.86;.94;1"/>'
            f'</circle>'
        )
    return "".join(s)

def reactor(x, y, r, label="LEVIATHAN", sub="PROJECT CORE", color=None):
    color = color or C["cyan"]
    inner = max(28, int(r * .40))
    spoke_inner = inner + 12
    spoke_outer = r - 14

    ticks = []
    for ang in range(0, 360, 15):
        ticks.append(
            f'<g transform="rotate({ang})"><path d="M0 -{r-3}V-{r-9}" stroke="#5bdff1" stroke-width="1.2" stroke-opacity=".55"/></g>'
        )

    spokes = []
    ports = []
    for i, ang in enumerate(range(0, 360, 60)):
        delay = i * 0.48
        y1 = -spoke_outer
        y2 = -spoke_inner
        spokes.append(
            f'''<g transform="rotate({ang})">
<path d="M-11 {y1}H11L8 {y2}H-8Z" fill="#04131d" stroke="{color}" stroke-opacity=".46"/>
<path d="M0 {y1+6}V{y2-5}" stroke="{color}" stroke-width="5.5" stroke-linecap="round" opacity=".35" filter="url(#glow)">
  <animate attributeName="opacity" values=".22;.22;.95;.35;.22" keyTimes="0;.36;.52;.68;1" dur="6s" begin="{delay}s" repeatCount="indefinite"/>
</path>
<path d="M0 {y1+7}V{y2-7}" pathLength="100" stroke="#d6fdff" stroke-width="2.1" stroke-linecap="round" stroke-dasharray="9 91" stroke-dashoffset="100">
  <animate attributeName="stroke-dashoffset" from="100" to="0" dur="6s" begin="{delay}s" repeatCount="indefinite"/>
</path>
</g>'''
        )
        ports.append(
            f'<g transform="rotate({ang})"><rect x="-6" y="-{r+23}" width="12" height="11" rx="2" fill="#04131d" stroke="{color}" stroke-opacity=".75"/><rect x="-2" y="-{r+20}" width="4" height="5" rx="1" fill="#bdfbff" filter="url(#glow)"/></g>'
        )

    emblem = f'''
<g filter="url(#glow)" stroke="{color}" stroke-width="4.2" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="M0 -{int(inner*.67)}V{int(inner*.58)}"/>
  <path d="M-{int(inner*.60)} -{int(inner*.22)}L-{int(inner*.24)} 0L-{int(inner*.46)} {int(inner*.50)}"/>
  <path d="M{int(inner*.60)} -{int(inner*.22)}L{int(inner*.24)} 0L{int(inner*.46)} {int(inner*.50)}"/>
</g>'''

    return f'''<g transform="translate({x} {y})">
<circle r="{r+34}" fill="url(#energy)"/>
<circle r="{r+20}" fill="#020b14" stroke="#123f52" stroke-width="1.1"/>
<circle r="{r+15}" fill="none" stroke="{color}" stroke-width="3" stroke-dasharray="58 18 18 12" filter="url(#glow)">
  <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="28s" repeatCount="indefinite"/>
</circle>
<circle r="{r+3}" fill="none" stroke="#2e7f98" stroke-width="1.35" stroke-dasharray="16 10 4 9">
  <animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="19s" repeatCount="indefinite"/>
</circle>
<g>{''.join(ticks)}<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="46s" repeatCount="indefinite"/></g>
{''.join(spokes)}
{''.join(ports)}
<circle r="{spoke_inner-3}" fill="none" stroke="{color}" stroke-width="1.4" stroke-opacity=".48"/>
<circle r="{inner+5}" fill="url(#energy)" opacity=".55">
  <animate attributeName="opacity" values=".38;.62;.38" dur="4.8s" repeatCount="indefinite"/>
</circle>
<polygon points="0,-{inner} {int(inner*.86)},-{int(inner*.50)} {int(inner*.86)},{int(inner*.50)} 0,{inner} -{int(inner*.86)},{int(inner*.50)} -{int(inner*.86)},-{int(inner*.50)}"
 fill="#04131d" stroke="{color}" stroke-width="1.4"/>
{emblem}
<text x="0" y="{r+48}" text-anchor="middle" fill="{C["white"]}" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">{esc(label)}</text>
<text x="0" y="{r+64}" text-anchor="middle" fill="#6b9aad" font-family="ui-monospace,Consolas,monospace" font-size="7.3" letter-spacing="1.4">{esc(sub)}</text>
</g>'''

def hero(light=False):
    w,h=1200,560
    bg = '#eff8fc' if light else '#020811'
    panel = '#ffffff' if light else '#061722'
    text = '#08202d' if light else '#effcff'
    muted = '#486c7f' if light else '#82a1b2'
    grid = '#8bc3d8' if light else '#12374d'
    defs = DEFS.replace('#020811',bg).replace('#061723',bg).replace('#020a12',bg).replace('#061722',panel).replace('#12374d',grid)
    L=[
      f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
      defs,
      f'<rect width="{w}" height="{h}" rx="26" fill="{bg}"/><rect width="{w}" height="{h}" rx="26" fill="url(#grid)" opacity=".72"/>',
      f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="25" fill="none" stroke="#1b5169"/>',
      '<text x="42" y="30" fill="#6394aa" font-family="monospace" font-size="8" letter-spacing="2">LEVIATHAN SYSTEM</text>',
      '<text x="210" y="30" fill="#35e9ff" font-family="monospace" font-size="8" letter-spacing="2">PROJECT CONTROL INTERFACE</text>',
      '<text x="1050" y="30" fill="#55e4ae" font-family="monospace" font-size="8" letter-spacing="2">SIGNAL ONLINE</text>',
      '<path d="M42 44H1158" stroke="#17445a"/>',
      '<rect x="42" y="78" width="4" height="258" rx="2" fill="#35e9ff" filter="url(#glow)"/>',
      '<text x="72" y="108" fill="#35e9ff" font-family="monospace" font-size="13" letter-spacing="3">LEVIATHAN // SYSTEM READY</text>',
      f'<text x="72" y="190" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="64" font-weight="800">LEVIATHAN</text>',
      f'<text x="72" y="228" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="18">Connected Minecraft software, services and infrastructure.</text>',
      '<text x="72" y="258" fill="#55e4ae" font-family="monospace" font-size="9">PLAYER • PLATFORM • SECURITY • OPERATIONS</text>',
      f'<text x="72" y="290" fill="{muted}" font-family="monospace" font-size="9">LAUNCHER • CLIENT • WEB • APP • SERVERS • API • DATA • TELEMETRY</text>',
      f'<path d="M72 322H560L576 338V405H72Z" fill="{panel}" stroke="#1b536b"/>',
      '<text x="94" y="348" fill="#638da1" font-family="monospace" font-size="8">CONNECTED DOMAINS</text>',
      f'<text x="94" y="379" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">6 SYSTEM FAMILIES</text>',
      '<text x="292" y="348" fill="#638da1" font-family="monospace" font-size="8">VISIBILITY</text>',
      f'<text x="292" y="379" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">PUBLIC + PRIVATE</text>',
      '<text x="462" y="348" fill="#638da1" font-family="monospace" font-size="8">STATUS</text>',
      '<text x="462" y="379" fill="#35e9ff" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">PER PRODUCT</text>',
      card(650,100,170,80,'PLAYER',['LAUNCH / CLIENT'],C['cyan'],'01'),
      card(1040,100,120,80,'PLATFORM',['API / AUTH'],C['violet'],'02'),
      card(650,392,170,80,'SECURITY',['VERIFY / GUARD'],C['amber'],'03'),
      card(1040,392,120,80,'OPS',['DATA / STATUS'],C['green'],'04'),
      connector('M820 140H842L858 176',C['cyan'],'5.2s','0s'),
      connector('M1040 140H1018L1002 176',C['violet'],'5.5s','.8s'),
      connector('M820 432H842L858 356',C['amber'],'5.8s','1.6s'),
      connector('M1040 432H1018L1002 356',C['green'],'6.1s','2.4s'),
      reactor(930,270,104,'LEVIATHAN','PROJECT CORE'),
      '<path d="M42 500H1158" stroke="#154052"/>',
      '<text x="42" y="526" fill="#5f8296" font-family="monospace" font-size="8">PUBLIC SURFACE // WEBSITE / PROFILE / DOCS / SDK / API / EXAMPLES / INTEGRATIONS / STATUS</text>',
      '<path d="M8 8H1192V552H8Z" fill="none" stroke="url(#edge)" stroke-width="2.4" stroke-dasharray="220 2400" filter="url(#glow)"><animate attributeName="stroke-dashoffset" from="0" to="-2620" dur="20s" repeatCount="indefinite"/></path>',
      '</svg>'
    ]
    return "\n".join(L)

write(ROOT/"hero-dark-v4.svg", hero(False))
write(ROOT/"hero-light-v4.svg", hero(True))

L=start(1200,520,'LEVIATHAN COMMAND CORE // PROJECT OVERVIEW','Four project-state inputs feed one mechanical Leviathan reactor core.')
for x,y,k,v,c in [
    (44,112,'ORCHESTRATION','MULTI-PROJECT',C['cyan']),
    (320,112,'VISIBILITY','PUBLIC + PRIVATE',C['cyan']),
    (44,232,'RELEASE MODE','COMPONENT-SPECIFIC',C['violet']),
    (320,232,'VALIDATION','BUILD • TEST • HARDEN',C['amber']),
]:
    L.append(card(x,y,250,94,v,[],c,k))
L += [
    connector('M570 159H730L790 205',C['cyan'],'5.3s','0s'),
    connector('M570 279H730L790 267',C['violet'],'5.7s','1.1s'),
    reactor(930,236,108,'LEVIATHAN','COMMAND CORE'),
    '<path d="M650 421H1115" stroke="#17465b"/><text x="650" y="408" fill="#6f93a6" font-family="monospace" font-size="8">ACTIVE DEVELOPMENT // TRACKED PER PRODUCT</text>',
]
write(P/'command-core-v3.svg',end(L,1200,520))

L=start(1200,690,'LEVIATHAN NEURAL CORE // PUBLIC SYSTEM PROJECTION','Four balanced domains terminate at dedicated ports around one larger reactor core.')
for x,y,t,rows,c,k in [
    (44,116,'PLAYER SOFTWARE',['LAUNCHER / CLIENT / APP / CAST'],C['cyan'],'DOMAIN 01'),
    (856,116,'PLATFORM SERVICES',['AUTH / API / INTEGRATIONS / ACCOUNTS'],C['violet'],'DOMAIN 02'),
    (44,452,'PROTECTION & INTEGRITY',['NIMBUS / VALIDATION / EVIDENCE'],C['amber'],'DOMAIN 03'),
    (856,452,'OBSERVABILITY',['TELEMETRY / ANALYTICS / STATUS'],C['green'],'DOMAIN 04'),
]:
    L.append(card(x,y,300,110,t,rows,c,k))
for d,c,dur,b in [
    ('M344 171H430L480 225',C['cyan'],'5.1s','0s'),
    ('M856 171H770L720 225',C['violet'],'5.4s','.8s'),
    ('M344 507H430L480 427',C['amber'],'5.7s','1.6s'),
    ('M856 507H770L720 427',C['green'],'6s','2.4s'),
]:
    L.append(connector(d,c,dur,b))
L.append(reactor(600,326,128,'LEVIATHAN','NEURAL CORE'))
write(P/'neural-core-v3.svg',end(L,1200,690))

L=start(1200,920,'LEVIATHAN SYSTEMS MATRIX // PROJECT DIRECTORY','Six aligned project families use wide routing lanes around one readable center core.')
xs=[44,425,806]
top_y,bottom_y=108,640
matrix=[
 ('Play, launch and customize',['LAUNCHER','CLIENT','APP','UPDATER','INSTALLER','MODPACK STUDIO'],C['cyan'],'01 // PLAYER SYSTEMS'),
 ('Identity, social and creation',['WEBSITE','DISCORD BOT','CREATOR STUDIO','COSMETICS','LINKS','VERIFY'],C['violet'],'02 // WEB & COMMUNITY'),
 ('Networks, routing and safety',['RELAY','SERVER MANAGER','SERVER GUARDIAN','SERVER TOOLS','NETWORK CONTROL'],C['green'],'03 // SERVER SYSTEMS'),
 ('Detect, verify and diagnose',['NIMBUS ANTICHEAT','LEVIATHAN ANTICHEAT','SECURITY','INCIDENT RECORDER','CONFLICT DETECTIVE','DOCTOR'],C['amber'],'04 // PROTECTION & INTEGRITY'),
 ('Identity, data and entitlements',['API','AUTH','LICENSING','DATABASE','PLATFORM','VAULT'],C['violet'],'05 // PLATFORM SERVICES'),
 ('Build, observe and release',['DOCS / API DOCS / SDK','INTEGRATIONS / EXAMPLES / STATUS','TELEMETRY / ANALYTICS','RESEARCH / INFRASTRUCTURE','RELEASE ENGINEERING','CLAUDE SKILLS'],C['cyan'],'06 // DEVELOPER & OPS'),
]
for i,m in enumerate(matrix):
    L.append(card(xs[i%3],top_y if i<3 else bottom_y,350,220,m[0],m[1],m[2],m[3]))
for d,c,dur,b,packet in [
 ('M219 328V376H505',C['cyan'],'5.4s','0s',True),
 ('M600 328V368',C['violet'],'5.1s','.8s',False),
 ('M981 328V376H695',C['green'],'5.6s','1.6s',True),
 ('M219 640V590H505',C['amber'],'5.5s','2.4s',True),
 ('M600 640V598',C['violet'],'5.2s','3.2s',False),
 ('M981 640V590H695',C['cyan'],'5.7s','4s',True),
 ('M505 376H530',C['cyan'],'4.8s','0s',False),
 ('M695 376H670',C['green'],'4.8s','0s',False),
 ('M505 590H530',C['amber'],'4.8s','0s',False),
 ('M695 590H670',C['cyan'],'4.8s','0s',False),
]:
    L.append(connector(d,c,dur,b,packet=packet))
L.append(reactor(600,483,90,'LEVIATHAN','MATRIX CORE'))
write(P/'systems-matrix-v1.svg',end(L,1200,920,'DIRECTORY SIGNAL // PUBLIC PRODUCT NAMES AND FAMILIES ONLY'))

def radial_six(filename,title,subtitle,left,right,center_label,center_sub):
    L=start(1200,700,title,subtitle)
    ys=[116,292,468]
    for i,(t,rows,c) in enumerate(left):
        L.append(card(44,ys[i],300,116,t,rows,c,f'{i+1:02}'))
    for i,(t,rows,c) in enumerate(right):
        L.append(card(856,ys[i],300,116,t,rows,c,f'{i+4:02}'))
    routes=[
      ('M344 174H430L480 232',left[0][2],'5.1s','0s'),
      ('M344 350H462',left[1][2],'5.3s','.7s'),
      ('M344 526H430L480 468',left[2][2],'5.5s','1.4s'),
      ('M856 174H770L720 232',right[0][2],'5.2s','2.1s'),
      ('M856 350H738',right[1][2],'5.4s','2.8s'),
      ('M856 526H770L720 468',right[2][2],'5.6s','3.5s'),
    ]
    for d,c,dur,b in routes: L.append(connector(d,c,dur,b))
    L.append(reactor(600,350,112,center_label,center_sub))
    write(P/filename,end(L,1200,700))

radial_six(
 'data-platform-v2.svg',
 'LEVIATHAN DATA PLATFORM // PUBLIC ARCHITECTURE DIRECTION',
 'Six data domains terminate cleanly around one shared state and event core.',
 [
   ('IDENTITY & ACCOUNTS',['USERS • PREFERENCES'],C['cyan']),
   ('LAUNCHER & CLIENT',['PROFILE • INSTANCES • SETTINGS'],C['cyan']),
   ('NIMBUS & SECURITY',['EVIDENCE • SIGNALS • AUDIT'],C['amber']),
 ],
 [
   ('API & PLATFORM',['PROTOCOLS • INTEGRATIONS'],C['violet']),
   ('TELEMETRY & ANALYTICS',['PERFORMANCE • DIAGNOSTICS'],C['green']),
   ('LICENSING & COMMERCE',['ORDERS • LICENSE STATE'],C['amber']),
 ],
 'DATA CORE','POSTGRESQL • EVENTS'
)
radial_six(
 'core-products-v2.svg',
 'LEVIATHAN // PRODUCT FAMILIES',
 'Six public product families connect to one branded Leviathan platform core.',
 [
   ('PLAYER SOFTWARE',['Launcher • Client • App','Profiles • Instances • Mods'],C['cyan']),
   ('WEB & COMMUNITY',['Website • Profiles • Forum','Verify • Discord • Creator'],C['violet']),
   ('PROTECTION & INTEGRITY',['Nimbus • Leviathan AntiCheat','Security • Diagnostics'],C['amber']),
 ],
 [
   ('SERVER ECOSYSTEM',['Relay • Manager • Guardian','Server Tools • Verification'],C['green']),
   ('PLATFORM SERVICES',['API • Auth • Licensing','Database • Platform • Vault'],C['violet']),
   ('DEVELOPER & OPS',['SDK • Docs • Integrations','Analytics • Status • Research'],C['cyan']),
 ],
 'LEVIATHAN','PLATFORM CORE'
)

L=start(1200,700,'IDENTITY & EXTERNAL SERVICE BOUNDARIES','Six trust stages terminate at explicit ports around the Leviathan identity boundary.')
nodes=[
 (54,120,'01 MICROSOFT',['OAUTH'],C['cyan']),
 (310,100,'02 XBOX LIVE',['IDENTITY'],C['cyan']),
 (700,100,'03 XSTS',['AUTHORIZATION'],C['violet']),
 (956,120,'04 MINECRAFT',['SERVICES'],C['violet']),
 (956,484,'05 OWNERSHIP',['PROFILE'],C['green']),
 (54,484,'06 LEVIATHAN',['IDENTITY BOUNDARY'],C['green']),
]
for n in nodes: L.append(card(n[0],n[1],190,88,n[2],n[3],n[4]))
for d,c,dur,b in [
 ('M244 164H360L484 238',C['cyan'],'5.3s','0s'),
 ('M500 144H522L548 217',C['cyan'],'5.5s','.7s'),
 ('M700 144H678L652 217',C['violet'],'5.7s','1.4s'),
 ('M956 164H840L716 238',C['violet'],'5.9s','2.1s'),
 ('M956 528H840L716 462',C['green'],'6.1s','2.8s'),
 ('M244 528H360L484 462',C['green'],'6.3s','3.5s'),
]:
    L.append(connector(d,c,dur,b))
L.append(reactor(600,350,108,'TRUST CORE','IDENTITY BOUNDARY'))
write(P/'external-services-v2.svg',end(L,1200,700))

for fname,title,subtitle in [
 ('ecosystem-overview-v2.svg','LEVIATHAN ECOSYSTEM // PRODUCT SURFACES','Four balanced domains surround one shared Leviathan core.'),
 ('platform-areas-v2.svg','LEVIATHAN // PLATFORM AREAS','Four platform domains terminate at one central routing core.'),
]:
    L=start(1200,610,title,subtitle)
    items=[
      (54,122,'PLAYER SOFTWARE',['Launcher • Client • Profiles'],C['cyan'],'01'),
      (826,122,'PLATFORM SERVICES',['Auth • API • Accounts'],C['violet'],'02'),
      (54,390,'PROTECTION',['Nimbus • Security • Integrity'],C['amber'],'03'),
      (826,390,'OBSERVABILITY',['Telemetry • Analytics • Status'],C['green'],'04'),
    ]
    for x,y,t,rows,c,k in items:L.append(card(x,y,320,112,t,rows,c,k))
    for d,c,dur,b in [
      ('M374 178H470L500 232',C['cyan'],'5.2s','0s'),
      ('M826 178H730L700 232',C['violet'],'5.4s','.8s'),
      ('M374 446H470L500 388',C['amber'],'5.6s','1.6s'),
      ('M826 446H730L700 388',C['green'],'5.8s','2.4s'),
    ]:L.append(connector(d,c,dur,b))
    L.append(reactor(600,310,102,'LEVIATHAN','ROUTING CORE' if 'platform' in fname else 'ECOSYSTEM CORE'))
    write(P/fname,end(L,1200,610))

L=start(1200,840,'LEVIATHAN EXPERIENCE + COMMERCE // PUBLIC DIRECTION','Player surfaces, platform state and entitlements use separated routing lanes and readable cores.')
tops=[
 (40,'WEBSITE',['ACCOUNT • STORE • SUPPORT'],C['cyan'],190),
 (294,'MOBILE APP',['ACCOUNT • COSMETICS • ALERTS'],C['cyan'],190),
 (716,'LAUNCHER',['PROFILES • INSTANCES • STORE'],C['cyan'],190),
 (970,'CLIENT',['COSMETICS • ENTITLEMENT'],C['cyan'],190),
]
for x,t,rows,c,w in tops:L.append(card(x,112,w,100,t,rows,c))
for d,c,dur,b,pkt in [
 ('M230 162H355L488 220',C['cyan'],'5.5s','0s',True),
 ('M484 162H470L492 250',C['cyan'],'5.8s','.8s',False),
 ('M716 162H730L708 250',C['cyan'],'5.7s','1.6s',False),
 ('M970 162H845L712 220',C['cyan'],'6s','2.4s',True),
]:
    L.append(connector(d,c,dur,b,pkt))
L.append(reactor(600,292,100,'PLATFORM','AUTH • API • STATE'))
L.append(connector('M600 426V476',C['violet'],'5.4s','.5s'))
L.append(reactor(600,566,72,'ENTITLEMENT','ORDER • LICENSE • WALLET',C['violet']))
bottom=[
 (30,'STORE / CATALOG',['PUBLIC FLOW'],C['amber']),
 (266,'CHECKOUT',['PUBLIC FLOW'],C['amber']),
 (502,'PAYMENT PROVIDER',['EXTERNAL BOUNDARY'],C['amber']),
 (738,'ORDER VERIFY',['PUBLIC FLOW'],C['amber']),
 (974,'GROWTH / ATTRIBUTION',['PUBLIC FLOW'],C['green']),
]
centers=[]
for x,t,rows,c in bottom:
    L.append(card(x,704,196,100,t,rows,c))
    centers.append(x+98)
L.append('<path d="M600 660V684H128 M600 684H1072" fill="none" stroke="#7d6332" stroke-width="1.35"/>')
for i,cx in enumerate(centers):
    col=C['green'] if i==4 else C['amber']
    L.append(connector(f'M{cx} 684V704',col,'4.8s',f'{i*.6}s',packet=(i in (0,2,4))))
write(P/'experience-commerce-v2.svg',end(L,1200,840,'COMMERCE FLOW // PAYMENT CREDENTIALS STAY WITH THE PAYMENT PROVIDER'))

L=start(1200,820,'LEVIATHAN // PUBLIC DEVELOPER NETWORK','Eight repositories route into a large hub using separated lanes and seamless one-way packet motion.')
left=[
 ('LAUNCHER',['project • guides'],C['cyan']),
 ('DOCS',['ecosystem guides'],C['cyan']),
 ('SERVER TOOLS',['Minecraft utilities'],C['green']),
 ('EXAMPLES',['safe patterns'],C['violet']),
]
right=[
 ('API DOCS',['public contracts'],C['violet']),
 ('SDK',['developer tooling'],C['cyan']),
 ('INTEGRATIONS',['webhooks • adapters'],C['violet']),
 ('STATUS',['health • incidents'],C['green']),
]
ys=[108,268,428,588]
for i,(t,r,c) in enumerate(left):L.append(card(44,ys[i],250,94,t,r,c,f'0{i+1}'))
for i,(t,r,c) in enumerate(right):L.append(card(906,ys[i],250,94,t,r,c,f'0{i+5}'))
routes=[
 ('M294 155H390L486 254',left[0][2],'5.4s','0s',True),
 ('M294 315H410L472 326',left[1][2],'5.7s','.7s',False),
 ('M294 475H410L472 414',left[2][2],'6s','1.4s',False),
 ('M294 635H390L486 486',left[3][2],'6.3s','2.1s',True),
 ('M906 155H810L714 254',right[0][2],'5.5s','2.8s',True),
 ('M906 315H790L728 326',right[1][2],'5.8s','3.5s',False),
 ('M906 475H790L728 414',right[2][2],'6.1s','4.2s',False),
 ('M906 635H810L714 486',right[3][2],'6.4s','4.9s',True),
]
for d,c,dur,b,pkt in routes:L.append(connector(d,c,dur,b,pkt))
L.append(reactor(600,390,122,'LEVIATHAN','PUBLIC DEV HUB'))
write(P/'developer-network-v2.svg',end(L,1200,820,'PUBLIC REPOSITORIES ONLY // PROPRIETARY SOURCE AND PRIVATE SERVICE TOPOLOGY EXCLUDED'))

L=start(1200,630,'LEVIATHAN PROJECT SIGNAL // LIVE ROUTING FIELD','Four project domains exchange smooth one-way packets through a mechanical Leviathan reactor core.')
for x,y,t,rows,c,k in [
 (54,128,'PLAYER SYSTEMS',['LAUNCHER / CLIENT / APP'],C['cyan'],'01'),
 (876,128,'PLATFORM SYSTEMS',['AUTH / API / DATA / SERVICES'],C['violet'],'02'),
 (54,408,'SECURITY SYSTEMS',['ANTICHEAT / VERIFY / GUARD'],C['amber'],'03'),
 (876,408,'OPERATIONS',['TELEMETRY / RELEASE / STATUS'],C['green'],'04'),
]:L.append(card(x,y,270,102,t,rows,c,k))
for d,c,dur,b in [
 ('M324 179H430L488 236',C['cyan'],'5.3s','0s'),
 ('M876 179H770L712 236',C['violet'],'5.6s','.8s'),
 ('M324 459H430L488 400',C['amber'],'5.9s','1.6s'),
 ('M876 459H770L712 400',C['green'],'6.2s','2.4s'),
]:L.append(connector(d,c,dur,b))
L.append(reactor(600,320,116,'LEVIATHAN','PROJECT SIGNAL'))
write(P/'project-signal-v1.svg',end(L,1200,630,'DEEP SCAN // PUBLIC PROJECT SURFACE'))

print("Generated Leviathan profile visual system v6")