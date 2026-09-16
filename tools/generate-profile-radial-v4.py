from pathlib import Path
from html import escape as e
P=Path('assets/profile'); P.mkdir(parents=True,exist_ok=True)
C={'c':'#35e9ff','v':'#8b7cff','g':'#55e4ae','a':'#ffb44e'}
D='''<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#020811"/><stop offset=".54" stop-color="#061723"/><stop offset="1" stop-color="#020a12"/></linearGradient><linearGradient id="q"><stop stop-color="#087dff"/><stop offset=".5" stop-color="#35e9ff"/><stop offset="1" stop-color="#00a5ff"/></linearGradient><radialGradient id="rg"><stop stop-color="#70f7ff" stop-opacity=".7"/><stop offset=".3" stop-color="#21dfff" stop-opacity=".12"/><stop offset="1" stop-color="#02101a" stop-opacity="0"/></radialGradient><filter id="gl"><feGaussianBlur stdDeviation="3" result="x"/><feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="gr" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#12374d" opacity=".15"/></pattern></defs>'''
def S(w,h,t,s): return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',D,f'<rect width="{w}" height="{h}" rx="24" fill="url(#b)"/><rect width="{w}" height="{h}" rx="24" fill="url(#gr)"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="none" stroke="#173d52"/><text x="42" y="42" fill="#58eaff" font-family="monospace" font-size="14" letter-spacing="2.8">{e(t)}</text><text x="42" y="66" fill="#789aac" font-family="Arial" font-size="11">{e(s)}</text><path d="M42 84H{w-42}" stroke="#13384b"/><rect x="42" y="82" width="120" height="3" rx="2" fill="url(#q)" filter="url(#gl)"><animate attributeName="x" values="42;{w-162};42" dur="10s" repeatCount="indefinite"/></rect>']
def E(L,w,h,f='PUBLIC-SAFE SYSTEM VIEW // PRIVATE SOURCE, SECRETS AND SENSITIVE IMPLEMENTATION EXCLUDED'):
 L += [f'<text x="42" y="{h-22}" fill="#557b8f" font-family="monospace" font-size="8.5">{e(f)}</text>',f'<path d="M6 6H{w-6}V{h-6}H6Z" fill="none" stroke="url(#q)" stroke-width="2" stroke-dasharray="180 2400" filter="url(#gl)"><animate attributeName="stroke-dashoffset" values="0;-2580" dur="14s" repeatCount="indefinite"/></path></svg>']; return '\n'.join(L)
def W(n,x): P.joinpath(n).write_text(x,encoding='utf-8')
def card(x,y,w,h,t,it,c,k=''):
 z=f'<path d="M{x} {y}H{x+w-14}L{x+w} {y+14}V{y+h}H{x}Z" fill="#061722" stroke="{c}" stroke-opacity=".5"/>'; yy=y+24
 if k:z+=f'<text x="{x+18}" y="{yy}" fill="{c}" font-family="monospace" font-size="9">{e(k)}</text>';yy+=25
 z+=f'<text x="{x+18}" y="{yy}" fill="#effcff" font-family="Arial" font-size="14" font-weight="700">{e(t)}</text>';yy+=24
 for a in it:z+=f'<text x="{x+20}" y="{yy}" fill="#cfe8f0" font-family="monospace" font-size="8.8">{e(a)}</text>';yy+=20
 return z+f'<path d="M{x+18} {y+h-18}H{x+w-24}" stroke="{c}" stroke-opacity=".25" stroke-dasharray="18 10"><animate attributeName="stroke-dashoffset" values="0;-56" dur="3s" repeatCount="indefinite"/></path>'
def core(x,y,r,a,b,c=C['c']): return f'<g transform="translate({x} {y})"><circle r="{r+24}" fill="url(#rg)"/><circle r="{r+12}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="62 18 15 11" filter="url(#gl)"><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="16s" repeatCount="indefinite"/></circle><circle r="{r-7}" fill="none" stroke="#28718b" stroke-dasharray="26 12 7 10"><animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="11s" repeatCount="indefinite"/></circle><circle r="{max(18,r-34)}" fill="#04131d" stroke="{c}"/><circle r="4" fill="#a9fbff" filter="url(#gl)"/><text x="0" y="-3" text-anchor="middle" fill="#effcff" font-family="Arial" font-size="13" font-weight="700">{e(a)}</text><text x="0" y="14" text-anchor="middle" fill="#6aa1b5" font-family="monospace" font-size="7">{e(b)}</text></g>'
def con(i,d,c=C['c'],du='3s',be='0s'): return f'<path id="{i}" d="{d}" fill="none" stroke="{c}" stroke-width="1.6" stroke-opacity=".72"/><circle r="4" fill="#c0fbff" filter="url(#gl)"><animateMotion dur="{du}" begin="{be}" repeatCount="indefinite"><mpath href="#{i}"/></animateMotion></circle>'
def radial(name,title,sub,left,right,center=('LEVIATHAN','PLATFORM CORE'),h=590,r=96):
 L=S(1200,h,title,sub); ys=[108,238,368]
 for i,(t,it,c) in enumerate(left):L.append(card(44,ys[i],300,100,t,it,c,f'{i+1:02}'))
 for i,(t,it,c) in enumerate(right):L.append(card(856,ys[i],300,100,t,it,c,f'{i+4:02}'))
 paths=[('l1','M344 158H445L510 215'),('l2','M344 288H472'),('l3','M344 418H445L510 355'),('r1','M856 158H755L690 215'),('r2','M856 288H728'),('r3','M856 418H755L690 355')]
 cols=[x[2] for x in left+right]
 for j,(i,d) in enumerate(paths):L.append(con(i,d,cols[j],f'{3+j*.1}s',f'{j*.15}s'))
 L.append(core(600,288,r,*center)); W(name,E(L,1200,h))
# neural 4
L=S(1200,560,'LEVIATHAN NEURAL CORE // PUBLIC SYSTEM PROJECTION','Circular control model with anchored domains and source-to-core signal paths.')
for x,y,t,it,c,k in [(44,108,'PLAYER SOFTWARE',['LAUNCHER / CLIENT / APP / CAST'],C['c'],'DOMAIN 01'),(856,108,'PLATFORM SERVICES',['AUTH / API / INTEGRATIONS / ACCOUNTS'],C['v'],'DOMAIN 02'),(44,348,'PROTECTION & INTEGRITY',['NIMBUS / VALIDATION / EVIDENCE'],C['a'],'DOMAIN 03'),(856,348,'OBSERVABILITY',['TELEMETRY / ANALYTICS / STATUS'],C['g'],'DOMAIN 04')]:L.append(card(x,y,300,104,t,it,c,k))
for z in [('n1','M344 160H430L500 225',C['c']),('n2','M856 160H770L700 225',C['v']),('n3','M344 400H430L500 335',C['a']),('n4','M856 400H770L700 335',C['g'])]:L.append(con(*z))
L.append(core(600,280,112,'LEVIATHAN','NEURAL ROUTING CORE'));W('neural-core-v3.svg',E(L,1200,560))
# systems matrix
L=S(1200,730,'LEVIATHAN SYSTEMS MATRIX // PROJECT DIRECTORY','Six aligned project families routed through one compact public-safe control core.'); xs=[44,425,806]; ys=[106,442]
M=[('Play, launch and customize',['LAUNCHER','CLIENT','APP','UPDATER','INSTALLER','MODPACK STUDIO'],C['c'],'01 // PLAYER SYSTEMS'),('Identity, social and creation',['WEBSITE','DISCORD BOT','CREATOR STUDIO','COSMETICS','LINKS','VERIFY'],C['v'],'02 // WEB & COMMUNITY'),('Networks, routing and safety',['RELAY','SERVER MANAGER','SERVER GUARDIAN','SERVER TOOLS','NETWORK CONTROL'],C['g'],'03 // SERVER SYSTEMS'),('Detect, verify and diagnose',['NIMBUS ANTICHEAT','LEVIATHAN ANTICHEAT','SECURITY','INCIDENT RECORDER','CONFLICT DETECTIVE','DOCTOR'],C['a'],'04 // PROTECTION & INTEGRITY'),('Identity, data and entitlements',['API','AUTH','LICENSING','DATABASE','PLATFORM','VAULT'],C['v'],'05 // PLATFORM SERVICES'),('Build, observe and release',['DOCS / API DOCS / SDK','INTEGRATIONS / EXAMPLES / STATUS','TELEMETRY / ANALYTICS','RESEARCH / INFRASTRUCTURE','RELEASE ENGINEERING','CLAUDE SKILLS'],C['c'],'06 // DEVELOPER & OPS')]
for i,m in enumerate(M):L.append(card(xs[i%3],ys[i//3],350,210,m[0],m[1],m[2],m[3]))
for z in [('m1','M219 316V340H546L558 351',C['c']),('m2','M600 316V341',C['v']),('m3','M981 316V340H654L642 351',C['g']),('m4','M219 442V418H546L558 407',C['a']),('m5','M600 442V417',C['v']),('m6','M981 442V418H654L642 407',C['c'])]:L.append(con(*z))
L.append(core(600,379,34,'LINK','MATRIX CORE'));W('systems-matrix-v1.svg',E(L,1200,730,'DIRECTORY SIGNAL // PUBLIC PRODUCT NAMES AND FAMILIES ONLY'))
# three-domain radial panels
radial('data-platform-v2.svg','LEVIATHAN DATA PLATFORM // PUBLIC ARCHITECTURE DIRECTION','Every public data domain connects to one shared state and event core.',[('IDENTITY & ACCOUNTS',['USERS • PREFERENCES'],C['c']),('LAUNCHER & CLIENT',['PROFILE • INSTANCES • SETTINGS'],C['c']),('NIMBUS & SECURITY',['EVIDENCE • SIGNALS • AUDIT'],C['a'])],[('API & PLATFORM',['PROTOCOLS • INTEGRATIONS'],C['v']),('TELEMETRY & ANALYTICS',['PERFORMANCE • DIAGNOSTICS'],C['g']),('LICENSING & COMMERCE',['ORDERS • LICENSE STATE'],C['a'])],('POSTGRESQL','EVENTS • STATE • BACKUP'))
radial('core-products-v2.svg','LEVIATHAN // PRODUCT FAMILIES','Six product families share one connected platform core.',[('PLAYER SOFTWARE',['Launcher • Client • App','Profiles • Instances • Mods'],C['c']),('WEB & COMMUNITY',['Website • Profiles • Forum','Verify • Discord • Creator'],C['v']),('PROTECTION & INTEGRITY',['Nimbus • Leviathan AntiCheat','Security • Diagnostics'],C['a'])],[('SERVER ECOSYSTEM',['Relay • Manager • Guardian','Server Tools • Verification'],C['g']),('PLATFORM SERVICES',['API • Auth • Licensing','Database • Platform • Vault'],C['v']),('DEVELOPER & OPS',['SDK • Docs • Integrations','Analytics • Status • Research'],C['c'])],('LEVIATHAN','CONNECTED PLATFORM'))
# command core
L=S(1200,420,'LEVIATHAN COMMAND CORE // PROJECT OVERVIEW','Aligned state cards feed one operations dial; decorative dead space removed.')
for x,y,k,v,c in [(44,104,'ORCHESTRATION','MULTI-PROJECT',C['c']),(316,104,'VISIBILITY','PUBLIC + PRIVATE',C['c']),(44,208,'RELEASE MODE','COMPONENT-SPECIFIC',C['v']),(316,208,'VALIDATION','BUILD • TEST • HARDEN',C['a'])]:L.append(card(x,y,250,82,v,[],c,k))
L += [con('c1','M566 145H730L830 174',C['c']),con('c2','M566 249H730L830 222',C['v']),core(930,198,82,'ACTIVE','COMMAND DIAL'),'<path d="M630 338H1120" stroke="#17465c"/><circle r="4" fill="#73f3ff"><animateMotion dur="6s" repeatCount="indefinite" path="M630 338H1120"/></circle>'];W('command-core-v3.svg',E(L,1200,420))
# external trust route
L=S(1200,560,'IDENTITY & EXTERNAL SERVICE BOUNDARIES','Six trust stages route around one identity boundary core.'); N=[(92,128,'01 MICROSOFT','OAUTH',C['c']),(310,92,'02 XBOX LIVE','IDENTITY',C['c']),(710,92,'03 XSTS','AUTHORIZATION',C['v']),(928,128,'04 MINECRAFT','SERVICES',C['v']),(928,356,'05 OWNERSHIP','PROFILE',C['g']),(92,356,'06 LEVIATHAN','IDENTITY BOUNDARY',C['g'])]
for x,y,t,s,c in N:L.append(card(x,y,190,74,t,[s],c))
for z in [('e1','M282 165H395L515 230',C['c']),('e2','M500 129H540L565 197',C['c']),('e3','M710 129H660L635 197',C['v']),('e4','M928 165H805L685 230',C['v']),('e5','M928 393H805L685 330',C['g']),('e6','M282 393H395L515 330',C['g'])]:L.append(con(*z))
L.append(core(600,280,86,'TRUST ROUTE','IDENTITY BOUNDARY'));W('external-services-v2.svg',E(L,1200,560))
# ecosystem 4
L=S(1200,500,'LEVIATHAN ECOSYSTEM // PRODUCT SURFACES','Four aligned domains around one platform core.')
Q=[(60,110,'PLAYER SOFTWARE',['Launcher • Client • Profiles'],C['c']),(820,110,'PLATFORM',['Auth • API • Accounts'],C['v']),(60,322,'PROTECTION',['Nimbus • Security • Integrity'],C['a']),(820,322,'OBSERVABILITY',['Telemetry • Analytics • Status'],C['g'])]
for x,y,t,it,c in Q:L.append(card(x,y,320,104,t,it,c))
for z in [('q1','M380 162H475L525 215',C['c']),('q2','M820 162H725L675 215',C['v']),('q3','M380 374H475L525 321',C['a']),('q4','M820 374H725L675 321',C['g'])]:L.append(con(*z))
L.append(core(600,268,76,'LEVIATHAN','PLATFORM CORE'));W('ecosystem-overview-v2.svg',E(L,1200,500))
# platform areas 4 compact
L=S(1200,400,'LEVIATHAN // PLATFORM AREAS','Four platform domains anchored to one routing bus.')
for x,y,t,it,c in [(44,112,'PLAYER SOFTWARE',['Launcher • Client • Profiles'],C['c']),(44,250,'PROTECTION',['Nimbus • Security • Integrity'],C['a']),(856,112,'PLATFORM SERVICES',['Auth • API • Integrations'],C['v']),(856,250,'OBSERVABILITY',['Telemetry • Analytics • Status'],C['g'])]:L.append(card(x,y,300,92,t,it,c))
for z in [('p1','M344 158H470L520 185',C['c']),('p2','M344 296H470L520 265',C['a']),('p3','M856 158H730L680 185',C['v']),('p4','M856 296H730L680 265',C['g'])]:L.append(con(*z))
L.append(core(600,225,58,'PLATFORM','AREA BUS'));W('platform-areas-v2.svg',E(L,1200,400))
# roadmap
L=S(1200,640,'LEVIATHAN DEVELOPMENT PIPELINE // CONTINUOUS WORKSTREAMS','A circular pipeline dial drives eight aligned release phases.');L.append(core(210,336,112,'PIPELINE','RESEARCH → RELEASE'));ph=[('RESEARCH','ecosystem, compatibility, user needs',C['c']),('ARCHITECTURE','boundaries, APIs, data, security controls',C['c']),('BUILD','launcher, client, web, app, server, platform',C['c']),('INTEGRATION','auth, API, server links, device and web flows',C['c']),('SECURITY & INTEGRITY','anticheat, abuse controls, privacy, diagnostics',C['a']),('TEST & VALIDATE','compatibility, recovery, regression, devices',C['g']),('OPERATE & OBSERVE','telemetry, analytics, status, support, logs',C['v']),('RELEASE & IMPROVE','signing, distribution, docs, feedback',C['c'])]
for i,(t,d,c) in enumerate(ph):
 y=98+i*61;L.append(f'<circle cx="390" cy="{y+22}" r="7" fill="#061722" stroke="{c}" stroke-width="2"/><path d="M397 {y+22}H430" stroke="{c}"/><path d="M430 {y}H1128L1142 {y+14}V{y+44}H430Z" fill="#061722" stroke="#19445a"/><text x="452" y="{y+18}" fill="#effcff" font-family="Arial" font-size="13" font-weight="700">{e(t)}</text><text x="700" y="{y+18}" fill="#789aac" font-family="Arial" font-size="9">{e(d)}</text>')
L += ['<path id="rr" d="M390 120V547" stroke="#19495f" stroke-width="2"/><circle r="4" fill="#73f3ff"><animateMotion dur="7s" repeatCount="indefinite"><mpath href="#rr"/></animateMotion></circle>',con('rc','M322 336H390',C['c'])];W('roadmap-v2.svg',E(L,1200,640))
# tech stack
L=S(1200,300,'LEVIATHAN // DEVELOPMENT STACK','Compact orbital technology rail with no disconnected nodes.');T=[('JAVA 21','RUNTIME'),('JAVASCRIPT','WEB/UI'),('KOTLIN DSL','BUILD LOGIC'),('GRADLE','BUILD'),('HTML + CSS','PRESENTATION'),('POSTGRESQL','DATA'),('CI / CD','PIPELINE')];X=[100,265,430,595,760,925,1090]
for i,((a,b),x) in enumerate(zip(T,X)):
 L.append(f'<g transform="translate({x} 176)"><circle r="42" fill="#051621" stroke="#1d5c73"/><circle r="48" fill="none" stroke="#35e9ff" stroke-dasharray="34 13 8 10"><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="{10+i}s" repeatCount="indefinite"/></circle><circle r="3" fill="#8ff7ff"/><text x="0" y="-4" text-anchor="middle" fill="#effcff" font-family="Arial" font-size="10" font-weight="700">{e(a)}</text><text x="0" y="14" text-anchor="middle" fill="#6f96aa" font-family="monospace" font-size="7">{e(b)}</text></g>')
 if i<6:L.append(con(f't{i}',f'M{x+48} 176H{X[i+1]-48}',C['c'],f'{2.5+i*.1}s'))
W('tech-stack-v2.svg',E(L,1200,300))
# commerce two-core
L=S(1200,650,'LEVIATHAN EXPERIENCE + COMMERCE // PUBLIC DIRECTION','Surface state and commerce state are separate, explicitly connected systems.')
for x,w,t,it in [(44,150,'WEBSITE',['ACCOUNT • STORE • SUPPORT']),(318,190,'MOBILE APP',['ACCOUNT • COSMETICS • ALERTS']),(856,150,'LAUNCHER',['PROFILES • INSTANCES • STORE']),(1030,126,'CLIENT',['COSMETICS • ENTITLEMENT'])]:L.append(card(x,104,w,92,t,it,C['c']))
L += [core(600,190,66,'PLATFORM','AUTH • API • ACCOUNT'),con('x1','M194 150H410L535 175'),con('x2','M508 150H540L540 165'),con('x3','M856 150H790L665 175'),con('x4','M1030 150H790L665 205'),con('xb','M600 256V360',C['v']),core(600,430,58,'ENTITLEMENT','ORDER • LICENSE • WALLET',C['v'])]
for i,(t,x,c) in enumerate([('STORE / CATALOG',60,C['a']),('CHECKOUT',280,C['a']),('PAYMENT PROVIDER',500,C['a']),('ORDER VERIFY',720,C['a']),('GROWTH / ATTRIBUTION',940,C['g'])]):L += [card(x,520,200,78,t,['PUBLIC FLOW'],c),con(f'xc{i}',f'M{x+100} 520V500L600 488',c)]
W('experience-commerce-v2.svg',E(L,1200,650,'COMMERCE FLOW // PAYMENT CREDENTIALS STAY WITH THE PAYMENT PROVIDER'))
# developer hub
L=S(1200,520,'LEVIATHAN // PUBLIC DEVELOPER NETWORK','Eight public repositories route into one developer hub.');N=[(90,118,'LAUNCHER','project • guides'),(330,92,'DOCS','ecosystem guides'),(730,92,'API DOCS','public contracts'),(970,118,'SDK','developer tooling'),(90,350,'SERVER TOOLS','Minecraft utilities'),(330,376,'EXAMPLES','code patterns'),(730,376,'INTEGRATIONS','webhooks • adapters'),(970,350,'STATUS','health • incidents')]
for x,y,t,s in N:L.append(card(x,y,140,74,t,[s],C['c']))
for i,d in enumerate(['M230 155H410L520 220','M470 129L545 205','M730 129L655 205','M970 155H790L680 220','M230 387H410L520 300','M470 413L545 315','M730 413L655 315','M970 387H790L680 300']):L.append(con(f'd{i}',d,C['c']))
L.append(core(600,260,82,'LEVIATHAN','PUBLIC DEV HUB'));W('developer-network-v2.svg',E(L,1200,520))
# project signal
L=S(1200,500,'LEVIATHAN PROJECT SIGNAL // LIVE ROUTING FIELD','Four operating domains route through one restrained circular signal core.')
for x,y,t,it,c in [(80,108,'PLAYER SYSTEMS',['LAUNCHER • CLIENT • APP'],C['c']),(840,108,'PLATFORM SYSTEMS',['AUTH • API • DATA • SERVICES'],C['v']),(80,350,'SECURITY SYSTEMS',['ANTICHEAT • VERIFY • GUARD'],C['a']),(840,350,'OPERATIONS',['TELEMETRY • RELEASE • STATUS'],C['g'])]:L.append(card(x,y,280,86,t,it,c))
for z in [('s1','M360 151H450L510 205',C['c']),('s2','M840 151H750L690 205',C['v']),('s3','M360 393H450L510 325',C['a']),('s4','M840 393H750L690 325',C['g'])]:L.append(con(*z))
L.append(core(600,265,96,'LEVIATHAN.LINK','PROJECT SIGNAL CORE'));W('project-signal-v1.svg',E(L,1200,500))
print('Generated radial profile panels.')
