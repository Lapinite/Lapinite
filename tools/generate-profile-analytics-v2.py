from __future__ import annotations

import html
import json
import os
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

USER = "Lapinite"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path("assets/profile/analytics-overview.svg")


def api(path: str):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Lapinite-profile-analytics-v2",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> None:
    events = api(f"/users/{USER}/events/public?per_page=100")
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&sort=pushed&direction=desc&type=owner") if not r.get("private")]

    languages: Counter[str] = Counter()
    for repo in repos:
        try:
            languages.update(api(f'/repos/{repo["full_name"]}/languages'))
        except Exception:
            pass

    activity = Counter(e.get("type", "Other").replace("Event", "") for e in events)
    recent_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    active_7d = {
        e.get("repo", {}).get("name", "").split("/")[-1]
        for e in events
        if e.get("created_at") and datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")) >= recent_cutoff
    }
    active_7d.discard("")

    total_size = sum(int(r.get("size", 0)) for r in repos)
    open_issues = sum(int(r.get("open_issues_count", 0)) for r in repos)
    top_repos = sorted(repos, key=lambda r: int(r.get("size", 0)), reverse=True)[:6]

    today = datetime.now(timezone.utc).date()
    event_days = Counter(datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).date() for e in events if e.get("created_at"))
    days = [today - timedelta(days=i) for i in range(13, -1, -1)]
    vals = [event_days[d] for d in days]
    vmax = max(vals, default=1) or 1

    lang_items = languages.most_common(5)
    lang_total = sum(v for _, v in lang_items) or 1
    act_items = activity.most_common(5)
    act_max = max((v for _, v in act_items), default=1) or 1
    repo_max = max((int(r.get("size", 0)) for r in top_repos), default=1) or 1

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="0 0 1200 700">',
        '''<defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#020913"/><stop offset=".55" stop-color="#061725"/><stop offset="1" stop-color="#020b13"/></linearGradient>
        <linearGradient id="cyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b7dff"/><stop offset=".5" stop-color="#29e7ff"/><stop offset="1" stop-color="#00a7ff"/></linearGradient>
        <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#12364b" stroke-width="1" opacity=".22"/></pattern>
        </defs>''',
        '<rect width="1200" height="700" rx="24" fill="url(#bg)"/>',
        '<rect width="1200" height="700" rx="24" fill="url(#grid)"/>',
        '<rect x="1" y="1" width="1198" height="698" rx="23" fill="none" stroke="#173b51"/>',
        '<text x="42" y="46" fill="#58eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">LEVIATHAN // PUBLIC DEVELOPMENT TELEMETRY</text>',
        '<text x="42" y="72" fill="#7d9fb2" font-family="Segoe UI,Arial,sans-serif" font-size="12">Live public GitHub signals presented as one unified dashboard.</text>',
    ]

    cards = [
        (42, "PUBLIC REPOS", len(repos), "visible repositories"),
        (326, "ACTIVE 7D", len(active_7d), "repositories with public activity"),
        (610, "PUBLIC SIZE", f"{total_size} KB", "GitHub-reported repository size"),
        (894, "OPEN ISSUES", open_issues, "across public repositories"),
    ]
    for x, label, value, note in cards:
        svg += [
            f'<rect x="{x}" y="98" width="264" height="96" rx="14" fill="#061723" stroke="#17465f"/>',
            f'<text x="{x+20}" y="123" fill="#64879b" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1.4">{label}</text>',
            f'<text x="{x+20}" y="158" fill="#f0fbff" font-family="Segoe UI,Arial,sans-serif" font-size="28" font-weight="800">{esc(value)}</text>',
            f'<text x="{x+20}" y="180" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="9.5">{esc(note)}</text>',
        ]

    # Languages
    svg += ['<rect x="42" y="220" width="548" height="220" rx="16" fill="#05131d" stroke="#173b50"/>',
            '<text x="62" y="250" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="750">Public Repository Language Mix</text>',
            '<text x="62" y="269" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="10">Detected in public repositories only</text>']
    y = 296
    for name, value in lang_items or [("No public language data", 0)]:
        pct = value * 100 / lang_total if lang_total else 0
        w = max(2, round(300 * pct / 100))
        svg += [f'<text x="62" y="{y+12}" fill="#b8d0dc" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(name)}</text>',
                f'<rect x="205" y="{y}" width="300" height="14" rx="5" fill="#102532"/>',
                f'<rect x="205" y="{y}" width="{w}" height="14" rx="5" fill="url(#cyan)"/>',
                f'<text x="520" y="{y+12}" text-anchor="end" fill="#eaf9ff" font-family="ui-monospace,Consolas,monospace" font-size="10">{pct:.1f}%</text>']
        y += 30

    # Activity
    svg += ['<rect x="610" y="220" width="548" height="220" rx="16" fill="#05131d" stroke="#173b50"/>',
            '<text x="630" y="250" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="750">Recent Public Activity Mix</text>',
            '<text x="630" y="269" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="10">Most recent public GitHub events</text>']
    y = 296
    for name, value in act_items or [("No activity", 0)]:
        w = max(2, round(300 * value / act_max))
        svg += [f'<text x="630" y="{y+12}" fill="#b8d0dc" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(name)}</text>',
                f'<rect x="775" y="{y}" width="300" height="14" rx="5" fill="#102532"/>',
                f'<rect x="775" y="{y}" width="{w}" height="14" rx="5" fill="#3988ff"/>',
                f'<text x="1093" y="{y+12}" fill="#eaf9ff" font-family="ui-monospace,Consolas,monospace" font-size="10">{value}</text>']
        y += 30

    # Repositories
    svg += ['<rect x="42" y="464" width="548" height="190" rx="16" fill="#05131d" stroke="#173b50"/>',
            '<text x="62" y="494" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="750">Largest Public Repositories</text>',
            '<text x="62" y="513" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="10">Relative GitHub-reported repository size</text>']
    y = 536
    for repo in top_repos:
        size = int(repo.get("size", 0))
        w = max(2, round(300 * size / repo_max))
        svg += [f'<text x="62" y="{y+11}" fill="#b8d0dc" font-family="Segoe UI,Arial,sans-serif" font-size="10">{esc(repo["name"][:24])}</text>',
                f'<rect x="225" y="{y}" width="270" height="12" rx="4" fill="#102532"/>',
                f'<rect x="225" y="{y}" width="{max(2, round(270*size/repo_max))}" height="12" rx="4" fill="#2d86ff"/>',
                f'<text x="520" y="{y+11}" fill="#ddecf3" font-family="ui-monospace,Consolas,monospace" font-size="9">{size} KB</text>']
        y += 21

    # Trend
    svg += ['<rect x="610" y="464" width="548" height="190" rx="16" fill="#05131d" stroke="#173b50"/>',
            '<text x="630" y="494" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="750">14-Day Public Activity Signal</text>',
            '<text x="630" y="513" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="10">Public GitHub events over the last fourteen days</text>']
    x0, y0, w0, h0 = 650, 540, 465, 78
    points = []
    for i, (d, value) in enumerate(zip(days, vals)):
        x = x0 + round(w0 * i / 13)
        y = y0 + h0 - round(h0 * value / vmax)
        points.append(f"{x},{y}")
        svg += [f'<circle cx="{x}" cy="{y}" r="3" fill="#51eaff"><title>{d.isoformat()}: {value} events</title></circle>']
    svg += [f'<polyline points="{" ".join(points)}" fill="none" stroke="#4fcfff" stroke-width="2.5"/>',
            f'<text x="{x0}" y="638" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="9">{days[0].strftime("%b %d")}</text>',
            f'<text x="{x0+w0}" y="638" text-anchor="end" fill="#64879b" font-family="Segoe UI,Arial,sans-serif" font-size="9">{days[-1].strftime("%b %d")}</text>',
            '<rect x="42" y="675" width="1116" height="2" rx="1" fill="#0c5067"><animate attributeName="x" values="42;1080;42" dur="9s" repeatCount="indefinite"/></rect>',
            '</svg>']

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(svg), encoding="utf-8")


if __name__ == "__main__":
    main()
