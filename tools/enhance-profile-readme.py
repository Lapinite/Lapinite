from pathlib import Path
import re

path = Path("README.md")
text = path.read_text(encoding="utf-8")

core = '''## Core Products

<p align="center">
  <img width="100%" src="assets/profile/core-products-v2.svg" alt="Animated Leviathan core product map">
</p>

<p align="center"><sub>Leviathan player software and Nimbus server protection are separate product lines connected by shared platform and security principles.</sub></p>

'''

stack = '''## Current Leviathan Development Stack

<p align="center">
  <img width="100%" src="assets/profile/tech-stack-v2.svg" alt="Animated high-level Leviathan development technology stack">
</p>

<p align="center"><sub>High-level technology names only. Proprietary implementation remains private.</sub></p>

'''

areas = '''## Platform Areas

<p align="center">
  <img width="100%" src="assets/profile/platform-areas-v2.svg" alt="Animated public Leviathan platform areas">
</p>

<p align="center"><sub>Player software, platform services, protection and observability shown as a deliberately simplified public domain map.</sub></p>

'''

network = '''## Public Developer Repositories

<p align="center">
  <img width="100%" src="assets/profile/developer-network-v2.svg" alt="Animated Leviathan public developer repository network">
</p>

<p align="center">
<a href="https://github.com/Lapinite/Leviathan-Launcher"><strong>Launcher</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-Docs"><strong>Docs</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-API-Docs"><strong>API Docs</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-SDK"><strong>SDK</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-Integrations"><strong>Integrations</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-Examples"><strong>Examples</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-Server-Tools"><strong>Server Tools</strong></a> ·
<a href="https://github.com/Lapinite/Leviathan-Status"><strong>Status</strong></a>
</p>

'''

text = re.sub(r'## Core Products\n.*?(?=## Current Leviathan Development Stack\n)', core, text, flags=re.S)
text = re.sub(r'## Current Leviathan Development Stack\n.*?(?=## Leviathan Ecosystem\n)', stack, text, flags=re.S)

text = re.sub(r'\n## Platform Areas\n.*?(?=\n## Experience & Commerce Flows\n)', '\n' + areas.rstrip() + '\n', text, flags=re.S)
if '## Platform Areas\n' not in text:
    marker = '## Experience & Commerce Flows\n'
    text = text.replace(marker, areas + marker, 1)

text = re.sub(r'## Public Developer Repositories\n.*?(?=## Leviathan Development Activity\n)', network, text, flags=re.S)

replacements = {
    'Leviathan is under active internal development. The current internal baseline is **v51.0.6**, with stabilization and validation work in progress. No public launcher or installer release is implied by this profile.':
        '<p align="center"><sub>Internal baseline <strong>v51.0.6</strong> • stabilization + validation • no public launcher or installer release</sub></p>',
    'The Neural Core is a deliberately simplified public system map. It communicates the product ecosystem without exposing proprietary source code, private endpoints, internal service topology, credentials or sensitive implementation details.':
        '<p align="center"><sub>Sanitized public architecture view. Proprietary implementation and private topology remain private.</sub></p>',
    'Microsoft account services, Xbox Live, XSTS, Minecraft Services and Mojang/Minecraft platform systems remain external trust boundaries. Leviathan owns only its own account mapping, session/permission state, product state, device/Cast state, telemetry, licensing and other platform data required for Leviathan functionality.':
        '<p align="center"><sub>External identity and game-service trust boundaries remain outside Leviathan ownership.</sub></p>',
    'The data layer is designed as a shared platform capability for accounts, launcher/client state, APIs, telemetry, analytics, Nimbus/security metadata, licensing, commerce, operations and recovery. The public diagram is intentionally high level; schemas, hosts, credentials and sensitive implementation details remain private.':
        '<p align="center"><sub>High-level public data-platform view. Schemas, hosts, credentials and sensitive topology remain private.</sub></p>',
    'The current focus is stabilization, testing and internal release preparation. Public release only happens after the required validation and release gates are complete.':
        '<p align="center"><sub>Current phase: stabilization and validation. The public release gate remains closed.</sub></p>',
    'The public model separates player-facing experiences from the commerce and entitlement path: website and mobile account/store surfaces, launcher/client consumption, external payment processing, verified orders, Leviathan entitlements, cosmetics ownership, LeviCoins ledger state, referrals and creator/campaign attribution. Payment credentials remain with the payment provider.':
        '<p align="center"><sub>Player experiences and commerce/entitlement flows remain separated, with payment credentials handled by the payment provider.</sub></p>',
}
for old, new in replacements.items():
    text = text.replace(old, new)

for forbidden in [
    'Browse public research lists',
    'The Pacman graph is generated by GitHub Actions and stored in this profile repository.',
    'Generated from public GitHub repositories and public activity only. Private repositories and proprietary source code are excluded.',
]:
    text = text.replace(forbidden, '')

text = re.sub(r'\n{4,}', '\n\n\n', text)
path.write_text(text, encoding="utf-8", newline="\n")
