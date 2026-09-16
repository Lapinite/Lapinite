from pathlib import Path
import math
import re

ROOT = Path("assets")
P = ROOT / "profile"

C = {
    "cyan": "#35e9ff",
    "blue": "#2f7dff",
    "violet": "#8b7cff",
    "green": "#55e4ae",
    "amber": "#ffb44e",
    "red": "#ff667a",
    "white": "#effcff",
    "muted": "#6f93a6",
}

MARKER = "<!-- LEVIATHAN_JARVIS_V7 -->"

def pt(cx, cy, radius, angle):
    a = math.radians(angle - 90)
    return cx + radius * math.cos(a), cy + radius * math.sin(a)

def semantic_overlay(x, y, r, sectors, compact=False):
    outer = r + (24 if not compact else 18)
    inner = r + (7 if not compact else 5)
    scan = outer + (8 if not compact else 6)
    arc_len = 34 if len(sectors) <= 4 else 24
    inner_len = max(12, arc_len - 12)

    out = [MARKER, f'<g data-leviathan-ui="jarvis-v7" transform="translate({x} {y})">']
    out.append(f'<circle r="{outer}" fill="none" stroke="#05141f" stroke-width="7" stroke-opacity=".92"/>')
    out.append(f'<circle r="{inner}" fill="none" stroke="#0f3548" stroke-width="1.2" stroke-dasharray="5 8" stroke-opacity=".7"/>')

    for i, (angle, color) in enumerate(sectors):
        start = angle - arc_len / 2
        out.append(
            f'<circle r="{outer}" pathLength="360" fill="none" stroke="{color}" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-dasharray="{arc_len} {360-arc_len}" '
            f'transform="rotate({start})" filter="url(#glow)" opacity=".9"/>'
        )
        out.append(
            f'<circle r="{inner}" pathLength="360" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-dasharray="{inner_len} {360-inner_len}" '
            f'transform="rotate({start+6})" opacity=".68"/>'
        )

        px, py = pt(0, 0, outer, angle)
        pulse_delay = i * 0.55
        out.append(
            f'<g transform="translate({px:.2f} {py:.2f}) rotate({angle})">'
            f'<rect x="-5" y="-3" width="10" height="6" rx="1.5" fill="#031019" stroke="{color}" stroke-width="1.1"/>'
            f'<circle r="1.8" fill="{color}" filter="url(#glow)">'
            f'<animate attributeName="opacity" values=".35;1;.35" dur="5.5s" begin="{pulse_delay}s" repeatCount="indefinite"/>'
            f'</circle></g>'
        )

    for angle in range(0, 360, 30):
        x1, y1 = pt(0, 0, outer + 5, angle)
        x2, y2 = pt(0, 0, outer + (12 if angle % 90 == 0 else 9), angle)
        out.append(
            f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" stroke="#55bdd1" '
            f'stroke-width="{1.4 if angle % 90 == 0 else .8}" stroke-opacity="{.7 if angle % 90 == 0 else .36}"/>'
        )

    out.append(
        f'<g opacity=".9"><circle r="{scan}" pathLength="360" fill="none" stroke="#b9fbff" '
        f'stroke-width="2.1" stroke-linecap="round" stroke-dasharray="18 342" filter="url(#glow)">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="8.5s" repeatCount="indefinite"/>'
        f'<animate attributeName="stroke-opacity" values=".18;.9;.35;.18" dur="4.2s" repeatCount="indefinite"/>'
        f'</circle></g>'
    )

    out.append(
        f'<circle r="{outer-10}" pathLength="360" fill="none" stroke="#56d9ef" stroke-width=".9" '
        f'stroke-dasharray="3 9" stroke-opacity=".48">'
        f'<animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="31s" repeatCount="indefinite"/>'
        f'</circle>'
    )

    for bead_r, dur, color, start in [
        (scan, "17s", C["cyan"], 0),
        (scan + 3, "23s", C["white"], 160),
    ]:
        bx, by = pt(0, 0, bead_r, 0)
        out.append(
            f'<g transform="rotate({start})"><circle cx="{bx:.2f}" cy="{by:.2f}" r="2.4" fill="{color}" '
            f'filter="url(#glow)" opacity=".8"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="{start} 0 0" '
            f'to="{start+360} 0 0" dur="{dur}" repeatCount="indefinite"/></g>'
        )

    b = inner - 10
    out += [
        f'<path d="M{-b} -8H{-b-10} M{-b} 8H{-b-10}" stroke="#4cb8cf" stroke-opacity=".45"/>',
        f'<path d="M{b} -8H{b+10} M{b} 8H{b+10}" stroke="#4cb8cf" stroke-opacity=".45"/>',
        f'<path d="M-8 {-b}V{-b-10} M8 {-b}V{-b-10}" stroke="#4cb8cf" stroke-opacity=".45"/>',
        f'<path d="M-8 {b}V{b+10} M8 {b}V{b+10}" stroke="#4cb8cf" stroke-opacity=".45"/>',
        '</g>',
    ]
    return "".join(out)

def recolor_packets(text):
    pattern = re.compile(
        r'(<path d="[^"]+" fill="none" stroke="(?P<color>#[0-9a-fA-F]{6})"[^>]*/>\s*)'
        r'<circle r="4" fill="#d4fdff"'
    )
    return pattern.sub(lambda m: m.group(1) + f'<circle r="4" fill="{m.group("color")}"', text)

def remove_old_v7(text):
    start = text.find(MARKER)
    if start == -1:
        return text
    return text[:start] + "</svg>"

def decorate(path, cores):
    path = Path(path)
    if not path.exists():
        print(f"skip missing {path}")
        return
    text = path.read_text(encoding="utf-8")
    text = remove_old_v7(text)
    text = recolor_packets(text)
    overlay = "".join(semantic_overlay(*spec) for spec in cores)
    text = text.replace("</svg>", overlay + "</svg>")
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"Jarvis v7: {path}")

PAL4 = [
    (315, C["cyan"]),
    (45, C["violet"]),
    (135, C["green"]),
    (225, C["amber"]),
]
PAL6_DATA = [
    (315, C["cyan"]),
    (270, C["cyan"]),
    (225, C["amber"]),
    (45, C["violet"]),
    (90, C["green"]),
    (135, C["amber"]),
]
PAL6_PRODUCTS = [
    (315, C["cyan"]),
    (270, C["violet"]),
    (225, C["amber"]),
    (45, C["green"]),
    (90, C["violet"]),
    (135, C["cyan"]),
]
PAL6_IDENTITY = [
    (315, C["cyan"]),
    (285, C["cyan"]),
    (45, C["violet"]),
    (75, C["violet"]),
    (135, C["green"]),
    (225, C["green"]),
]
PAL6_MATRIX = [
    (300, C["cyan"]),
    (0, C["violet"]),
    (60, C["green"]),
    (240, C["amber"]),
    (180, C["violet"]),
    (120, C["cyan"]),
]
PAL8_DEV = [
    (315, C["cyan"]),
    (285, C["cyan"]),
    (255, C["green"]),
    (225, C["violet"]),
    (45, C["violet"]),
    (75, C["cyan"]),
    (105, C["violet"]),
    (135, C["green"]),
]

TARGETS = {
    ROOT / "hero-dark-v4.svg": [(930, 270, 104, PAL4, False)],
    ROOT / "hero-light-v4.svg": [(930, 270, 104, PAL4, False)],
    P / "command-core-v3.svg": [(930, 236, 108, [(300,C["cyan"]),(270,C["cyan"]),(235,C["violet"]),(205,C["amber"])], False)],
    P / "neural-core-v3.svg": [(600, 326, 128, PAL4, False)],
    P / "systems-matrix-v1.svg": [(600, 483, 90, PAL6_MATRIX, False)],
    P / "data-platform-v2.svg": [(600, 350, 112, PAL6_DATA, False)],
    P / "core-products-v2.svg": [(600, 350, 112, PAL6_PRODUCTS, False)],
    P / "external-services-v2.svg": [(600, 350, 108, PAL6_IDENTITY, False)],
    P / "ecosystem-overview-v2.svg": [(600, 310, 102, PAL4, False)],
    P / "platform-areas-v2.svg": [(600, 310, 102, PAL4, False)],
    P / "experience-commerce-v2.svg": [
        (600, 292, 100, [(310,C["cyan"]),(335,C["cyan"]),(25,C["cyan"]),(50,C["cyan"]),(180,C["violet"])], False),
        (600, 566, 72, [(240,C["amber"]),(270,C["amber"]),(300,C["amber"]),(60,C["green"]),(90,C["green"]),(180,C["violet"])], True),
    ],
    P / "developer-network-v2.svg": [(600, 390, 122, PAL8_DEV, False)],
    P / "project-signal-v1.svg": [(600, 320, 116, PAL4, False)],
}

for path, cores in TARGETS.items():
    decorate(path, cores)

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

def base(w,h,title,subtitle):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        DEFS,
        f'<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>',
        f'<rect width="{w}" height="{h}" rx="24" fill="url(#grid)"/>',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="none" stroke="#173d52"/>',
        f'<text x="42" y="43" fill="#58eaff" font-family="ui-monospace,Consolas,monospace" font-size="14" letter-spacing="2.8">{title}</text>',
        f'<text x="42" y="67" fill="#7e9caf" font-family="Segoe UI,Arial,sans-serif" font-size="11">{subtitle}</text>',
        f'<path d="M42 86H{w-42}" stroke="#14384a"/>',
        '<path d="M42 84H162" stroke="#35e9ff" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>',
    ]

def finish(lines,w,h,footer):
    lines += [
        f'<text x="42" y="{h-22}" fill="#557b8f" font-family="ui-monospace,Consolas,monospace" font-size="8.5">{footer}</text>',
        f'<path d="M6 6H{w-6}V{h-6}H6Z" fill="none" stroke="url(#edge)" stroke-width="2" stroke-dasharray="170 2500" filter="url(#glow)" opacity=".7">'
        '<animate attributeName="stroke-dashoffset" from="0" to="-2670" dur="22s" repeatCount="indefinite"/></path>',
        '</svg>',
    ]
    return "\n".join(lines)

def mini_card(x,y,w,h,title,desc,color):
    return (
        f'<path d="M{x} {y}H{x+w-14}L{x+w} {y+14}V{y+h}H{x}Z" fill="#061722" stroke="{color}" stroke-opacity=".48"/>'
        f'<text x="{x+18}" y="{y+28}" fill="#effcff" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">{title}</text>'
        f'<text x="{x+18}" y="{y+50}" fill="#7ea4b6" font-family="ui-monospace,Consolas,monospace" font-size="8">{desc}</text>'
    )

def simple_core(x,y,r,label,sub,sectors):
    inner=max(30,int(r*.38))
    parts=[
        f'<g transform="translate({x} {y})">',
        f'<circle r="{r+30}" fill="url(#energy)"/>',
        f'<circle r="{r+16}" fill="#020b14" stroke="#123f52"/>',
        f'<circle r="{r+9}" fill="none" stroke="#2e7f98" stroke-width="1.2" stroke-dasharray="10 8">'
        f'<animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="23s" repeatCount="indefinite"/></circle>',
    ]
    for i, angle in enumerate(range(0,360,60)):
        col = sectors[i % len(sectors)][1]
        parts.append(
            f'<g transform="rotate({angle})"><path d="M-10 -{r-14}H10L7 -{inner+11}H-7Z" fill="#04131d" stroke="{col}" stroke-opacity=".5"/>'
            f'<path d="M0 -{r-21}V-{inner+17}" stroke="{col}" stroke-width="5" stroke-linecap="round" opacity=".35" filter="url(#glow)">'
            f'<animate attributeName="opacity" values=".2;.2;.95;.3;.2" keyTimes="0;.35;.5;.67;1" dur="6s" begin="{i*.45}s" repeatCount="indefinite"/></path></g>'
        )
    parts += [
        f'<polygon points="0,-{inner} {int(inner*.82)},-{int(inner*.48)} {int(inner*.82)},{int(inner*.48)} 0,{inner} -{int(inner*.82)},{int(inner*.48)} -{int(inner*.82)},-{int(inner*.48)}" fill="#04131d" stroke="#35e9ff" stroke-width="1.4"/>',
        '<g filter="url(#glow)" stroke="#35e9ff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M0 -{int(inner*.64)}V{int(inner*.56)}"/>'
        f'<path d="M-{int(inner*.56)} -{int(inner*.2)}L-{int(inner*.22)} 0L-{int(inner*.43)} {int(inner*.48)}"/>'
        f'<path d="M{int(inner*.56)} -{int(inner*.2)}L{int(inner*.22)} 0L{int(inner*.43)} {int(inner*.48)}"/></g>',
        f'<text x="0" y="{r+47}" text-anchor="middle" fill="#effcff" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">{label}</text>',
        f'<text x="0" y="{r+63}" text-anchor="middle" fill="#6b9aad" font-family="ui-monospace,Consolas,monospace" font-size="7.3" letter-spacing="1.3">{sub}</text>',
        '</g>',
        semantic_overlay(x,y,r,sectors),
    ]
    return "".join(parts)

w,h=1200,700
L=base(w,h,"LEVIATHAN DEVELOPMENT PIPELINE // CONTINUOUS WORKSTREAMS","Eight release phases use a color-coded JARVIS-style pipeline core and one directional execution spine.")
L.append(simple_core(210,360,108,"PIPELINE","RESEARCH • RELEASE",[(315,C["cyan"]),(45,C["blue"]),(105,C["violet"]),(165,C["green"]),(225,C["amber"]),(270,C["cyan"])]))
phases=[
    ("01","RESEARCH","ecosystem • compatibility • user needs",C["cyan"]),
    ("02","ARCHITECTURE","boundaries • APIs • data • security controls",C["blue"]),
    ("03","BUILD","launcher • client • web • app • server • platform",C["cyan"]),
    ("04","INTEGRATION","auth • API • server links • devices • cross-product",C["violet"]),
    ("05","SECURITY & INTEGRITY","anticheat • abuse controls • privacy • diagnostics",C["amber"]),
    ("06","TEST & VALIDATE","compatibility • recovery • regression • devices",C["green"]),
    ("07","OPERATE & OBSERVE","telemetry • analytics • status • support • logs",C["violet"]),
    ("08","RELEASE & IMPROVE","signing • distribution • docs • feedback",C["green"]),
]
L.append('<path d="M365 122V590" stroke="#1f7d97" stroke-width="2"/>')
L.append('<circle r="4" fill="#35e9ff" filter="url(#glow)" opacity="0"><animateMotion path="M365 122V590" dur="10s" repeatCount="indefinite" calcMode="linear"/><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.04;.9;.96;1" dur="10s" repeatCount="indefinite"/></circle>')
y=104
for num,title,desc,col in phases:
    cy=y+25
    L += [
        f'<circle cx="365" cy="{cy}" r="6" fill="#04131d" stroke="{col}" stroke-width="2"/>',
        f'<path d="M371 {cy}H402" stroke="{col}" stroke-opacity=".75"/>',
        f'<path d="M402 {y}H1138L1150 {y+12}V{y+50}H402Z" fill="#061722" stroke="#1a4c61"/>',
        f'<text x="423" y="{y+22}" fill="{col}" font-family="ui-monospace,Consolas,monospace" font-size="8.3">{num}</text>',
        f'<text x="456" y="{y+31}" fill="#effcff" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">{title}</text>',
        f'<text x="690" y="{y+31}" fill="#7ea4b6" font-family="ui-monospace,Consolas,monospace" font-size="8.3">{desc}</text>',
    ]
    y += 60
(P/"roadmap-v2.svg").write_text(finish(L,w,h,"PUBLIC-SAFE PROJECT PIPELINE // PRODUCT-SPECIFIC STATUS REMAINS IN EACH REPOSITORY"),encoding="utf-8",newline="\n")

w,h=1200,500
L=base(w,h,"LEVIATHAN // DEVELOPMENT STACK","Technology families are grouped by function around one compact build core instead of an older standalone dial.")
L.append(simple_core(170,268,72,"STACK","BUILD CORE",[(315,C["cyan"]),(45,C["blue"]),(105,C["violet"]),(165,C["green"]),(225,C["amber"]),(270,C["cyan"])]))
stack=[
    (300,118,"JAVA 21","RUNTIME",C["cyan"]),
    (515,118,"KOTLIN DSL","BUILD LOGIC",C["violet"]),
    (730,118,"HTML + CSS","PRESENTATION",C["blue"]),
    (945,118,"JSON / YAML","CONFIG",C["green"]),
    (300,282,"JAVASCRIPT","WEB / UI",C["blue"]),
    (515,282,"GRADLE","BUILD",C["amber"]),
    (730,282,"POSTGRESQL","DATA",C["green"]),
    (945,282,"CI / CD","PIPELINES",C["violet"]),
]
L.append('<path d="M242 268H272V158H300 M272 268V322H300" fill="none" stroke="#35e9ff" stroke-opacity=".55"/>')
for x,y,title,desc,col in stack:
    L.append(mini_card(x,y,180,84,title,desc,col))
L.append('<path d="M280 240H1130" stroke="#17495e" stroke-dasharray="8 10"/>')
L.append('<circle r="3.5" fill="#35e9ff" filter="url(#glow)" opacity="0"><animateMotion path="M280 240H1130" dur="9s" repeatCount="indefinite" calcMode="linear"/><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.88;.95;1" dur="9s" repeatCount="indefinite"/></circle>')
(P/"tech-stack-v2.svg").write_text(finish(L,w,h,"HIGH-LEVEL STACK ONLY // IMPLEMENTATION DETAILS AND CREDENTIALS EXCLUDED"),encoding="utf-8",newline="\n")

print("Applied Leviathan JARVIS semantic color system v7 across all profile reactor surfaces")
