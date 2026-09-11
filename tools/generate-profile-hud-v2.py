from __future__ import annotations

import html
import json
import os
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

USER = "Lapinite"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ASSETS = Path("assets/profile")


def api(path: str):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Lapinite-holographic-profile",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def defs() -> str:
    return '''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#020812"/><stop offset=".55" stop-color="#061725"/><stop offset="1" stop-color="#020b13"/></linearGradient>
<linearGradient id="cyan" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#087dff"/><stop offset=".5" stop-color="#2be8ff"/><stop offset="1" stop-color="#00a8ff"/></linearGradient>
<linearGradient id="amber" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#ff9c31"/><stop offset=".5" stop-color="#ffd37c"/><stop offset="1" stop-color="#ff8c1f"/></linearGradient>
<filter id="g" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#12344b" opacity=".18"/></pattern>
</defs>'''


def frame(w: int, h: int, title: str, subtitle: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', defs(),
        f'<rect width="{w}" height="{h}" rx="24" fill="url(#bg)"/>',
        f'<rect width="{w}" height="{h}" rx="24" fill="url(#grid)"/>',
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="none" stroke="#173b51"/>',
        f'<text x="42" y="45" fill="#58eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">{esc(title)}</text>',
        f'<text x="42" y="70" fill="#7899ac" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(subtitle)}</text>',
    ]


def border(w: int, h: int) -> list[str]:
    perimeter = 2 * ((w - 8) + (h - 8))
    dash = round(perimeter * .21)
    gap = perimeter - dash
    return [
        f'<rect x="4" y="4" width="{w-8}" height="{h-8}" rx="21" fill="none" stroke="url(#cyan)" stroke-width="3" stroke-dasharray="{dash} {gap}" filter="url(#g)" opacity=".9"><animate attributeName="stroke-dashoffset" values="0;-{perimeter}" dur="10s" repeatCount="indefinite"/></rect>',
        '</svg>'
    ]


def commits_last_year(repos: list[dict]) -> Counter[date]:
    counts: Counter[date] = Counter()
    since = (datetime.now(timezone.utc) - timedelta(days=365)).isoformat()
    for repo in repos:
        full = repo["full_name"]
        for page in range(1, 11):
            query = urllib.parse.urlencode({"author": USER, "since": since, "per_page": 100, "page": page})
            try:
                data = api(f"/repos/{full}/commits?{query}")
            except Exception:
                break
            if not isinstance(data, list) or not data:
                break
            for commit in data:
                stamp = commit.get("commit", {}).get("author", {}).get("date") or commit.get("commit", {}).get("committer", {}).get("date")
                if stamp:
                    counts[datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()] += 1
            if len(data) < 100:
                break
    return counts


def write_contributions(counts: Counter[date]) -> None:
    w, h = 1200, 430
    today = datetime.now(timezone.utc).date()
    first = today - timedelta(days=364)
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    total = sum(counts.values())
    active = sum(1 for i in range(365) if counts.get(first + timedelta(days=i), 0))
    peak_day, peak = max(counts.items(), key=lambda x: x[1], default=(today, 0))
    maxv = max(counts.values(), default=1) or 1
    lines = frame(w, h, "PUBLIC COMMIT SIGNAL // 365 DAY MATRIX", "Public repository activity projected as a live development field.")
    cards = [(42, "TOTAL COMMITS", total), (278, "ACTIVE DAYS", active), (514, "PEAK OUTPUT", f"{peak} commits"), (750, "PEAK DATE", peak_day.strftime("%b %d"))]
    for x, label, value in cards:
        lines += [f'<path d="M{x} 96 H{x+202} L{x+214} 108 V162 H{x} Z" fill="#061723" stroke="#17465f"/>', f'<text x="{x+18}" y="119" fill="#64879b" font-family="ui-monospace,Consolas,monospace" font-size="9">{label}</text>', f'<text x="{x+18}" y="150" fill="#edfaff" font-family="Segoe UI,Arial,sans-serif" font-size="23" font-weight="750">{esc(value)}</text>']
    lines += ['<path d="M42 180 H1158" stroke="#174052"/><text x="42" y="202" fill="#6f93a6" font-family="ui-monospace,Consolas,monospace" font-size="9">DEVELOPMENT FIELD / LOW → HIGH</text>']
    x0, y0, cell, gap = 105, 220, 12, 3
    for week in range(53):
        for dow in range(7):
            day = start + timedelta(days=week*7+dow)
            value = counts.get(day, 0)
            ratio = value/maxv if maxv else 0
            fill = '#08151e' if value == 0 else '#08384d' if ratio < .25 else '#08647e' if ratio < .5 else '#00a0b8' if ratio < .75 else '#4beeff'
            x, y = x0+week*(cell+gap), y0+dow*(cell+gap)
            lines.append(f'<path d="M{x} {y+6} L{x+6} {y} L{x+12} {y+6} L{x+6} {y+12} Z" fill="{fill}" stroke="#0c2d3c" stroke-width=".5"><title>{day.isoformat()}: {value} public commits</title></path>')
    lines += ['<path id="scan" d="M96 210 H920" stroke="none"/><rect width="42" height="3" rx="1.5" fill="url(#cyan)" filter="url(#g)"><animateMotion dur="7s" repeatCount="indefinite"><mpath href="#scan"/></animateMotion></rect>', '<path d="M930 228 H1135 M930 252 H1090 M930 276 H1110 M930 300 H1060" stroke="#16495f" stroke-width="6"/>', '<path d="M930 228 H1085 M930 252 H1020 M930 276 H1050 M930 300 H990" stroke="url(#cyan)" stroke-width="6"/>', '<text x="930" y="332" fill="#66899d" font-family="ui-monospace,Consolas,monospace" font-size="9">MONTHLY OUTPUT CHANNEL</text>']
    lines += border(w, h)
    (ASSETS / "contributions-v2.svg").write_text("\n".join(lines), encoding="utf-8")


def event_label(event: dict) -> str:
    kind = event.get("type", "Activity").replace("Event", "").upper()
    repo = event.get("repo", {}).get("name", "GitHub").split("/")[-1]
    payload = event.get("payload", {})
    if kind == "PULLREQUEST":
        pr = payload.get("pull_request", {})
        action = "MERGED" if pr.get("merged_at") else str(payload.get("action", "UPDATED")).upper()
        return f"PR {action} // {repo} #{pr.get('number','')}"
    if kind == "PUSH":
        return f"PUSH // {repo}"
    if kind == "CREATE":
        return f"CREATE // {repo}"
    return f"{kind} // {repo}"


def write_activity(events: list[dict]) -> None:
    w, h = 1200, 510
    lines = frame(w, h, "LIVE PUBLIC ACTIVITY // EVENT STREAM", "Recent GitHub events rendered as an operational signal feed.")
    lines += ['<path d="M73 103 V450" stroke="#16485e" stroke-width="2"/><path d="M73 103 V450" stroke="#29e7ff" stroke-width="2" stroke-dasharray="20 18"><animate attributeName="stroke-dashoffset" values="0;-76" dur="3s" repeatCount="indefinite"/></path>']
    y = 102
    for idx, event in enumerate(events[:8]):
        stamp = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%H:%M UTC")
        label = event_label(event)
        accent = '#ffb45e' if 'MERGED' in label else '#58eaff'
        lines += [f'<path d="M73 {y+20} H104 L120 {y+4} H1138" fill="none" stroke="#14394d"/>', f'<rect x="66" y="{y+13}" width="14" height="14" rx="2" fill="{accent}" filter="url(#g)"><animate attributeName="opacity" values=".35;1;.35" dur="{1.4+idx*.09:.2f}s" repeatCount="indefinite"/></rect>', f'<path d="M120 {y+4} H1138 V{y+42} H132 L120 {y+30} Z" fill="#061621" stroke="#14394d"/>', f'<text x="145" y="{y+27}" fill="#dcecf4" font-family="ui-monospace,Consolas,monospace" font-size="11">{esc(label)}</text>', f'<text x="1118" y="{y+27}" text-anchor="end" fill="#6e92a5" font-family="ui-monospace,Consolas,monospace" font-size="9">{stamp}</text>']
        y += 47
    lines += ['<rect x="120" y="480" width="180" height="2" rx="1" fill="url(#cyan)"><animate attributeName="x" values="120;930;120" dur="8s" repeatCount="indefinite"/></rect>']
    lines += border(w, h)
    (ASSETS / "activity-feed-v2.svg").write_text("\n".join(lines), encoding="utf-8")


def write_health(repos: list[dict]) -> None:
    w, h = 1200, 560
    rows = sorted(repos, key=lambda r: r.get("pushed_at") or "", reverse=True)[:8]
    lines = frame(w, h, "PUBLIC REPOSITORY HEALTH // SERVICE MATRIX", "Freshness, size and issue state across active public surfaces.")
    lines += ['<text x="58" y="105" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">REPOSITORY</text><text x="660" y="105" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">LAST PUSH</text><text x="825" y="105" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">SIZE</text><text x="955" y="105" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">ISSUES</text><text x="1080" y="105" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">STATE</text>']
    y = 120
    for idx, repo in enumerate(rows):
        name = repo.get('name','repo')
        pushed = (repo.get('pushed_at') or 'unknown')[:10]
        size = int(repo.get('size',0))
        issues = int(repo.get('open_issues_count',0))
        state = 'FRESH' if pushed != 'unknown' else 'UNKNOWN'
        lines += [f'<path d="M42 {y} H1142 L1158 {y+16} V{y+44} H58 L42 {y+28} Z" fill="#061621" stroke="#14394d"/>', f'<rect x="55" y="{y+17}" width="8" height="8" rx="2" fill="#4cefa8"><animate attributeName="opacity" values=".35;1;.35" dur="{1.5+idx*.08:.2f}s" repeatCount="indefinite"/></rect>', f'<text x="78" y="{y+28}" fill="#dcecf4" font-family="Segoe UI,Arial,sans-serif" font-size="12" font-weight="700">{esc(name)}</text>', f'<text x="660" y="{y+28}" fill="#8ba8b7" font-family="ui-monospace,Consolas,monospace" font-size="10">{pushed}</text>', f'<text x="825" y="{y+28}" fill="#8ba8b7" font-family="ui-monospace,Consolas,monospace" font-size="10">{size} KB</text>', f'<text x="955" y="{y+28}" fill="#8ba8b7" font-family="ui-monospace,Consolas,monospace" font-size="10">{issues}</text>', f'<text x="1080" y="{y+28}" fill="#4cefa8" font-family="ui-monospace,Consolas,monospace" font-size="9">{state}</text>']
        y += 51
    lines += border(w, h)
    (ASSETS / "repository-health-v2.svg").write_text("\n".join(lines), encoding="utf-8")


def write_analytics(repos: list[dict], events: list[dict]) -> None:
    w, h = 1200, 700
    public_size = sum(int(r.get('size',0)) for r in repos)
    open_issues = sum(int(r.get('open_issues_count',0)) for r in repos)
    event_types = Counter(e.get('type','Other').replace('Event','') for e in events)
    largest = sorted(((r.get('name','repo'), int(r.get('size',0))) for r in repos), key=lambda x:x[1], reverse=True)[:6]
    lines = frame(w, h, "PUBLIC DEVELOPMENT TELEMETRY // HOLOGRAPHIC OVERVIEW", "Live public GitHub signals rendered as one Leviathan operations surface.")
    cards = [(42,'PUBLIC REPOS',len(repos)),(326,'ACTIVE SIGNALS',len(events)),(610,'PUBLIC SIZE',f'{public_size} KB'),(894,'OPEN ISSUES',open_issues)]
    for x,label,value in cards:
        lines += [f'<path d="M{x} 98 H{x+246} L{x+264} 116 V194 H{x} Z" fill="#061723" stroke="#17465f"/>', f'<text x="{x+20}" y="124" fill="#64879b" font-family="ui-monospace,Consolas,monospace" font-size="10">{label}</text>', f'<text x="{x+20}" y="162" fill="#f0fbff" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="800">{esc(value)}</text>']
    lines += ['<path d="M42 225 H580 L598 243 V430 H42 Z" fill="#05131d" stroke="#173b50"/><text x="62" y="255" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="750">Activity Routing</text>', '<path d="M620 225 H1140 L1158 243 V430 H620 Z" fill="#05131d" stroke="#173b50"/><text x="640" y="255" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="750">Repository Mass</text>']
    y=290
    maxe=max(event_types.values(),default=1) or 1
    for name,value in event_types.most_common(5):
        width=round(330*value/maxe)
        lines += [f'<text x="62" y="{y+12}" fill="#b8d0dc" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(name)}</text>', f'<path d="M205 {y+6} H520" stroke="#102532" stroke-width="10"/><path d="M205 {y+6} H{205+width}" stroke="url(#cyan)" stroke-width="10"/>', f'<text x="548" y="{y+12}" text-anchor="end" fill="#eaf9ff" font-family="ui-monospace,Consolas,monospace" font-size="9">{value}</text>']
        y+=29
    y=290
    maxs=max((v for _,v in largest),default=1) or 1
    for name,value in largest:
        width=round(320*value/maxs)
        lines += [f'<text x="640" y="{y+12}" fill="#b8d0dc" font-family="Segoe UI,Arial,sans-serif" font-size="10">{esc(name[:24])}</text>', f'<path d="M810 {y+6} H1110" stroke="#102532" stroke-width="9"/><path d="M810 {y+6} H{810+width}" stroke="#2d86ff" stroke-width="9"/>']
        y+=25
    lines += ['<path d="M42 468 H1158" stroke="#17384d"/><text x="42" y="496" fill="#6f93a6" font-family="ui-monospace,Consolas,monospace" font-size="9">14 DAY SIGNAL TRACE</text>']
    today=datetime.now(timezone.utc).date(); ec=Counter(datetime.fromisoformat(e['created_at'].replace('Z','+00:00')).date() for e in events); days=[today-timedelta(days=i) for i in range(13,-1,-1)]; vals=[ec[d] for d in days]; maxv=max(vals,default=1) or 1
    pts=[]
    for i,(d,v) in enumerate(zip(days,vals)):
        x=65+round(1060*i/13); y=625-round(100*v/maxv); pts.append(f'{x},{y}'); lines.append(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" rx="1" fill="#51eaff"><title>{d.isoformat()}: {v} events</title></rect>')
    lines += [f'<polyline points="{" ".join(pts)}" fill="none" stroke="#4fcfff" stroke-width="2.5"/>', '<rect x="42" y="675" width="120" height="2" rx="1" fill="url(#cyan)"><animate attributeName="x" values="42;1038;42" dur="9s" repeatCount="indefinite"/></rect>']
    lines += border(w,h)
    (ASSETS / "analytics-overview-v2.svg").write_text("\n".join(lines), encoding="utf-8")


def write_pacman(counts: Counter[date]) -> None:
    w,h=1200,330
    lines=frame(w,h,"CONTRIBUTION ACTIVITY // ARCADE SIGNAL","A playful contribution route kept inside the Leviathan interface language.")
    lines += ['<path id="route" d="M70 180 H260 V120 H470 V225 H680 V130 H890 V205 H1120" fill="none" stroke="#17465e" stroke-width="5" stroke-linejoin="round"/>']
    for x,y in [(100,180),(150,180),(200,180),(260,150),(320,120),(380,120),(440,120),(470,170),(530,225),(590,225),(650,225),(680,175),(740,130),(800,130),(860,130),(890,170),(950,205),(1010,205),(1070,205)]:
        lines.append(f'<rect x="{x-3}" y="{y-3}" width="6" height="6" rx="1" fill="#49efff" opacity=".8"/>')
    lines += ['<path d="M0 -14 A14 14 0 1 1 0 14 L14 0 Z" fill="#ffd65c" transform="translate(70 180)" filter="url(#g)"><animateMotion dur="10s" repeatCount="indefinite"><mpath href="#route"/></animateMotion></path>', '<path d="M-12 -12 H12 V10 L7 5 L2 10 L-3 5 L-8 10 L-12 6 Z" fill="#6f75ff"><animateMotion dur="12s" begin="2s" repeatCount="indefinite"><mpath href="#route"/></animateMotion></path>', f'<text x="70" y="285" fill="#6f93a6" font-family="ui-monospace,Consolas,monospace" font-size="10">PUBLIC COMMITS DETECTED // {sum(counts.values())}</text>']
    lines += border(w,h)
    (ASSETS / "pacman-v2.svg").write_text("\n".join(lines),encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    events=api(f"/users/{USER}/events/public?per_page=100")
    repos=api(f"/users/{USER}/repos?per_page=100&sort=pushed&direction=desc&type=owner")
    repos=[r for r in repos if not r.get('private')]
    counts=commits_last_year(repos)
    write_contributions(counts)
    write_activity(events)
    write_health(repos)
    write_analytics(repos,events)
    write_pacman(counts)


if __name__ == "__main__":
    main()
