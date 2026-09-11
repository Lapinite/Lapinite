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
ASSETS = Path("assets/profile")
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def api(path: str):
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Lapinite-profile-visuals",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def public_commit_counts(repos: list[dict]) -> Counter[date]:
    counts: Counter[date] = Counter()
    since = (datetime.now(timezone.utc) - timedelta(days=365)).isoformat()
    for repo in repos:
        full_name = repo["full_name"]
        for page in range(1, 11):
            query = urllib.parse.urlencode({"author": USER, "since": since, "per_page": 100, "page": page})
            try:
                commits = api(f"/repos/{full_name}/commits?{query}")
            except Exception as exc:
                print(f"Commit history skipped for {full_name}: {exc}")
                break
            if not isinstance(commits, list) or not commits:
                break
            for commit in commits:
                stamp = commit.get("commit", {}).get("author", {}).get("date") or commit.get("commit", {}).get("committer", {}).get("date")
                if stamp:
                    counts[datetime.fromisoformat(stamp.replace("Z", "+00:00")).date()] += 1
            if len(commits) < 100:
                break
    return counts


def longest_streak(counts: Counter[date]) -> int:
    active = sorted(day for day, value in counts.items() if value > 0)
    if not active:
        return 0
    longest = current = 1
    for previous, current_day in zip(active, active[1:]):
        if current_day == previous + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def svg_defs() -> str:
    return '''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#020913"/><stop offset="0.55" stop-color="#061726"/><stop offset="1" stop-color="#020b13"/></linearGradient>
<linearGradient id="cyan" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#087dff"/><stop offset="0.52" stop-color="#29e7ff"/><stop offset="1" stop-color="#00a7ff"/></linearGradient>
<radialGradient id="core"><stop offset="0" stop-color="#65f3ff" stop-opacity=".9"/><stop offset=".38" stop-color="#00c8ff" stop-opacity=".28"/><stop offset="1" stop-color="#007dff" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#12344b" stroke-width="1" opacity=".24"/></pattern>
</defs>'''


def panel(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        svg_defs(),
        f'<rect width="{width}" height="{height}" rx="24" fill="url(#bg)"/>',
        f'<rect width="{width}" height="{height}" rx="24" fill="url(#grid)"/>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="23" fill="none" stroke="#173a50"/>',
    ]


def write_contributions(path: Path, counts: Counter[date]) -> None:
    today = datetime.now(timezone.utc).date()
    first_day = today - timedelta(days=364)
    grid_start = first_day - timedelta(days=(first_day.weekday() + 1) % 7)
    total = sum(counts.values())
    active_days = sum(1 for day in (first_day + timedelta(days=i) for i in range(365)) if counts.get(day, 0) > 0)
    streak = longest_streak(counts)
    busiest_day, busiest_count = max(counts.items(), key=lambda item: item[1], default=(today, 0))
    max_count = max(counts.values(), default=1) or 1

    month_counts: list[tuple[str, int]] = []
    for offset in range(11, -1, -1):
        year = today.year
        month = today.month - offset
        while month <= 0:
            month += 12
            year -= 1
        label = date(year, month, 1).strftime("%b")
        value = sum(count for day, count in counts.items() if day.year == year and day.month == month)
        month_counts.append((label, value))

    lines = panel(1200, 430)
    lines += [
        '<text x="42" y="46" fill="#59eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">PUBLIC COMMIT ACTIVITY // 365 DAY SIGNAL</text>',
        '<text x="42" y="72" fill="#7f9eb2" font-family="Segoe UI,Arial,sans-serif" font-size="12">Public repositories only. Private repositories and proprietary source are excluded.</text>',
    ]

    cards = [
        (42, "TOTAL COMMITS", str(total)),
        (278, "ACTIVE DAYS", str(active_days)),
        (514, "LONGEST STREAK", f"{streak} days"),
        (750, "BUSIEST DAY", f"{busiest_count} commits"),
    ]
    for x, label, value in cards:
        lines += [
            f'<rect x="{x}" y="96" width="214" height="70" rx="14" fill="#071724" stroke="#17465e"/>',
            f'<text x="{x+18}" y="119" fill="#668aa1" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1.4">{label}</text>',
            f'<text x="{x+18}" y="150" fill="#edfaff" font-family="Segoe UI,Arial,sans-serif" font-size="24" font-weight="750">{esc(value)}</text>',
        ]
    lines += [
        '<rect x="986" y="96" width="172" height="70" rx="14" fill="#071724" stroke="#17465e"/>',
        '<text x="1004" y="119" fill="#668aa1" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1.4">PEAK DATE</text>',
        f'<text x="1004" y="147" fill="#edfaff" font-family="Segoe UI,Arial,sans-serif" font-size="18" font-weight="700">{busiest_day.strftime("%b %d, %Y")}</text>',
    ]

    x0, y0, cell, gap = 115, 207, 12, 3
    for index, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        lines.append(f'<text x="63" y="{y0 + index*(cell+gap)+10}" fill="#7190a4" font-family="Segoe UI,Arial,sans-serif" font-size="10">{label}</text>')
    current_month = None
    for week in range(53):
        week_start = grid_start + timedelta(days=week * 7)
        if week_start.month != current_month:
            current_month = week_start.month
            lines.append(f'<text x="{x0 + week*(cell+gap)}" y="195" fill="#6d8fa3" font-family="Segoe UI,Arial,sans-serif" font-size="9">{week_start.strftime("%b")}</text>')
        for dow in range(7):
            day = week_start + timedelta(days=dow)
            value = counts.get(day, 0)
            ratio = value / max_count if max_count else 0
            fill = "#0a1822" if value == 0 else "#08344a" if ratio <= .2 else "#075c78" if ratio <= .4 else "#008aa9" if ratio <= .65 else "#16bfd6" if ratio <= .85 else "#61f0ff"
            x = x0 + week*(cell+gap)
            y = y0 + dow*(cell+gap)
            lines.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{fill}" stroke="#0d2b3a" stroke-width=".45"><title>{day.isoformat()}: {value} public commits</title></rect>')

    chart_x, chart_y, chart_w, chart_h = 920, 210, 238, 102
    max_month = max((value for _, value in month_counts), default=1) or 1
    bar_w = 14
    gap_w = 5
    for index, (label, value) in enumerate(month_counts):
        h = max(2, round(chart_h * value / max_month)) if value else 2
        x = chart_x + index*(bar_w+gap_w)
        y = chart_y + chart_h - h
        lines += [
            f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" rx="3" fill="#18bad7"><title>{label}: {value} public commits</title></rect>',
            f'<text x="{x+7}" y="329" text-anchor="middle" fill="#65869a" font-family="Segoe UI,Arial,sans-serif" font-size="7">{label}</text>',
        ]
    lines += [
        '<text x="920" y="195" fill="#84a8bc" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1">MONTHLY OUTPUT</text>',
        '<text x="42" y="395" fill="#66889d" font-family="Segoe UI,Arial,sans-serif" font-size="10">LOW</text>',
        '<rect x="78" y="385" width="12" height="12" rx="2" fill="#0a1822"/><rect x="96" y="385" width="12" height="12" rx="2" fill="#08344a"/><rect x="114" y="385" width="12" height="12" rx="2" fill="#075c78"/><rect x="132" y="385" width="12" height="12" rx="2" fill="#008aa9"/><rect x="150" y="385" width="12" height="12" rx="2" fill="#16bfd6"/><rect x="168" y="385" width="12" height="12" rx="2" fill="#61f0ff"/><text x="190" y="395" fill="#66889d" font-family="Segoe UI,Arial,sans-serif" font-size="10">HIGH</text>',
        '<line x1="42" y1="178" x2="1158" y2="178" stroke="#17384d"/>',
        '<rect x="40" y="410" width="1118" height="2" rx="1" fill="#0b4a61"><animate attributeName="x" values="40;1050;40" dur="8s" repeatCount="indefinite"/></rect>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_roadmap(path: Path) -> None:
    phases = [
        ("01", "RESEARCH", "Complete", "Competitive research, ecosystem mapping, security research"),
        ("02", "ARCHITECTURE", "Complete", "Platform boundaries, repositories, interfaces, release model"),
        ("03", "FOUNDATION", "Complete", "Launcher core, build system, authentication foundation"),
        ("04", "INTEGRATION", "Active", "Client, APIs, Cast, installer, updater, connected services"),
        ("05", "SECURITY", "Active", "Threat hardening, Nimbus, privacy controls, validation gates"),
        ("06", "TESTING", "Active", "Windows retests, compatibility, failure recovery, device validation"),
        ("07", "STABILIZATION", "Current", "v51.0.6 internal baseline, bug fixing, regression control"),
        ("08", "RELEASE PREP", "Locked", "Release checks, signing, distribution validation, documentation"),
    ]
    lines = panel(1200, 720)
    lines += [
        '<text x="42" y="46" fill="#59eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">LEVIATHAN DEVELOPMENT ROADMAP // INTERNAL</text>',
        '<text x="42" y="72" fill="#7f9eb2" font-family="Segoe UI,Arial,sans-serif" font-size="12">Detailed development path. Current work is internal development, testing, stabilization and release preparation only.</text>',
        '<rect x="42" y="94" width="1116" height="58" rx="14" fill="#061724" stroke="#17455d"/>',
        '<text x="62" y="117" fill="#6b8ea4" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1.5">CURRENT BASELINE</text>',
        '<text x="62" y="141" fill="#effbff" font-family="Segoe UI,Arial,sans-serif" font-size="21" font-weight="750">v51.0.6 // Stabilization and validation</text>',
        '<text x="760" y="118" fill="#6b8ea4" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1.5">OUTSTANDING MANUAL GATES</text>',
        '<text x="760" y="141" fill="#b7d0dc" font-family="Segoe UI,Arial,sans-serif" font-size="12">Legacy Fabric 1.8.9 • Modrinth pagination • Installer/uninstall • Physical Android TV Cast</text>',
        '<path d="M96 204 V628" fill="none" stroke="#143a50" stroke-width="6" stroke-linecap="round"/>',
        '<path d="M96 204 V548" fill="none" stroke="#11bad6" stroke-width="6" stroke-linecap="round" opacity=".78"/>',
        '<circle r="5" fill="#64efff" filter="url(#glow)"><animateMotion dur="5.5s" repeatCount="indefinite" path="M96 204 V548"/></circle>',
    ]
    y = 204
    for number, title, status, detail in phases:
        current = status == "Current"
        active = status in {"Complete", "Active", "Current"}
        stroke = "#69f1ff" if current else "#24c9e3" if active else "#405c6c"
        fill = "#0b2938" if current else "#071a25" if active else "#081219"
        lines += [
            f'<circle cx="96" cy="{y}" r="{20 if current else 14}" fill="{fill}" stroke="{stroke}" stroke-width="3"{(" filter=\"url(#glow)\"" if current else "")}/>',
            f'<rect x="142" y="{y-34}" width="1016" height="68" rx="13" fill="#06131e" stroke="#16394d"/>',
            f'<text x="164" y="{y-9}" fill="#5f8ca4" font-family="ui-monospace,Consolas,monospace" font-size="10" letter-spacing="1.2">PHASE {number} // {status.upper()}</text>',
            f'<text x="164" y="{y+15}" fill="{stroke if current else "#eaf8ff"}" font-family="Segoe UI,Arial,sans-serif" font-size="18" font-weight="750">{title}</text>',
            f'<text x="368" y="{y+14}" fill="#83a1b3" font-family="Segoe UI,Arial,sans-serif" font-size="12">{esc(detail)}</text>',
        ]
        if current:
            lines += [
                f'<circle cx="96" cy="{y}" r="7" fill="#70f2ff"><animate attributeName="r" values="5;9;5" dur="2s" repeatCount="indefinite"/></circle>',
                f'<text x="1110" y="{y+5}" text-anchor="end" fill="#67efff" font-family="ui-monospace,Consolas,monospace" font-size="11">CURRENT FOCUS</text>',
            ]
        y += 61
    lines += [
        '<rect x="42" y="654" width="1116" height="38" rx="10" fill="#07141e" stroke="#203c4d"/>',
        '<text x="600" y="678" text-anchor="middle" fill="#7898aa" font-family="ui-monospace,Consolas,monospace" font-size="11">PUBLIC RELEASE GATE REMAINS CLOSED UNTIL VALIDATION, SECURITY, COMPATIBILITY AND DISTRIBUTION CHECKS ARE COMPLETE</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_neural_core(path: Path) -> None:
    nodes = [
        (195, 190, "LAUNCHER", "Player entry"), (195, 285, "CLIENT", "Game experience"), (195, 380, "WEBSITE", "Web surface"), (195, 475, "APP", "Mobile surface"),
        (1005, 180, "AUTH", "Identity"), (1005, 265, "API", "Public services"), (1005, 350, "SDK", "Developer access"), (1005, 435, "STATUS", "Service health"), (1005, 520, "INTEGRATIONS", "Connected systems"),
        (430, 610, "TELEMETRY", "Signals"), (600, 640, "ANALYTICS", "Insights"), (770, 610, "MONITORING", "Reliability"),
        (430, 135, "NIMBUS", "AntiCheat"), (600, 110, "SECURITY", "Protection"), (770, 135, "INTEGRITY", "Validation"),
        (420, 500, "CAST", "TV and device bridge"), (780, 500, "UPDATER", "Update path"),
    ]
    lines = panel(1200, 760)
    lines += [
        '<text x="42" y="46" fill="#59eaff" font-family="ui-monospace,Consolas,monospace" font-size="15" letter-spacing="3">LEVIATHAN NEURAL CORE // PUBLIC ARCHITECTURE MAP</text>',
        '<text x="42" y="72" fill="#7f9eb2" font-family="Segoe UI,Arial,sans-serif" font-size="12">Sanitized high-level system model. Private source, internal endpoints, credentials, database details and sensitive topology are intentionally excluded.</text>',
        '<circle cx="600" cy="365" r="205" fill="url(#core)" opacity=".42"><animate attributeName="opacity" values=".24;.5;.24" dur="6s" repeatCount="indefinite"/></circle>',
    ]

    for x, y, _, _ in nodes:
        lines.append(f'<path d="M600 365 Q{(600+x)//2} {(365+y)//2-25} {x} {y}" fill="none" stroke="#1a7ea3" stroke-width="1.4" opacity=".34"/>')
    secondary = [((195,190),(195,285)),((195,285),(195,380)),((195,380),(195,475)),((1005,180),(1005,265)),((1005,265),(1005,350)),((1005,350),(1005,435)),((1005,435),(1005,520)),((430,610),(600,640)),((600,640),(770,610)),((430,135),(600,110)),((600,110),(770,135)),((420,500),(600,365)),((780,500),(600,365))]
    for (x1,y1),(x2,y2) in secondary:
        lines.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#164d67" stroke-width="1" stroke-dasharray="4 7" opacity=".5"/>')

    signal_paths = [
        ("s1", "M195 190 Q390 245 600 365 Q800 275 1005 180", 6.0, 0),
        ("s2", "M195 285 Q390 310 600 365 Q820 335 1005 265", 5.2, 1.1),
        ("s3", "M420 500 Q500 430 600 365 Q710 430 780 500", 4.8, 2.0),
        ("s4", "M430 135 Q520 220 600 365 Q680 220 770 135", 5.6, .5),
        ("s5", "M430 610 Q515 520 600 365 Q690 520 770 610", 6.2, 1.8),
    ]
    for pid, d, dur, begin in signal_paths:
        lines.append(f'<path id="{pid}" d="{d}" fill="none" stroke="#2adbf3" stroke-width="2" opacity=".14"/>')
        lines.append(f'<circle r="4" fill="#61f1ff" filter="url(#glow)"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>')

    lines += [
        '<circle cx="600" cy="365" r="88" fill="#061a28" stroke="#36e4f7" stroke-width="2.5" filter="url(#glow)"/>',
        '<circle cx="600" cy="365" r="67" fill="none" stroke="#159dc7" stroke-width="1.5" stroke-dasharray="5 9"><animateTransform attributeName="transform" type="rotate" from="0 600 365" to="360 600 365" dur="14s" repeatCount="indefinite"/></circle>',
        '<circle cx="600" cy="365" r="49" fill="none" stroke="#50eafa" stroke-width="1" stroke-dasharray="2 7"><animateTransform attributeName="transform" type="rotate" from="360 600 365" to="0 600 365" dur="10s" repeatCount="indefinite"/></circle>',
        '<text x="600" y="353" text-anchor="middle" fill="#effcff" font-family="Segoe UI,Arial,sans-serif" font-size="23" font-weight="800">LEVIATHAN</text>',
        '<text x="600" y="378" text-anchor="middle" fill="#62dce9" font-family="ui-monospace,Consolas,monospace" font-size="11" letter-spacing="1.5">CORE PLATFORM</text>',
        '<text x="600" y="399" text-anchor="middle" fill="#54788c" font-family="Segoe UI,Arial,sans-serif" font-size="10">orchestration • identity • services • delivery</text>',
    ]

    for x, y, name, subtitle in nodes:
        if y < 170:
            stroke = "#ff9f43"
        elif y > 560:
            stroke = "#43d9a3"
        elif x > 850:
            stroke = "#8174ff"
        else:
            stroke = "#20bddd"
        width = 154 if len(name) < 10 else 178
        lines += [
            f'<rect x="{x-width//2}" y="{y-29}" width="{width}" height="58" rx="13" fill="#061722" stroke="{stroke}" stroke-width="1.4"/>',
            f'<text x="{x}" y="{y-4}" text-anchor="middle" fill="#eaf9ff" font-family="Segoe UI,Arial,sans-serif" font-size="14" font-weight="750">{name}</text>',
            f'<text x="{x}" y="{y+15}" text-anchor="middle" fill="#7897aa" font-family="Segoe UI,Arial,sans-serif" font-size="9.5">{esc(subtitle)}</text>',
        ]

    lines += [
        '<text x="42" y="720" fill="#66889d" font-family="ui-monospace,Consolas,monospace" font-size="10">SIGNAL LEGEND</text>',
        '<circle cx="155" cy="716" r="4" fill="#20bddd"/><text x="168" y="720" fill="#7897aa" font-family="Segoe UI,Arial,sans-serif" font-size="10">Player surfaces</text>',
        '<circle cx="282" cy="716" r="4" fill="#8174ff"/><text x="295" y="720" fill="#7897aa" font-family="Segoe UI,Arial,sans-serif" font-size="10">Platform services</text>',
        '<circle cx="425" cy="716" r="4" fill="#ff9f43"/><text x="438" y="720" fill="#7897aa" font-family="Segoe UI,Arial,sans-serif" font-size="10">Protection</text>',
        '<circle cx="535" cy="716" r="4" fill="#43d9a3"/><text x="548" y="720" fill="#7897aa" font-family="Segoe UI,Arial,sans-serif" font-size="10">Observability</text>',
        '<text x="1158" y="720" text-anchor="end" fill="#58788b" font-family="ui-monospace,Consolas,monospace" font-size="10">PUBLIC SANITIZED MODEL</text>',
        '</svg>',
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed&direction=desc&type=owner")
    public_repos = [repo for repo in repos if not repo.get("private")]
    counts = public_commit_counts(public_repos)
    write_contributions(ASSETS / "contributions.svg", counts)
    write_roadmap(ASSETS / "roadmap.svg")
    write_neural_core(ASSETS / "neural-core.svg")


if __name__ == "__main__":
    main()
