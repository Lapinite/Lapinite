from __future__ import annotations

import html
import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

USER = "Lapinite"
README = Path("README.md")
ASSETS = Path("assets/profile")
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(path: str):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Lapinite-profile-dashboard",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def replace_marked(text: str, start: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    replacement = f"{start}\n{body.rstrip()}\n{end}"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not find marker block: {start}")
    return updated


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def event_description(event: dict) -> tuple[str, str]:
    event_type = event.get("type", "Activity")
    repo = event.get("repo", {}).get("name", "GitHub")
    payload = event.get("payload", {})
    repo_url = f"https://github.com/{repo}"

    if event_type == "PushEvent":
        count = payload.get("distinct_size") or payload.get("size") or len(payload.get("commits", []))
        ref = payload.get("ref", "").replace("refs/heads/", "")
        label = f"Pushed {count} commit{'s' if count != 1 else ''} to {repo}" if count else f"Pushed updates to {repo}"
        if ref:
            label += f" ({ref})"
        return label, f"{repo_url}/commits/{ref}" if ref else repo_url

    if event_type == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        action = "merged" if pr.get("merged_at") else payload.get("action", "updated")
        return f"{action.capitalize()} pull request #{pr.get('number', '')} in {repo}", pr.get("html_url", repo_url)

    if event_type == "IssuesEvent":
        issue = payload.get("issue", {})
        return f"{payload.get('action', 'updated').capitalize()} issue #{issue.get('number', '')} in {repo}", issue.get("html_url", repo_url)

    if event_type == "IssueCommentEvent":
        issue = payload.get("issue", {})
        return f"Commented on #{issue.get('number', '')} in {repo}", issue.get("html_url", repo_url)

    if event_type == "CreateEvent":
        ref = payload.get("ref")
        suffix = f" {ref}" if ref else ""
        return f"Created {payload.get('ref_type', 'item')}{suffix} in {repo}", repo_url

    if event_type == "ReleaseEvent":
        release = payload.get("release", {})
        name = release.get("name") or release.get("tag_name") or "release"
        return f"{payload.get('action', 'updated').capitalize()} {name} in {repo}", release.get("html_url", repo_url)

    if event_type == "ForkEvent":
        return f"Forked {repo}", payload.get("forkee", {}).get("html_url", repo_url)
    if event_type == "WatchEvent":
        return f"Starred {repo}", repo_url
    return f"{event_type.replace('Event', '')} in {repo}", repo_url


def build_activity(events: list[dict]) -> str:
    rows = []
    for event in events[:8]:
        description, url = event_description(event)
        created = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
        stamp = created.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        rows.append(f'<tr><td><a href="{esc(url)}">{esc(description)}</a></td><td align="right"><sub>{stamp}</sub></td></tr>')
    if not rows:
        rows.append('<tr><td>No recent public activity found.</td><td></td></tr>')
    return "\n".join([
        '<table align="center" width="100%">',
        '<tr><th align="left">Activity</th><th align="right">When</th></tr>',
        *rows,
        '</table>',
    ])


def size_label(kb: int) -> str:
    return f"{kb / 1024:.1f} MB" if kb >= 1024 else f"{kb} KB"


def build_freshness(repos: list[dict]) -> str:
    repos = sorted(repos, key=lambda repo: repo.get("pushed_at") or "", reverse=True)
    rows = []
    for repo in repos[:7]:
        pushed = (repo.get("pushed_at") or "unknown")[:10]
        rows.append(
            f'<tr><td><a href="{esc(repo["html_url"])}">{esc(repo["name"])}</a></td>'
            f'<td>{pushed}</td><td align="right">{size_label(int(repo.get("size", 0)))}</td>'
            f'<td align="right">{repo.get("stargazers_count", 0)}</td>'
            f'<td align="right">{repo.get("forks_count", 0)}</td>'
            f'<td align="right">{repo.get("open_issues_count", 0)}</td></tr>'
        )
    return "\n".join([
        '<table align="center" width="100%">',
        '<tr><th align="left">Repository</th><th align="left">Last Push</th><th align="right">Size</th><th align="right">Stars</th><th align="right">Forks</th><th align="right">Open Issues</th></tr>',
        *rows,
        '</table>',
    ])


def svg_open(width: int, height: int, title: str, subtitle: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect x="0.5" y="0.5" width="99.85%" height="99.4%" rx="12" fill="#0d1117" stroke="#30363d"/>',
        f'<text x="24" y="32" fill="#f0f6fc" font-family="Segoe UI,Arial,sans-serif" font-size="17" font-weight="700">{esc(title)}</text>',
        f'<text x="24" y="51" fill="#8b949e" font-family="Segoe UI,Arial,sans-serif" font-size="10">{esc(subtitle)}</text>',
    ]


def write_bar(path: Path, title: str, subtitle: str, items: list[tuple[str, int]], suffix: str = "") -> None:
    items = items[:7]
    height = 82 + max(1, len(items)) * 34
    lines = svg_open(760, height, title, subtitle)
    maximum = max((value for _, value in items), default=1) or 1
    if not items:
        items = [("No public data yet", 0)]
    y = 72
    for label, value in items:
        width = max(2, round(410 * value / maximum)) if value else 2
        lines.extend([
            f'<text x="24" y="{y + 13}" fill="#c9d1d9" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(label[:29])}</text>',
            f'<rect x="210" y="{y}" width="410" height="16" rx="4" fill="#21262d"/>',
            f'<rect x="210" y="{y}" width="{width}" height="16" rx="4" fill="#2f81f7"/>',
            f'<text x="638" y="{y + 13}" fill="#f0f6fc" font-family="Segoe UI,Arial,sans-serif" font-size="11">{value:,}{esc(suffix)}</text>',
        ])
        y += 34
    lines.append('</svg>')
    path.write_text("\n".join(lines), encoding="utf-8")


def write_languages(path: Path, languages: Counter[str]) -> None:
    items = languages.most_common(7)
    total = sum(value for _, value in items) or 1
    height = 82 + max(1, len(items)) * 34
    lines = svg_open(760, height, "Public Code Language Mix", "Aggregated from public repositories only")
    if not items:
        items = [("No public language data yet", 0)]
    y = 72
    for label, value in items:
        pct = value * 100 / total
        width = max(2, round(410 * pct / 100)) if value else 2
        lines.extend([
            f'<text x="24" y="{y + 13}" fill="#c9d1d9" font-family="Segoe UI,Arial,sans-serif" font-size="11">{esc(label)}</text>',
            f'<rect x="210" y="{y}" width="410" height="16" rx="4" fill="#21262d"/>',
            f'<rect x="210" y="{y}" width="{width}" height="16" rx="4" fill="#00b4d8"/>',
            f'<text x="638" y="{y + 13}" fill="#f0f6fc" font-family="Segoe UI,Arial,sans-serif" font-size="11">{pct:.1f}%</text>',
        ])
        y += 34
    lines.append('</svg>')
    path.write_text("\n".join(lines), encoding="utf-8")


def public_commits_last_year(repos: list[dict]) -> Counter[date]:
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


def write_heatmap(path: Path, counts: Counter[date]) -> None:
    today = datetime.now(timezone.utc).date()
    first_day = today - timedelta(days=364)
    grid_start = first_day - timedelta(days=(first_day.weekday() + 1) % 7)
    maximum = max(counts.values(), default=1) or 1
    total = sum(counts.values())
    lines = svg_open(900, 190, "Public Commit Activity, Last 12 Months", f"{total:,} commits across public repositories")
    x0, y0, cell, gap = 108, 72, 11, 3
    for index, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        lines.append(f'<text x="58" y="{y0 + index * (cell + gap) + 9}" fill="#8b949e" font-family="Segoe UI,Arial,sans-serif" font-size="10">{label}</text>')
    current_month = None
    for week in range(53):
        week_start = grid_start + timedelta(days=week * 7)
        if week_start.month != current_month:
            current_month = week_start.month
            lines.append(f'<text x="{x0 + week * (cell + gap)}" y="66" fill="#8b949e" font-family="Segoe UI,Arial,sans-serif" font-size="9">{week_start.strftime("%b")}</text>')
        for dow in range(7):
            day = week_start + timedelta(days=dow)
            count = counts.get(day, 0)
            ratio = count / maximum if maximum else 0
            fill = "#161b22" if count == 0 else "#0e4429" if ratio <= .25 else "#006d32" if ratio <= .5 else "#26a641" if ratio <= .75 else "#39d353"
            x = x0 + week * (cell + gap)
            y = y0 + dow * (cell + gap)
            lines.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}"><title>{day.isoformat()}: {count} public commits</title></rect>')
    lines.append('</svg>')
    path.write_text("\n".join(lines), encoding="utf-8")


def write_activity_trend(path: Path, events: list[dict]) -> None:
    today = datetime.now(timezone.utc).date()
    event_counts = Counter(datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")).date() for event in events)
    days = [today - timedelta(days=offset) for offset in range(13, -1, -1)]
    values = [event_counts[day] for day in days]
    maximum = max(values, default=1) or 1
    lines = svg_open(760, 245, "Recent Public Activity Trend", "Public GitHub events over the last 14 days")
    x0, y0, chart_w, chart_h = 52, 75, 675, 120
    points = []
    for index, (day, value) in enumerate(zip(days, values)):
        x = x0 + round(chart_w * index / 13)
        y = y0 + chart_h - round(chart_h * value / maximum)
        points.append(f"{x},{y}")
        lines.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#58a6ff"><title>{day.isoformat()}: {value} events</title></circle>')
        if index in (0, 6, 13):
            lines.append(f'<text x="{x}" y="222" text-anchor="middle" fill="#8b949e" font-family="Segoe UI,Arial,sans-serif" font-size="10">{day.strftime("%b %d")}</text>')
    lines.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#58a6ff" stroke-width="3"/>')
    lines.append('</svg>')
    path.write_text("\n".join(lines), encoding="utf-8")


def analytics_block() -> str:
    return '''<h3 align="center">Public Development Analytics</h3>

<table align="center" width="100%">
<tr>
<td width="50%" valign="top"><img width="100%" src="assets/profile/languages.svg" alt="Public code language mix"></td>
<td width="50%" valign="top"><img width="100%" src="assets/profile/activity-types.svg" alt="Recent public activity mix"></td>
</tr>
<tr>
<td width="50%" valign="top"><img width="100%" src="assets/profile/repository-sizes.svg" alt="Largest public repositories"></td>
<td width="50%" valign="top"><img width="100%" src="assets/profile/activity-trend.svg" alt="Recent public activity trend"></td>
</tr>
</table>

<p align="center"><sub>Generated from public GitHub repositories and public activity only. Private repositories and proprietary source code are excluded.</sub></p>'''


def update_layout(text: str) -> str:
    contribution_pattern = re.compile(r'<h3 align="center">Contributions in the Last Year</h3>.*?(?=<h3 align="center">Recent Public Activity</h3>)', re.S)
    contribution = '''<h3 align="center">Public Commit Activity in the Last Year</h3>

<p align="center">
  <a href="https://github.com/Lapinite?tab=overview"><img width="100%" src="assets/profile/contributions.svg" alt="Public commit activity in the last year"></a>
</p>

'''
    text, count = contribution_pattern.subn(contribution, text, count=1)
    if count != 1:
        raise RuntimeError("Contribution activity block not found")

    if '<!-- PUBLIC_ANALYTICS_START -->' in text:
        text = replace_marked(text, '<!-- PUBLIC_ANALYTICS_START -->', '<!-- PUBLIC_ANALYTICS_END -->', analytics_block())
    else:
        marker = '<h3 align="center">Leviathan Launcher</h3>'
        if marker not in text:
            raise RuntimeError("Leviathan Launcher section not found")
        text = text.replace(marker, f'<!-- PUBLIC_ANALYTICS_START -->\n{analytics_block()}\n<!-- PUBLIC_ANALYTICS_END -->\n\n{marker}', 1)

    text = re.sub(r'\n---\s*\n\s*(<h2 align="center">Contribution Activity</h2>)', r'\n\n\1', text, count=1)
    return text


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    text = README.read_text(encoding="utf-8")
    events = api(f"/users/{USER}/events/public?per_page=100")
    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed&direction=desc&type=owner")
    public_repos = [repo for repo in repos if not repo.get("private")]

    languages: Counter[str] = Counter()
    for repo in public_repos:
        try:
            languages.update(api(f'/repos/{repo["full_name"]}/languages'))
        except Exception as exc:
            print(f"Language lookup skipped for {repo['full_name']}: {exc}")

    activity_types = Counter(event.get("type", "Other").replace("Event", "") for event in events)
    repo_sizes = sorted(((repo["name"], int(repo.get("size", 0))) for repo in public_repos), key=lambda item: item[1], reverse=True)
    commit_counts = public_commits_last_year(public_repos)

    write_heatmap(ASSETS / "contributions.svg", commit_counts)
    write_languages(ASSETS / "languages.svg", languages)
    write_bar(ASSETS / "activity-types.svg", "Recent Public Activity Mix", "Most recent public GitHub events", activity_types.most_common(7))
    write_bar(ASSETS / "repository-sizes.svg", "Largest Public Repositories", "Repository size reported by GitHub", repo_sizes, " KB")
    write_activity_trend(ASSETS / "activity-trend.svg", events)

    text = update_layout(text)
    text = replace_marked(text, '<!-- RECENT_ACTIVITY_START -->', '<!-- RECENT_ACTIVITY_END -->', build_activity(events))
    text = replace_marked(text, '<!-- REPOSITORY_FRESHNESS_START -->', '<!-- REPOSITORY_FRESHNESS_END -->', build_freshness(public_repos))
    README.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
