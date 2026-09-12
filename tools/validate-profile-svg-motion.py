from __future__ import annotations

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

ROOTS = [Path("assets"), Path("assets/profile")]


def iter_svgs() -> list[Path]:
    seen: set[Path] = set()
    files: list[Path] = []
    for root in ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.svg"):
            if path in seen:
                continue
            seen.add(path)
            files.append(path)
    return sorted(files)


def href_of(node: ET.Element) -> str | None:
    return node.get("href") or node.get(f"{{{XLINK_NS}}}href")


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    checked = 0

    for path in iter_svgs():
        checked += 1
        try:
            root = ET.parse(path).getroot()
        except Exception as exc:
            failures.append(f"{path}: invalid XML: {exc}")
            continue

        ids: dict[str, ET.Element] = {}
        for node in root.iter():
            node_id = node.get("id")
            if node_id:
                ids[node_id] = node

        for motion in root.iter(f"{{{SVG_NS}}}animateMotion"):
            direct_path = motion.get("path")
            mpaths = list(motion.findall(f"{{{SVG_NS}}}mpath"))

            if direct_path and mpaths:
                failures.append(f"{path}: animateMotion mixes path= with mpath")

            if direct_path:
                # A direct path has no separately visible geometry to drift from. It is allowed,
                # but new HUD assets should prefer a shared path + mpath whenever a line is shown.
                if len(re.findall(r"(?<![A-Za-z])[Mm](?=[\s\d.-])", direct_path)) > 1:
                    failures.append(f"{path}: animateMotion path contains multiple move segments and may jump")
                warnings.append(f"{path}: direct animateMotion path; prefer shared path id + mpath for visible routes")

            for mpath in mpaths:
                href = href_of(mpath)
                if not href or not href.startswith("#"):
                    failures.append(f"{path}: mpath missing local #id href")
                    continue
                target_id = href[1:]
                target = ids.get(target_id)
                if target is None:
                    failures.append(f"{path}: mpath references missing #{target_id}")
                    continue
                if target.tag != f"{{{SVG_NS}}}path":
                    failures.append(f"{path}: mpath #{target_id} does not reference a path element")
                    continue
                d = target.get("d", "")
                if not d.strip():
                    failures.append(f"{path}: motion path #{target_id} has empty d")
                if len(re.findall(r"(?<![A-Za-z])[Mm](?=[\s\d.-])", d)) > 1:
                    failures.append(f"{path}: motion path #{target_id} contains multiple move segments and may jump")

        # Catch duplicate ids because they can make mpath target resolution unpredictable.
        source = path.read_text(encoding="utf-8")
        raw_ids = re.findall(r'\bid=["\']([^"\']+)["\']', source)
        duplicates = sorted({item for item in raw_ids if raw_ids.count(item) > 1})
        for item in duplicates:
            failures.append(f"{path}: duplicate id #{item}")

    print(f"Checked {checked} SVG files.")
    for warning in warnings:
        print(f"WARN: {warning}")
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print("SVG motion validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
