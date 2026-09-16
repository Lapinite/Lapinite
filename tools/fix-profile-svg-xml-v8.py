from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path("assets")
P = ROOT / "profile"

# v7 roadmap labels contain literal ampersands in XML text nodes. GitHub's SVG
# renderer rejects malformed XML, so repair those labels after the visual pass.
REPLACEMENTS = {
    "SECURITY & INTEGRITY": "SECURITY &amp; INTEGRITY",
    "TEST & VALIDATE": "TEST &amp; VALIDATE",
    "OPERATE & OBSERVE": "OPERATE &amp; OBSERVE",
    "RELEASE & IMPROVE": "RELEASE &amp; IMPROVE",
}

roadmap = P / "roadmap-v2.svg"
text = roadmap.read_text(encoding="utf-8")
for old, new in REPLACEMENTS.items():
    text = text.replace(old, new)
roadmap.write_text(text, encoding="utf-8", newline="\n")

# Validate every profile SVG currently referenced by the README, plus the hero
# surfaces. This catches malformed XML before GitHub tries to render it.
readme = Path("README.md").read_text(encoding="utf-8")
paths = [ROOT / "hero-dark-v4.svg", ROOT / "hero-light-v4.svg"]
paths += sorted(P.glob("*.svg"))

errors = []
for path in paths:
    if str(path).replace("\\", "/") not in readme and path.name not in {"hero-dark-v4.svg", "hero-light-v4.svg"}:
        continue
    try:
        ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"{path}: {exc}")

if errors:
    raise SystemExit("Invalid SVG XML:\n" + "\n".join(errors))

print("Profile SVG XML validation passed")
