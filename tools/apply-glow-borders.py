from __future__ import annotations

import re
from pathlib import Path

TARGETS = [
    Path("assets/hero-dark.svg"),
    Path("assets/hero-light.svg"),
    Path("assets/profile/command-core.svg"),
    Path("assets/profile/neural-core.svg"),
    Path("assets/profile/external-services.svg"),
    Path("assets/profile/data-platform.svg"),
    Path("assets/profile/ecosystem-overview.svg"),
    Path("assets/profile/experience-commerce.svg"),
    Path("assets/profile/roadmap.svg"),
    Path("assets/profile/contributions.svg"),
    Path("assets/profile/activity-feed.svg"),
    Path("assets/profile/repository-health.svg"),
    Path("assets/profile/analytics-overview.svg"),
    Path("assets/profile/pacman.svg"),
    Path("assets/profile/core-products.svg"),
    Path("assets/profile/tech-stack.svg"),
    Path("assets/profile/platform-areas.svg"),
    Path("assets/profile/developer-network.svg"),
]

MARKER = "LEVIATHAN_GLOW_BORDER_V1"


def dimensions(svg: str) -> tuple[float, float]:
    match = re.search(r'viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', svg)
    if match:
        return float(match.group(1)), float(match.group(2))
    width = re.search(r'width="([\d.]+)', svg)
    height = re.search(r'height="([\d.]+)', svg)
    if not width or not height:
        raise ValueError("SVG dimensions not found")
    return float(width.group(1)), float(height.group(1))


def border_markup(width: float, height: float, hero: bool) -> str:
    inset = 4
    radius = 26 if hero else 22
    dash = max(260, int((width + height) * 0.26))
    gap = max(900, int((width + height) * 0.95))
    duration = "8s" if hero else "10s"
    return f'''\n<!-- {MARKER} -->
<defs>
  <linearGradient id="leviathanBorderGradient" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#067dff"/>
    <stop offset="0.34" stop-color="#32efff"/>
    <stop offset="0.62" stop-color="#11bddf"/>
    <stop offset="1" stop-color="#4a65ff"/>
  </linearGradient>
  <filter id="leviathanBorderGlow" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
    <feGaussianBlur stdDeviation="5" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect x="{inset}" y="{inset}" width="{width - inset*2:g}" height="{height - inset*2:g}" rx="{radius}" fill="none" stroke="#0b3346" stroke-width="1.5" opacity="0.9"/>
<rect x="{inset}" y="{inset}" width="{width - inset*2:g}" height="{height - inset*2:g}" rx="{radius}" fill="none" stroke="url(#leviathanBorderGradient)" stroke-width="3" stroke-linecap="round" stroke-dasharray="{dash} {gap}" filter="url(#leviathanBorderGlow)" opacity="0.92">
  <animate attributeName="stroke-dashoffset" values="0;-{dash + gap}" dur="{duration}" repeatCount="indefinite"/>
</rect>
<rect x="12" y="12" width="{width - 24:g}" height="{height - 24:g}" rx="{max(12, radius-8)}" fill="none" stroke="#27dff5" stroke-width="0.7" stroke-dasharray="2 12" opacity="0.2">
  <animate attributeName="stroke-dashoffset" values="0;28" dur="5s" repeatCount="indefinite"/>
</rect>'''


def apply(path: Path) -> None:
    if not path.exists():
        print(f"skip missing {path}")
        return
    svg = path.read_text(encoding="utf-8")
    if MARKER in svg:
        return
    width, height = dimensions(svg)
    hero = path.name.startswith("hero-")
    markup = border_markup(width, height, hero)
    index = svg.rfind("</svg>")
    if index < 0:
        raise ValueError(f"No closing svg tag in {path}")
    svg = svg[:index] + markup + "\n" + svg[index:]
    path.write_text(svg, encoding="utf-8", newline="\n")
    print(f"bordered {path}")


def main() -> None:
    for target in TARGETS:
        apply(target)


if __name__ == "__main__":
    main()
