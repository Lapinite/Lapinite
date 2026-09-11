from __future__ import annotations
import html, json, os, urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER="Lapinite"
TOKEN=os.environ.get("GITHUB_TOKEN","")
OUT=Path("assets/profile")

def esc(v): return html.escape(str(v), quote=True)
def api(path):
    req=urllib.request.Request(f"https://api.github.com{path}",headers={"Accept":"application/vnd.github+json","User-Agent":"Lapinite-profile-live-panels","X-GitHub-Api-Version":"2022-11-28",**({"Authorization":f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)

def defs():
    return '''<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#020913"/><stop offset=".55" stop-color="#061725"/><stop offset="1" stop-color="#020b13"/></linearGradient><linearGradient id="cyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b7dff"/><stop offset=".5" stop-color="#29e7ff"/><stop offset="1" stop-color="#00a7ff"/></linearGradient><filter id="g" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#12364b" stroke-width="1" opacity=".2"/></pattern></defs>'''

def event_text(e):
    typ=e.get("type","").replace("Event","") or "Activity"
    repo=e.get("repo",{}).get("name","").split("/")[-1]
    p=e.get("payload",{})
    if typ=="Push":
        ref=(p.get("ref") or "").replace("refs/heads/","")
        return f"PUSH // {repo}"+(f" // {ref}" if ref else "")
    if typ=="PullRequest":
        pr=p.get("pull_request",{})
        action="MERGED" if pr.get("merged_at") else str(p.get("action","UPDATED")).upper()
        return f"PR {action} // {repo} #{pr.get('number','')}"
    if typ=="Create": return f"CREATE // {repo} // {p.get('ref_type','item')}"
    if typ=="Issues": return f"ISSUE {str(p.get('action','updated')).upper()} // {repo}"
    return f"{typ.upper()} // {repo}"

def write_activity(events):
    rows=events[:8]
    h=118+len(rows)*48
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}">',defs(),f'<rect width="1200" height="{h}" rx="22" fill="url(#bg)"/><rect width="1200" height="{h}" rx="22" fill="url(#grid)"/><rect x="1" y="1" width="1198" height="{h-2}" rx="21" fill="none" stroke="#173b51"/>','<text x="42" y="45" fill="#58eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">LIVE PUBLIC ACTIVITY FEED</text>','<text x="42" y="70" fill="#7899ac" font-family="Segoe UI,Arial,sans-serif" font-size="11">Latest public GitHub events</text>']
    y=98
    for i,e in enumerate(rows):
        stamp=datetime.fromisoformat(e["created_at"].replace("Z","+00:00")).astimezone(timezone.utc).strftime("%H:%M UTC")
        s += [f'<rect x="42" y="{y}" width="1116" height="38" rx="9" fill="#061621" stroke="#14394d"/>',f'<circle cx="61" cy="{y+19}" r="4" fill="#42e9ff" filter="url(#g)"><animate attributeName="opacity" values=".35;1;.35" dur="{1.5+i*.08}s" repeatCount="indefinite"/></circle>',f'<text x="79" y="{y+24}" fill="#dcecf4" font-family="ui-monospace,Consolas,monospace" font-size="11">{esc(event_text(e)[:94])}</text>',f'<text x="1138" y="{y+24}" text-anchor="end" fill="#6e92a5" font-family="ui-monospace,Consolas,monospace" font-size="10">{stamp}</text>']
        y+=48
    s += [f'<rect x="42" y="{h-18}" width="180" height="2" rx="1" fill="url(#cyan)"><animate attributeName="x" values="42;978;42" dur="8s" repeatCount="indefinite"/></rect>','</svg>']
    (OUT/"activity-feed.svg").write_text("\n".join(s),encoding="utf-8")

def write_repos(repos):
    repos=sorted(repos,key=lambda r:r.get("pushed_at") or "",reverse=True)[:8]
    h=144+len(repos)*50
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}">',defs(),f'<rect width="1200" height="{h}" rx="22" fill="url(#bg)"/><rect width="1200" height="{h}" rx="22" fill="url(#grid)"/><rect x="1" y="1" width="1198" height="{h-2}" rx="21" fill="none" stroke="#173b51"/>','<text x="42" y="45" fill="#58eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">PUBLIC REPOSITORY HEALTH</text>','<text x="42" y="70" fill="#7899ac" font-family="Segoe UI,Arial,sans-serif" font-size="11">Freshness, size and issue state for the most recently updated public repositories</text>','<text x="56" y="106" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">REPOSITORY</text><text x="655" y="106" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">LAST PUSH</text><text x="830" y="106" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">SIZE</text><text x="970" y="106" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">ISSUES</text><text x="1090" y="106" fill="#597f94" font-family="ui-monospace,Consolas,monospace" font-size="9">STATE</text>']
    y=122
    today=datetime.now(timezone.utc).date()
    for i,r in enumerate(repos):
        pushed=(r.get("pushed_at") or "")[:10]
        age=(today-datetime.fromisoformat((r.get("pushed_at") or datetime.now(timezone.utc).isoformat()).replace("Z","+00:00")).date()).days
        state="FRESH" if age<=7 else "QUIET"
        state_color="#4cefa8" if age<=7 else "#f0b15e"
        size=int(r.get("size",0)); size_txt=f"{size/1024:.1f} MB" if size>=1024 else f"{size} KB"
        s += [f'<rect x="42" y="{y}" width="1116" height="40" rx="9" fill="#061621" stroke="#14394d"/>',f'<text x="56" y="{y+25}" fill="#dcecf4" font-family="Segoe UI,Arial,sans-serif" font-size="12" font-weight="700">{esc(r.get("name",""))}</text>',f'<text x="655" y="{y+25}" fill="#8ba8b7" font-family="ui-monospace,Consolas,monospace" font-size="10">{pushed}</text>',f'<text x="830" y="{y+25}" fill="#8ba8b7" font-family="ui-monospace,Consolas,monospace" font-size="10">{size_txt}</text>',f'<text x="970" y="{y+25}" fill="#8ba8b7" font-family="ui-monospace,Consolas,monospace" font-size="10">{r.get("open_issues_count",0)}</text>',f'<circle cx="1098" cy="{y+20}" r="4" fill="{state_color}" filter="url(#g)"/><text x="1112" y="{y+24}" fill="{state_color}" font-family="ui-monospace,Consolas,monospace" font-size="9">{state}</text>']
        y+=50
    s+=['</svg>']
    (OUT/"repository-health.svg").write_text("\n".join(s),encoding="utf-8")

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    events=api(f"/users/{USER}/events/public?per_page=100")
    repos=[r for r in api(f"/users/{USER}/repos?per_page=100&sort=pushed&direction=desc&type=owner") if not r.get("private")]
    write_activity(events); write_repos(repos)

if __name__=="__main__": main()
