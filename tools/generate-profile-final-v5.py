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
  <stop stop-color="#8ff9ff" stop-opacity=".55"/><stop offset=".28" stop-color="#22dfff" stop-opacity=".15"/><stop offset="1" stop-color="#02101a" stop-opacity="0"/>
</radialGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
  <feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
  <path d="M28 0H0V28" fill="none" stroke="#12374d" opacity=".14"/>
</pattern>
</defs>'''

def write(path: Path, text: str):
    path.write_text(text, encoding="utf-8", newline="\n")

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
        '<rect x="42" y="84" width="120" height="3" rx="1.5" fill="url(#edge)" filter="url(#glow)">'
        f'<animate attributeName="x" values="42;{w-162};42" dur="12s" repeatCount="indefinite"/></rect>',
    ]

def end(lines, w, h, footer="PUBLIC-SAFE SYSTEM VIEW // PRIVATE SOURCE, SECRETS AND SENSITIVE IMPLEMENTATION EXCLUDED"):
    lines += [
        f'<text x="42" y="{h-22}" fill="#557b8f" font-family="ui-monospace,Consolas,monospace" font-size="8.5">{esc(footer)}</text>',
        f'<path d="M6 6H{w-6}V{h-6}H6Z" fill="none" stroke="url(#edge)" stroke-width="2" stroke-dasharray="170 2500" filter="url(#glow)" opacity=".85">'
        '<animate attributeName="stroke-dashoffset" values="0;-2670" dur="18s" repeatCount="indefinite"/></path>',
        '</svg>',
    ]
    return "\n".join(lines)

def card(x, y, w, h, title, rows, color, eyebrow=""):
    a = ['<g>']
    a.append(f'<path d="M{x} {y}H{x+w-14}L{x+w} {y+14}V{y+h}H{x}Z" fill="{C["panel"]}" stroke="{color}" stroke-opacity=".52"/>')
    yy = y + 24
    if eyebrow:
        a.append(f'<text x="{x+18}" y="{yy}" fill="{color}" font-family="ui-monospace,Consolas,monospace" font-size="9">{esc(eyebrow)}</text>')
        yy += 25
    a.append(f'<text x="{x+18}" y="{yy}" fill="{C["white"]}" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="700">{esc(title)}</text>')
    yy += 23
    for row in rows:
        a.append(f'<text x="{x+20}" y="{yy}" fill="#cae5ed" font-family="ui-monospace,Consolas,monospace" font-size="8.6">{esc(row)}</text>')
        yy += 19
    a.append(f'<path d="M{x+18} {y+h-17}H{x+w-24}" stroke="{color}" stroke-opacity=".22" stroke-dasharray="18 10"/>')
    a.append('</g>')
    return "".join(a)

def reactor(x, y, r, label="LEVIATHAN", sub="ENERGY CORE", color=None):
    color = color or C["cyan"]
    blades = []
    for ang in range(0, 360, 60):
        blades.append(
            f'<g transform="rotate({ang})"><path d="M0 {-r+15} L-8 {-r+34} L8 {-r+34} Z" '
            f'fill="{color}" fill-opacity=".16" stroke="{color}" stroke-opacity=".62"/></g>'
        )
    return f'''<g transform="translate({x} {y})">
<circle r="{r+30}" fill="url(#energy)"/>
<circle r="{r+16}" fill="none" stroke="{color}" stroke-width="2.4" stroke-dasharray="42 16 9 12" filter="url(#glow)">
  <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="22s" repeatCount="indefinite"/>
</circle>
<circle r="{r+4}" fill="none" stroke="#2a7590" stroke-width="1.1" stroke-dasharray="18 15">
  <animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="16s" repeatCount="indefinite"/>
</circle>
{''.join(blades)}
<polygon points="0,-{int(r*.50)} {int(r*.44)},-{int(r*.25)} {int(r*.44)},{int(r*.25)} 0,{int(r*.50)} -{int(r*.44)},{int(r*.25)} -{int(r*.44)},-{int(r*.25)}"
 fill="#04131d" stroke="{color}" stroke-width="1.4"/>
<path d="M-16 -19V16H15 M-16 -19L-3 -28M15 16L24 7" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)">
  <animate attributeName="stroke-opacity" values=".68;1;.68" dur="3.8s" repeatCount="indefinite"/>
</path>
<text x="0" y="{int(r*.66)}" text-anchor="middle" fill="{C["white"]}" font-family="Segoe UI,Arial,sans-serif" font-size="12" font-weight="700">{esc(label)}</text>
<text x="0" y="{int(r*.66)+16}" text-anchor="middle" fill="#6b9aad" font-family="ui-monospace,Consolas,monospace" font-size="7">{esc(sub)}</text>
</g>'''

def connector(pid, d, color, dur="4s", begin="0s", packet=True, opacity=.72):
    s = [f'<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-width="1.55" stroke-opacity="{opacity}"/>']
    if packet:
        s.append(
            f'<circle r="3.7" fill="#c9fbff" filter="url(#glow)" opacity="0">'
            f'<animateMotion dur="{dur}" begin="{begin}" repeatCount="indefinite" calcMode="paced"><mpath href="#{pid}"/></animateMotion>'
            f'<animate attributeName="opacity" dur="{dur}" begin="{begin}" repeatCount="indefinite" '
            f'values="0;1;1;0;0" keyTimes="0;.08;.78;.9;1"/></circle>'
        )
    return "".join(s)

def label_line(x1, y1, x2, y2, text):
    return f'<path d="M{x1} {y1}H{x2}" stroke="#17465b"/><text x="{x1}" y="{y1-9}" fill="#6f93a6" font-family="ui-monospace,Consolas,monospace" font-size="8">{esc(text)}</text>'

def make_hero(light=False):
    w, h = 1200, 520
    if light:
        bg = '#eef8fc'
        panel = '#ffffff'
        text = '#08202d'
        muted = '#486c7f'
        grid = '#8bc3d8'
    else:
        bg = '#020811'
        panel = '#061722'
        text = '#effcff'
        muted = '#82a1b2'
        grid = '#12374d'
    defs = DEFS.replace('#020811', bg).replace('#061723', bg).replace('#020a12', bg).replace('#061722', panel).replace('#12374d', grid)
    L = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        defs,
        f'<rect width="{w}" height="{h}" rx="26" fill="{bg}"/><rect width="{w}" height="{h}" rx="26" fill="url(#grid)" opacity=".75"/>',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="25" fill="none" stroke="#1b5169"/>',
        '<text x="42" y="30" fill="#6394aa" font-family="monospace" font-size="8" letter-spacing="2">LEVIATHAN SYSTEM</text>',
        '<text x="202" y="30" fill="#35e9ff" font-family="monospace" font-size="8" letter-spacing="2">HOLOGRAPHIC PROJECT INTERFACE</text>',
        '<text x="1054" y="30" fill="#55e4ae" font-family="monospace" font-size="8" letter-spacing="2">SIGNAL ONLINE</text>',
        '<path d="M42 44H1158" stroke="#17445a"/>',
        '<rect x="42" y="76" width="4" height="248" rx="2" fill="#35e9ff" filter="url(#glow)"/>',
        '<text x="72" y="105" fill="#35e9ff" font-family="monospace" font-size="13" letter-spacing="3">LEVIATHAN // SYSTEM READY</text>',
        f'<text x="72" y="186" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="64" font-weight="800">LEVIATHAN</text>',
        f'<text x="72" y="224" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="18">Connected Minecraft software, services and infrastructure.</text>',
        '<text x="72" y="254" fill="#55e4ae" font-family="monospace" font-size="9">CHANNEL // PLAYER + PLATFORM + OPS</text>',
        f'<text x="72" y="286" fill="{muted}" font-family="monospace" font-size="9">LAUNCHER • CLIENT • WEB • APP • SERVERS • SECURITY • API • DATA • OPERATIONS</text>',
        f'<path d="M72 318H560L576 334V398H72Z" fill="{panel}" stroke="#1b536b"/>',
        '<text x="94" y="343" fill="#638da1" font-family="monospace" font-size="8">SYSTEM FAMILIES</text>',
        f'<text x="94" y="373" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">6 CONNECTED DOMAINS</text>',
        '<text x="292" y="343" fill="#638da1" font-family="monospace" font-size="8">VISIBILITY</text>',
        f'<text x="292" y="373" fill="{text}" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">PUBLIC + PRIVATE</text>',
        '<text x="462" y="343" fill="#638da1" font-family="monospace" font-size="8">STATUS</text>',
        '<text x="462" y="373" fill="#35e9ff" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700">PER PRODUCT</text>',
        card(690, 104, 180, 78, 'PLAYER', ['LAUNCH / CLIENT'], C['cyan'], '01'),
        card(1000, 104, 160, 78, 'PLATFORM', ['API / AUTH'], C['violet'], '02'),
        card(690, 338, 180, 78, 'SECURITY', ['VERIFY / GUARD'], C['amber'], '03'),
        card(1000, 338, 160, 78, 'OPERATIONS', ['DATA / STATUS'], C['green'], '04'),
        connector('hp1', 'M870 143H902L925 170', C['cyan'], '4.5s', '0s'),
        connector('hp2', 'M1000 143H968L945 170', C['violet'], '4.7s', '.6s'),
        connector('hp3', 'M870 377H902L925 350', C['amber'], '4.9s', '1.2s'),
        connector('hp4', 'M1000 377H968L945 350', C['green'], '5.1s', '1.8s'),
        reactor(935, 260, 82, 'LEVIATHAN', 'PROJECT CORE'),
        '<path d="M42 448H1158" stroke="#154052"/>',
        '<text x="42" y="474" fill="#5f8296" font-family="monospace" font-size="8">PUBLIC SURFACE  //  WEBSITE / PROFILE / DOCS / SDK / API / EXAMPLES / INTEGRATIONS / STATUS</text>',
        '<text x="868" y="474" fill="#55e4ae" font-family="monospace" font-size="8">SYSTEM NORMAL</text>',
        '<text x="1045" y="474" fill="#35e9ff" font-family="monospace" font-size="8">ACTIVE</text>',
        '<path d="M8 8H1192V512H8Z" fill="none" stroke="url(#edge)" stroke-width="2.4" stroke-dasharray="220 2400" filter="url(#glow)"><animate attributeName="stroke-dashoffset" values="0;-2620" dur="18s" repeatCount="indefinite"/></path>',
        '</svg>',
    ]
    return "\n".join(L)

write(ROOT / "hero-dark-v4.svg", make_hero(False))
write(ROOT / "hero-light-v4.svg", make_hero(True))

L = start(1200, 470, 'LEVIATHAN COMMAND CORE // PROJECT OVERVIEW', 'Four project-state inputs feed one branded operations core.')
for x,y,k,v,c in [
    (44,110,'ORCHESTRATION','MULTI-PROJECT',C['cyan']),
    (320,110,'VISIBILITY','PUBLIC + PRIVATE',C['cyan']),
    (44,218,'RELEASE MODE','COMPONENT-SPECIFIC',C['violet']),
    (320,218,'VALIDATION','BUILD • TEST • HARDEN',C['amber']),
]:
    L.append(card(x,y,250,88,v,[],c,k))
L += [
    connector('cc1','M570 154H720L804 196',C['cyan'],'4.6s','0s'),
    connector('cc2','M570 262H720L804 236',C['violet'],'4.9s','.9s'),
    reactor(920,218,92,'LEVIATHAN','COMMAND CORE'),
    label_line(650, 376, 1115, 376, 'ACTIVE DEVELOPMENT // STATUS RAIL'),
    '<rect x="650" y="391" width="465" height="4" rx="2" fill="#173f53"/>',
    '<rect x="650" y="391" width="120" height="4" rx="2" fill="#35e9ff"><animate attributeName="x" values="650;995;650" dur="10s" repeatCount="indefinite"/></rect>',
]
write(P/'command-core-v3.svg', end(L,1200,470))

L = start(1200, 620, 'LEVIATHAN NEURAL CORE // PUBLIC SYSTEM PROJECTION', 'Four balanced domains route through a larger Leviathan energy core.')
for x,y,t,r,c,k in [
    (44,118,'PLAYER SOFTWARE',['LAUNCHER / CLIENT / APP / CAST'],C['cyan'],'DOMAIN 01'),
    (856,118,'PLATFORM SERVICES',['AUTH / API / INTEGRATIONS / ACCOUNTS'],C['violet'],'DOMAIN 02'),
    (44,392,'PROTECTION & INTEGRITY',['NIMBUS / VALIDATION / EVIDENCE'],C['amber'],'DOMAIN 03'),
    (856,392,'OBSERVABILITY',['TELEMETRY / ANALYTICS / STATUS'],C['green'],'DOMAIN 04'),
]:
    L.append(card(x,y,300,106,t,r,c,k))
for z in [
    ('nn1','M344 171H430L490 226',C['cyan'],'4.4s','0s'),
    ('nn2','M856 171H770L710 226',C['violet'],'4.6s','.8s'),
    ('nn3','M344 445H430L490 390',C['amber'],'4.8s','1.6s'),
    ('nn4','M856 445H770L710 390',C['green'],'5s','2.4s'),
]:
    L.append(connector(*z))
L.append(reactor(600,308,112,'LEVIATHAN','NEURAL CORE'))
write(P/'neural-core-v3.svg', end(L,1200,620))

L = start(1200, 830, 'LEVIATHAN SYSTEMS MATRIX // PROJECT DIRECTORY', 'Six aligned project families with a larger center core and cleaner routing lanes.')
xs=[44,425,806]
yt,yb=108,540
matrix=[
    ('Play, launch and customize',['LAUNCHER','CLIENT','APP','UPDATER','INSTALLER','MODPACK STUDIO'],C['cyan'],'01 // PLAYER SYSTEMS'),
    ('Identity, social and creation',['WEBSITE','DISCORD BOT','CREATOR STUDIO','COSMETICS','LINKS','VERIFY'],C['violet'],'02 // WEB & COMMUNITY'),
    ('Networks, routing and safety',['RELAY','SERVER MANAGER','SERVER GUARDIAN','SERVER TOOLS','NETWORK CONTROL'],C['green'],'03 // SERVER SYSTEMS'),
    ('Detect, verify and diagnose',['NIMBUS ANTICHEAT','LEVIATHAN ANTICHEAT','SECURITY','INCIDENT RECORDER','CONFLICT DETECTIVE','DOCTOR'],C['amber'],'04 // PROTECTION & INTEGRITY'),
    ('Identity, data and entitlements',['API','AUTH','LICENSING','DATABASE','PLATFORM','VAULT'],C['violet'],'05 // PLATFORM SERVICES'),
    ('Build, observe and release',['DOCS / API DOCS / SDK','INTEGRATIONS / EXAMPLES / STATUS','TELEMETRY / ANALYTICS','RESEARCH / INFRASTRUCTURE','RELEASE ENGINEERING','CLAUDE SKILLS'],C['cyan'],'06 // DEVELOPER & OPS'),
]
for i,m in enumerate(matrix):
    L.append(card(xs[i%3], yt if i<3 else yb, 350, 220, m[0],m[1],m[2],m[3]))
L += [
    connector('sm1','M219 328V365H500',C['cyan'],'5.2s','0s'),
    connector('sm2','M600 328V355',C['violet'],'4.7s','.7s',packet=False),
    connector('sm3','M981 328V365H700',C['green'],'5.4s','1.4s'),
    connector('sm4','M219 540V503H500',C['amber'],'5.3s','2.1s'),
    connector('sm5','M600 540V513',C['violet'],'4.9s','2.8s',packet=False),
    connector('sm6','M981 540V503H700',C['cyan'],'5.5s','3.5s'),
    connector('smc1','M500 365H530',C['cyan'],'4s','0s',packet=False),
    connector('smc2','M700 365H670',C['green'],'4s','0s',packet=False),
    connector('smc3','M500 503H530',C['amber'],'4s','0s',packet=False),
    connector('smc4','M700 503H670',C['cyan'],'4s','0s',packet=False),
    reactor(600,434,58,'LEVIATHAN','MATRIX CORE'),
]
write(P/'systems-matrix-v1.svg', end(L,1200,830,'DIRECTORY SIGNAL // PUBLIC PRODUCT NAMES AND FAMILIES ONLY'))

def radial_six(filename,title,subtitle,left,right,center_label,center_sub):
    L=start(1200,650,title,subtitle)
    ys=[116,270,424]
    for i,(t,rows,c) in enumerate(left):
        L.append(card(44,ys[i],300,112,t,rows,c,f'{i+1:02}'))
    for i,(t,rows,c) in enumerate(right):
        L.append(card(856,ys[i],300,112,t,rows,c,f'{i+4:02}'))
    paths=[
        ('r1','M344 172H430L490 230',left[0][2],'4.5s','0s'),
        ('r2','M344 326H468',left[1][2],'4.7s','.6s'),
        ('r3','M344 480H430L490 422',left[2][2],'4.9s','1.2s'),
        ('r4','M856 172H770L710 230',right[0][2],'5.1s','1.8s'),
        ('r5','M856 326H732',right[1][2],'5.3s','2.4s'),
        ('r6','M856 480H770L710 422',right[2][2],'5.5s','3s'),
    ]
    for p in paths: L.append(connector(*p))
    L.append(reactor(600,326,96,center_label,center_sub))
    write(P/filename,end(L,1200,650))

radial_six(
    'data-platform-v2.svg',
    'LEVIATHAN DATA PLATFORM // PUBLIC ARCHITECTURE DIRECTION',
    'Every public data domain connects to one shared state and event core.',
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
    'Six product families share one connected Leviathan core.',
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
    'LEVIATHAN','CONNECTED PLATFORM'
)

L=start(1200,650,'IDENTITY & EXTERNAL SERVICE BOUNDARIES','Six trust stages route around a single Leviathan identity boundary core.')
nodes=[
    (64,122,'01 MICROSOFT',['OAUTH'],C['cyan']),
    (282,104,'02 XBOX LIVE',['IDENTITY'],C['cyan']),
    (728,104,'03 XSTS',['AUTHORIZATION'],C['violet']),
    (946,122,'04 MINECRAFT',['SERVICES'],C['violet']),
    (946,424,'05 OWNERSHIP',['PROFILE'],C['green']),
    (64,424,'06 LEVIATHAN',['IDENTITY BOUNDARY'],C['green']),
]
for n in nodes:L.append(card(n[0],n[1],190,84,n[2],n[3],n[4]))
for p in [
    ('ex1','M254 164H380L500 246',C['cyan'],'5s','0s'),
    ('ex2','M472 146H515L545 215',C['cyan'],'5.2s','.7s'),
    ('ex3','M728 146H685L655 215',C['violet'],'5.4s','1.4s'),
    ('ex4','M946 164H820L700 246',C['violet'],'5.6s','2.1s'),
    ('ex5','M946 466H820L700 404',C['green'],'5.8s','2.8s'),
    ('ex6','M254 466H380L500 404',C['green'],'6s','3.5s'),
]:L.append(connector(*p))
L.append(reactor(600,325,92,'TRUST ROUTE','IDENTITY BOUNDARY'))
write(P/'external-services-v2.svg',end(L,1200,650))

L=start(1200,670,'LEVIATHAN DEVELOPMENT PIPELINE // CONTINUOUS WORKSTREAMS','A circular pipeline dial drives eight aligned release phases.')
L.append(reactor(208,348,108,'PIPELINE','RESEARCH • RELEASE'))
phases=[
    ('01','RESEARCH','ecosystem, compatibility, user needs'),
    ('02','ARCHITECTURE','boundaries, APIs, data, security controls'),
    ('03','BUILD','launcher, client, web, app, server, platform'),
    ('04','INTEGRATION','auth, API, server links, devices, cross-product flows'),
    ('05','SECURITY & INTEGRITY','anticheat, abuse controls, privacy, diagnostics'),
    ('06','TEST & VALIDATE','compatibility, recovery, regression, devices'),
    ('07','OPERATE & OBSERVE','telemetry, analytics, status, support, logs'),
    ('08','RELEASE & IMPROVE','signing, distribution, docs, feedback'),
]
L += [
    '<path id="roadspine" d="M360 126V570" fill="none" stroke="#25829d" stroke-width="2"/>',
    '<circle r="4" fill="#b8fbff" filter="url(#glow)" opacity="0"><animateMotion dur="9s" repeatCount="indefinite" calcMode="paced"><mpath href="#roadspine"/></animateMotion><animate attributeName="opacity" dur="9s" repeatCount="indefinite" values="0;1;1;0;0" keyTimes="0;.04;.9;.96;1"/></circle>',
]
y=105
for i,(num,title,desc) in enumerate(phases):
    cy=y+22
    col = C['amber'] if i==4 else C['green'] if i==5 else C['violet'] if i==6 else C['cyan']
    L += [
        f'<circle cx="360" cy="{cy}" r="6" fill="#061722" stroke="{col}" stroke-width="2"/>',
        f'<path d="M366 {cy}H395" stroke="{col}" stroke-opacity=".7"/>',
        f'<path d="M395 {y}H1138L1150 {y+12}V{y+44}H395Z" fill="#061722" stroke="#1a4c61"/>',
        f'<text x="418" y="{y+27}" fill="#effcff" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">{esc(title)}</text>',
        f'<text x="660" y="{y+27}" fill="#7ea4b6" font-family="ui-monospace,Consolas,monospace" font-size="8.5">{esc(desc)}</text>',
    ]
    y += 58
L.append(connector('roadlink','M316 348H360',C['cyan'],'4.4s','1s'))
write(P/'roadmap-v2.svg',end(L,1200,670))

L=start(1200,560,'LEVIATHAN ECOSYSTEM // PRODUCT SURFACES','Four platform domains surround one shared Leviathan core.')
for x,y,t,rows,c,k in [
    (54,116,'PLAYER SOFTWARE',['Launcher • Client • Profiles'],C['cyan'],'01'),
    (826,116,'PLATFORM SERVICES',['Auth • API • Accounts'],C['violet'],'02'),
    (54,354,'PROTECTION',['Nimbus • Security • Integrity'],C['amber'],'03'),
    (826,354,'OBSERVABILITY',['Telemetry • Analytics • Status'],C['green'],'04'),
]:L.append(card(x,y,320,108,t,rows,c,k))
for p in [
    ('eco1','M374 170H470L510 216',C['cyan'],'4.8s','0s'),
    ('eco2','M826 170H730L690 216',C['violet'],'5s','.8s'),
    ('eco3','M374 408H470L510 362',C['amber'],'5.2s','1.6s'),
    ('eco4','M826 408H730L690 362',C['green'],'5.4s','2.4s'),
]:L.append(connector(*p))
L.append(reactor(600,289,84,'LEVIATHAN','PLATFORM CORE'))
write(P/'ecosystem-overview-v2.svg',end(L,1200,560))

L=start(1200,520,'LEVIATHAN // PLATFORM AREAS','Four domains connect through one central routing core, with no floating bus geometry.')
for x,y,t,rows,c,k in [
    (54,116,'PLAYER SOFTWARE',['Launcher • Client • Profiles','Instances • Updates'],C['cyan'],'SURFACE 01'),
    (826,116,'PLATFORM SERVICES',['Authentication • APIs • Accounts','SDK • Integrations'],C['violet'],'SURFACE 02'),
    (54,322,'PROTECTION',['Nimbus • Security • Integrity','Reliability • Diagnostics'],C['amber'],'SURFACE 03'),
    (826,322,'OBSERVABILITY',['Telemetry • Analytics • Logging','Monitoring • Status'],C['green'],'SURFACE 04'),
]:L.append(card(x,y,320,112,t,rows,c,k))
for p in [
    ('pa1','M374 172H470L510 215',C['cyan'],'4.7s','0s'),
    ('pa2','M826 172H730L690 215',C['violet'],'4.9s','.7s'),
    ('pa3','M374 378H470L510 335',C['amber'],'5.1s','1.4s'),
    ('pa4','M826 378H730L690 335',C['green'],'5.3s','2.1s'),
]:L.append(connector(*p))
L.append(reactor(600,275,82,'LEVIATHAN','ROUTING CORE'))
write(P/'platform-areas-v2.svg',end(L,1200,520))

L=start(1200,790,'LEVIATHAN EXPERIENCE + COMMERCE // PUBLIC DIRECTION','Player surfaces, platform state and entitlement flow use separate, explicit routing lanes.')
tops=[
    (44,'WEBSITE',['ACCOUNT • STORE • SUPPORT'],C['cyan']),
    (320,'MOBILE APP',['ACCOUNT • COSMETICS • ALERTS'],C['cyan']),
    (816,'LAUNCHER',['PROFILES • INSTANCES • STORE'],C['cyan']),
    (1010,'CLIENT',['COSMETICS • ENTITLEMENT'],C['cyan']),
]
for x,t,rows,c in tops:L.append(card(x,112,150 if x==1010 else 190,100,t,rows,c))
L += [
    connector('cm1','M234 162H390L494 214',C['cyan'],'5.6s','0s'),
    connector('cm2','M510 162H470L494 232',C['cyan'],'5.2s','.8s',packet=False),
    connector('cm3','M816 162H710L706 214',C['cyan'],'5.8s','1.6s'),
    connector('cm4','M1010 162H810L706 232',C['cyan'],'5.4s','2.4s',packet=False),
    reactor(600,245,78,'PLATFORM','AUTH • API • STATE'),
    connector('cm5','M600 353V430',C['violet'],'5.2s','.6s'),
    reactor(600,510,58,'ENTITLEMENT','ORDER • LICENSE • WALLET',C['violet']),
]
bottom=[
    (34,'STORE / CATALOG',['PUBLIC FLOW'],C['amber']),
    (270,'CHECKOUT',['PUBLIC FLOW'],C['amber']),
    (506,'PAYMENT PROVIDER',['EXTERNAL BOUNDARY'],C['amber']),
    (742,'ORDER VERIFY',['PUBLIC FLOW'],C['amber']),
    (978,'GROWTH / ATTRIBUTION',['PUBLIC FLOW'],C['green']),
]
centers=[]
for x,t,rows,c in bottom:
    L.append(card(x,642,188,104,t,rows,c))
    centers.append(x+94)
L.append('<path d="M600 598V620H128 M600 620H1072" fill="none" stroke="#7d6332" stroke-width="1.4"/>')
for i,cx in enumerate(centers):
    col = C['green'] if i==4 else C['amber']
    L.append(connector(f'cb{i}',f'M{cx} 620V642',col,'4.6s',f'{i*.45}s',packet=(i in (0,2,4))))
write(P/'experience-commerce-v2.svg',end(L,1200,790,'COMMERCE FLOW // PAYMENT CREDENTIALS STAY WITH THE PAYMENT PROVIDER'))

L=start(1200,720,'LEVIATHAN // PUBLIC DEVELOPER NETWORK','Eight public repositories route through one spacious developer hub.')
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
ys=[108,244,380,516]
for i,(t,r,c) in enumerate(left):L.append(card(54,ys[i],250,92,t,r,c,f'0{i+1}'))
for i,(t,r,c) in enumerate(right):L.append(card(896,ys[i],250,92,t,r,c,f'0{i+5}'))
paths=[
    ('dn1','M304 154H410L510 246',left[0][2],'5.1s','0s'),
    ('dn2','M304 290H430L492 300',left[1][2],'5.3s','.6s'),
    ('dn3','M304 426H430L492 382',left[2][2],'5.5s','1.2s'),
    ('dn4','M304 562H410L510 430',left[3][2],'5.7s','1.8s'),
    ('dn5','M896 154H790L690 246',right[0][2],'5.2s','2.4s'),
    ('dn6','M896 290H770L708 300',right[1][2],'5.4s','3s'),
    ('dn7','M896 426H770L708 382',right[2][2],'5.6s','3.6s'),
    ('dn8','M896 562H790L690 430',right[3][2],'5.8s','4.2s'),
]
for p in paths:L.append(connector(*p))
L.append(reactor(600,356,96,'LEVIATHAN','PUBLIC DEV HUB'))
write(P/'developer-network-v2.svg',end(L,1200,720,'PUBLIC REPOSITORIES ONLY // PROPRIETARY SOURCE AND PRIVATE SERVICE TOPOLOGY EXCLUDED'))

L=start(1200,560,'LEVIATHAN PROJECT SIGNAL // LIVE ROUTING FIELD','Four project domains exchange one-way packets through a branded Leviathan core.')
for x,y,t,r,c,k in [
    (54,120,'PLAYER SYSTEMS',['LAUNCHER / CLIENT / APP'],C['cyan'],'01'),
    (876,120,'PLATFORM SYSTEMS',['AUTH / API / DATA / SERVICES'],C['violet'],'02'),
    (54,356,'SECURITY SYSTEMS',['ANTICHEAT / VERIFY / GUARD'],C['amber'],'03'),
    (876,356,'OPERATIONS',['TELEMETRY / RELEASE / STATUS'],C['green'],'04'),
]:L.append(card(x,y,270,100,t,r,c,k))
for p in [
    ('ps1','M324 170H430L500 226',C['cyan'],'4.8s','0s'),
    ('ps2','M876 170H770L700 226',C['violet'],'5s','.8s'),
    ('ps3','M324 406H430L500 350',C['amber'],'5.2s','1.6s'),
    ('ps4','M876 406H770L700 350',C['green'],'5.4s','2.4s'),
]:L.append(connector(*p))
L.append(reactor(600,288,98,'LEVIATHAN','PROJECT SIGNAL'))
write(P/'project-signal-v1.svg',end(L,1200,560,'DEEP SCAN // PUBLIC PROJECT SURFACE'))

L=start(1200,420,'LEVIATHAN // DEVELOPMENT STACK','High-level technologies arranged on a clean execution rail.')
L.append(reactor(160,235,64,'STACK','BUILD CORE'))
stack=[('JAVA 21','RUNTIME'),('KOTLIN DSL','BUILD LOGIC'),('HTML + CSS','PRESENTATION'),('JSON / YAML','CONFIG'),('JAVASCRIPT','WEB / UI'),('GRADLE','BUILD'),('POSTGRESQL','DATA'),('CI / CD','PIPELINES')]
x=285
for i,(a,b) in enumerate(stack):
    yy=116 if i<4 else 244
    xx=x+(i%4)*215
    L.append(card(xx,yy,180,80,a,[b],C['cyan'] if i%3==0 else C['violet'] if i%3==1 else C['green']))
L += [
    '<path d="M224 235H278" stroke="#35e9ff" stroke-width="1.6"/>',
    '<path d="M278 214H1130" stroke="#17495e"/>',
    '<path d="M278 342H1130" stroke="#17495e"/>',
]
write(P/'tech-stack-v2.svg',end(L,1200,420))

print("Generated Leviathan profile visual system v5")
