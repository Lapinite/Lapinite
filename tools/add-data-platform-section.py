from pathlib import Path

path = Path("README.md")
text = path.read_text(encoding="utf-8")

section = '''## Leviathan Data Platform

<p align="center">
  <img width="100%" src="assets/profile/data-platform-v2.svg" alt="Animated high-level Leviathan data platform architecture">
</p>

The data layer is designed as a shared platform capability for accounts, launcher/client state, APIs, telemetry, analytics, Nimbus/security metadata, licensing, commerce, operations and recovery. The public diagram is intentionally high level; schemas, hosts, credentials and sensitive implementation details remain private.

'''

if "## Leviathan Data Platform" not in text:
    marker = "## Development Roadmap\n"
    if marker not in text:
        raise SystemExit("Development Roadmap heading not found")
    text = text.replace(marker, section + marker, 1)

path.write_text(text, encoding="utf-8", newline="\n")
