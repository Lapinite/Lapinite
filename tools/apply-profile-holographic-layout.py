from pathlib import Path
import re

path = Path("README.md")
text = path.read_text(encoding="utf-8")

replacements = {
    "./assets/hero-dark.svg": "./assets/hero-dark-v4.svg",
    "./assets/hero-light.svg": "./assets/hero-light-v4.svg",
    "./assets/hero-dark-v2.svg": "./assets/hero-dark-v4.svg",
    "./assets/hero-light-v2.svg": "./assets/hero-light-v4.svg",
    "./assets/hero-dark-v3.svg": "./assets/hero-dark-v4.svg",
    "./assets/hero-light-v3.svg": "./assets/hero-light-v4.svg",
    "assets/profile/command-core.svg": "assets/profile/command-core-v3.svg",
    "assets/profile/command-core-v2.svg": "assets/profile/command-core-v3.svg",
    "assets/profile/neural-core.svg": "assets/profile/neural-core-v3.svg",
    "assets/profile/neural-core-v2.svg": "assets/profile/neural-core-v3.svg",
    "assets/profile/external-services.svg": "assets/profile/external-services-v2.svg",
    "assets/profile/data-platform.svg": "assets/profile/data-platform-v2.svg",
    "assets/profile/roadmap.svg": "assets/profile/roadmap-v2.svg",
    "assets/profile/core-products.svg": "assets/profile/core-products-v2.svg",
    "assets/profile/tech-stack.svg": "assets/profile/tech-stack-v2.svg",
    "assets/profile/ecosystem-overview.svg": "assets/profile/ecosystem-overview-v2.svg",
    "assets/profile/platform-areas.svg": "assets/profile/platform-areas-v2.svg",
    "assets/profile/experience-commerce.svg": "assets/profile/experience-commerce-v2.svg",
    "assets/profile/developer-network.svg": "assets/profile/developer-network-v2.svg",
    "assets/profile/contributions.svg": "assets/profile/contributions-v2.svg",
    "assets/profile/activity-feed.svg": "assets/profile/activity-feed-v2.svg",
    "assets/profile/repository-health.svg": "assets/profile/repository-health-v2.svg",
    "assets/profile/analytics-overview.svg": "assets/profile/analytics-overview-v2.svg",
    "assets/profile/pacman.svg": "assets/profile/pacman-v2.svg",
}
for old, new in replacements.items():
    text = text.replace(old, new)

account_block = '''<h3 align="center">Live Account Overview</h3>

<!-- PROFILE_SUMMARY_START -->
<p align="center">
  <img width="100%" src="assets/profile/account-overview-v2.svg" alt="Leviathan public account overview HUD">
</p>
<!-- PROFILE_SUMMARY_END -->

<!-- REPOSITORY_AGGREGATES_START -->
<!-- REPOSITORY_AGGREGATES_END -->'''
text = re.sub(
    r'<h3 align="center">Live Account Overview</h3>.*?<!-- REPOSITORY_AGGREGATES_END -->',
    account_block,
    text,
    flags=re.S,
)

launcher_block = '''<h3 align="center">Leviathan Launcher</h3>

<p align="center">
  <a href="https://github.com/Lapinite/Leviathan-Launcher"><img width="100%" src="assets/profile/launcher-status-v2.svg" alt="Leviathan Launcher public status HUD"></a>
</p>'''
text = re.sub(
    r'<h3 align="center">Leviathan Launcher</h3>.*?(?=\n## Contribution Activity)',
    launcher_block + '\n',
    text,
    flags=re.S,
)

text = re.sub(r'\n{4,}', '\n\n\n', text)
path.write_text(text, encoding="utf-8", newline="\n")
