from pathlib import Path

path = Path('README.md')
text = path.read_text(encoding='utf-8')

old_languages = '''<h3 align="center">Languages & Markup</h3>
<p align="center"><img src="https://skillicons.dev/icons?i=java,c,cpp,cs,js,kotlin,py,lua,php,powershell,html,css,md&perline=7" alt="Languages"></p>
<p align="center"><sub>Java 21 · JavaScript · PHP · Kotlin · Python · C · C++ · C# · Lua · PowerShell · Skript · HTML · CSS · Markdown · JSON · YAML</sub></p>'''

new_languages = '''<h3 align="center">Current Leviathan Development Stack</h3>
<p align="center"><img src="https://skillicons.dev/icons?i=java,js,kotlin,powershell,html,css,gradle,githubactions,windows&perline=9" alt="Current Leviathan development stack"></p>
<p align="center"><sub>Java 21 · JavaScript · HTML · CSS · PowerShell · Kotlin DSL / Gradle · Windows CMD · Shell · Inno Setup · JSON · YAML · Markdown</sub></p>
<p align="center"><sub>High-level technology names only. Proprietary Leviathan source code remains private.</sub></p>'''

if old_languages not in text:
    raise SystemExit('Expected Languages & Markup block not found')
text = text.replace(old_languages, new_languages, 1)

# Make launcher metric badges act like the controls they visually resemble.
replacements = {
    '<img src="https://img.shields.io/github/last-commit/Lapinite/Leviathan-Launcher?style=flat-square&label=Last%20Commit" alt="Last commit">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/commits/main"><img src="https://img.shields.io/github/last-commit/Lapinite/Leviathan-Launcher?style=flat-square&label=Last%20Commit" alt="Last commit"></a>',
    '<img src="https://img.shields.io/github/repo-size/Lapinite/Leviathan-Launcher?style=flat-square&label=Size" alt="Repository size">': '<a href="https://github.com/Lapinite/Leviathan-Launcher"><img src="https://img.shields.io/github/repo-size/Lapinite/Leviathan-Launcher?style=flat-square&label=Size" alt="Repository size"></a>',
    '<img src="https://img.shields.io/github/languages/top/Lapinite/Leviathan-Launcher?style=flat-square&label=Language" alt="Top language">': '<a href="https://github.com/Lapinite/Leviathan-Launcher"><img src="https://img.shields.io/github/languages/top/Lapinite/Leviathan-Launcher?style=flat-square&label=Language" alt="Top language"></a>',
    '<img src="https://img.shields.io/github/last-commit/Lapinite/Leviathan-Launcher?style=flat-square&label=Last%20Commit" alt="Last commit">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/commits/main"><img src="https://img.shields.io/github/last-commit/Lapinite/Leviathan-Launcher?style=flat-square&label=Last%20Commit" alt="Last commit"></a>',
    '<img src="https://img.shields.io/github/commit-activity/m/Lapinite/Leviathan-Launcher?style=flat-square&label=Monthly%20Commits" alt="Monthly commit activity">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/commits/main"><img src="https://img.shields.io/github/commit-activity/m/Lapinite/Leviathan-Launcher?style=flat-square&label=Monthly%20Commits" alt="Monthly commit activity"></a>',
    '<img src="https://img.shields.io/github/repo-size/Lapinite/Leviathan-Launcher?style=flat-square&label=Repo%20Size" alt="Repository size">': '<a href="https://github.com/Lapinite/Leviathan-Launcher"><img src="https://img.shields.io/github/repo-size/Lapinite/Leviathan-Launcher?style=flat-square&label=Repo%20Size" alt="Repository size"></a>',
    '<img src="https://img.shields.io/github/stars/Lapinite/Leviathan-Launcher?style=flat-square&label=Stars" alt="Stars">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/stargazers"><img src="https://img.shields.io/github/stars/Lapinite/Leviathan-Launcher?style=flat-square&label=Stars" alt="Stars"></a>',
    '<img src="https://img.shields.io/github/forks/Lapinite/Leviathan-Launcher?style=flat-square&label=Forks" alt="Forks">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/forks"><img src="https://img.shields.io/github/forks/Lapinite/Leviathan-Launcher?style=flat-square&label=Forks" alt="Forks"></a>',
    '<img src="https://img.shields.io/github/watchers/Lapinite/Leviathan-Launcher?style=flat-square&label=Watchers" alt="Watchers">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/watchers"><img src="https://img.shields.io/github/watchers/Lapinite/Leviathan-Launcher?style=flat-square&label=Watchers" alt="Watchers"></a>',
    '<img src="https://img.shields.io/github/contributors/Lapinite/Leviathan-Launcher?style=flat-square&label=Contributors" alt="Contributors">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/graphs/contributors"><img src="https://img.shields.io/github/contributors/Lapinite/Leviathan-Launcher?style=flat-square&label=Contributors" alt="Contributors"></a>',
    '<img src="https://img.shields.io/github/issues/Lapinite/Leviathan-Launcher?style=flat-square&label=Open%20Issues" alt="Open issues">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/issues"><img src="https://img.shields.io/github/issues/Lapinite/Leviathan-Launcher?style=flat-square&label=Open%20Issues" alt="Open issues"></a>',
    '<img src="https://img.shields.io/github/issues-closed/Lapinite/Leviathan-Launcher?style=flat-square&label=Closed%20Issues" alt="Closed issues">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/Lapinite/Leviathan-Launcher?style=flat-square&label=Closed%20Issues" alt="Closed issues"></a>',
    '<img src="https://img.shields.io/github/issues-pr/Lapinite/Leviathan-Launcher?style=flat-square&label=Open%20PRs" alt="Open pull requests">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/pulls"><img src="https://img.shields.io/github/issues-pr/Lapinite/Leviathan-Launcher?style=flat-square&label=Open%20PRs" alt="Open pull requests"></a>',
    '<img src="https://img.shields.io/github/issues-pr-closed/Lapinite/Leviathan-Launcher?style=flat-square&label=Closed%20PRs" alt="Closed pull requests">': '<a href="https://github.com/Lapinite/Leviathan-Launcher/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed/Lapinite/Leviathan-Launcher?style=flat-square&label=Closed%20PRs" alt="Closed pull requests"></a>',
}

for old, new in replacements.items():
    text = text.replace(old, new)

# The second launcher metric panel uses shorter alt labels.
short_metric_links = {
    '<img src="https://img.shields.io/github/stars/Lapinite/Leviathan-Launcher?style=flat-square&label=Stars" alt="Stars">': 'https://github.com/Lapinite/Leviathan-Launcher/stargazers',
    '<img src="https://img.shields.io/github/forks/Lapinite/Leviathan-Launcher?style=flat-square&label=Forks" alt="Forks">': 'https://github.com/Lapinite/Leviathan-Launcher/forks',
    '<img src="https://img.shields.io/github/watchers/Lapinite/Leviathan-Launcher?style=flat-square&label=Watchers" alt="Watchers">': 'https://github.com/Lapinite/Leviathan-Launcher/watchers',
    '<img src="https://img.shields.io/github/contributors/Lapinite/Leviathan-Launcher?style=flat-square&label=Contributors" alt="Contributors">': 'https://github.com/Lapinite/Leviathan-Launcher/graphs/contributors',
    '<img src="https://img.shields.io/github/issues/Lapinite/Leviathan-Launcher?style=flat-square&label=Open%20Issues" alt="Open issues">': 'https://github.com/Lapinite/Leviathan-Launcher/issues',
    '<img src="https://img.shields.io/github/issues-closed/Lapinite/Leviathan-Launcher?style=flat-square&label=Closed%20Issues" alt="Closed issues">': 'https://github.com/Lapinite/Leviathan-Launcher/issues?q=is%3Aissue+is%3Aclosed',
    '<img src="https://img.shields.io/github/issues-pr/Lapinite/Leviathan-Launcher?style=flat-square&label=Open%20PRs" alt="Open PRs">': 'https://github.com/Lapinite/Leviathan-Launcher/pulls',
    '<img src="https://img.shields.io/github/issues-pr-closed/Lapinite/Leviathan-Launcher?style=flat-square&label=Closed%20PRs" alt="Closed PRs">': 'https://github.com/Lapinite/Leviathan-Launcher/pulls?q=is%3Apr+is%3Aclosed',
}
for badge, href in short_metric_links.items():
    if badge in text and f'<a href="{href}">{badge}</a>' not in text:
        text = text.replace(badge, f'<a href="{href}">{badge}</a>')

path.write_text(text, encoding='utf-8')
print('README profile technology and badge-link updates applied.')
