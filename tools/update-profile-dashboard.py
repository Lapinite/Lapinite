from __future__ import annotations

import html
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = "Lapinite"
README = Path("README.md")
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
    new_text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not find marker block: {start}")
    return new_text


def event_description(event: dict) -> tuple[str, str]:
    event_type = event.get("type", "Activity")
    repo = html.escape(event.get("repo", {}).get("name", "GitHub"))
    payload = event.get("payload", {})
    repo_url = f"https://github.com/{repo}"

    if event_type == "PushEvent":
        count = payload.get("distinct_size") or payload.get("size") or len(payload.get("commits", []))
        ref = payload.get("ref", "").replace("refs/heads/", "")
        if count:
            label = f"Pushed {count} commit{'s' if count != 1 else ''} to {repo}"
        else:
            label = f"Pushed updates to {repo}"
        if ref:
            label += f" ({html.escape(ref)})"
        return label, f"{repo_url}/commits/{html.escape(ref)}" if ref else repo_url

    if event_type == "PullRequestEvent":
        pr = payload.get("pull_request", {})
        number = pr.get("number", "")
        action = payload.get("action", "updated")
        if pr.get("merged_at"):
            action = "merged"
        return f"{action.capitalize()} pull request #{number} in {repo}", pr.get("html_url", repo_url)

    if event_type == "IssuesEvent":
        issue = payload.get("issue", {})
        number = issue.get("number", "")
        action = payload.get("action", "updated")
        return f"{action.capitalize()} issue #{number} in {repo}", issue.get("html_url", repo_url)

    if event_type == "IssueCommentEvent":
        issue = payload.get("issue", {})
        number = issue.get("number", "")
        return f"Commented on #{number} in {repo}", issue.get("html_url", repo_url)

    if event_type == "ReleaseEvent":
        release = payload.get("release", {})
        action = payload.get("action", "updated")
        name = html.escape(release.get("name") or release.get("tag_name") or "release")
        return f"{action.capitalize()} {name} in {repo}", release.get("html_url", repo_url)

    if event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "item")
        ref = payload.get("ref")
        suffix = f" {html.escape(str(ref))}" if ref else ""
        return f"Created {ref_type}{suffix} in {repo}", repo_url

    if event_type == "ForkEvent":
        forkee = payload.get("forkee", {})
        return f"Forked {repo}", forkee.get("html_url", repo_url)

    if event_type == "WatchEvent":
        return f"Starred {repo}", repo_url

    return f"{html.escape(event_type.replace('Event', ''))} in {repo}", repo_url


def build_activity(events: list[dict]) -> str:
    rows = []
    for event in events[:8]:
        desc, url = event_description(event)
        created = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00")).astimezone(timezone.utc)
        stamp = created.strftime("%Y-%m-%d %H:%M UTC")
        rows.append(
            f'<tr><td><a href="{html.escape(url, quote=True)}">{desc}</a></td><td align="right"><sub>{stamp}</sub></td></tr>'
        )
    if not rows:
        rows.append('<tr><td align="center">No recent public activity found.</td></tr>')
    return "\n".join([
        '<table align="center" width="100%">',
        '<tr><th align="left">Activity</th><th align="right">When</th></tr>',
        *rows,
        '</table>',
    ])


def size_label(kb: int) -> str:
    if kb >= 1024:
        return f"{kb / 1024:.1f} MB"
    return f"{kb} KB"


def build_freshness(repos: list[dict]) -> str:
    public = [r for r in repos if not r.get("private")]
    public.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    rows = []
    for repo in public[:7]:
        pushed = repo.get("pushed_at") or ""
        pushed_date = pushed[:10] if pushed else "unknown"
        name = html.escape(repo["name"])
        url = html.escape(repo["html_url"], quote=True)
        rows.append(
            f'<tr><td><a href="{url}">{name}</a></td>'
            f'<td>{pushed_date}</td>'
            f'<td align="right">{size_label(int(repo.get("size", 0)))}</td>'
            f'<td align="right">{repo.get("stargazers_count", 0)}</td>'
            f'<td align="right">{repo.get("forks_count", 0)}</td>'
            f'<td align="right">{repo.get("open_issues_count", 0)}</td></tr>'
        )
    return "\n".join([
        '<table align="center" width="100%">',
        '<tr>',
        '<th align="left">Repository</th>',
        '<th align="left">Last Push</th>',
        '<th align="right">Size</th>',
        '<th align="right">Stars</th>',
        '<th align="right">Forks</th>',
        '<th align="right">Open Issues</th>',
        '</tr>',
        *rows,
        '</table>',
    ])


def ensure_contribution_graph(text: str) -> str:
    marker = '<h3 align="center">Recent Public Activity</h3>'
    block = '''<h3 align="center">Contributions in the Last Year</h3>

<p align="center">
  <a href="https://github.com/Lapinite?tab=overview">
    <img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=Lapinite&theme=github-compact&hide_border=true&area=true&hide_title=true" alt="Lapinite contributions in the last year">
  </a>
</p>

'''
    if '<h3 align="center">Contributions in the Last Year</h3>' in text:
        return text
    if marker not in text:
        raise RuntimeError("Recent Public Activity heading not found")
    return text.replace(marker, block + marker, 1)


def main() -> None:
    text = README.read_text(encoding="utf-8")
    events = api(f"/users/{USER}/events/public?per_page=30")
    repos = api(f"/users/{USER}/repos?per_page=100&sort=pushed&direction=desc&type=owner")

    text = ensure_contribution_graph(text)
    text = replace_marked(
        text,
        '<!-- RECENT_ACTIVITY_START -->',
        '<!-- RECENT_ACTIVITY_END -->',
        build_activity(events),
    )
    text = replace_marked(
        text,
        '<!-- REPOSITORY_FRESHNESS_START -->',
        '<!-- REPOSITORY_FRESHNESS_END -->',
        build_freshness(repos),
    )

    README.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
