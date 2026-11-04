#!/usr/bin/env python3
"""Generate a Dracula-colored SVG language treemap from public GitHub repositories."""
import collections
import html
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

USER = "Metal-Bat"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "profile-treemap"}
if os.getenv("GITHUB_TOKEN"):
    HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

def get(url):
    with urlopen(Request(url, headers=HEADERS), timeout=30) as response:
        return json.load(response)

repos = []
for page in range(1, 11):
    batch = get(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner")
    repos.extend(r for r in batch if not r.get("fork") and not r.get("archived"))
    if len(batch) < 100:
        break
counts = collections.Counter()
for repo in repos:
    try:
        counts.update(get(repo["languages_url"]))
    except Exception as exc:
        print("Skipping", repo["name"], str(exc))
counts = dict(counts.most_common(12))
width, height = 900, 340
colors = ["#bd93f9", "#ff79c6", "#8be9fd", "#50fa7b", "#ffb86c", "#f1fa8c", "#ff5555", "#6272a4"]
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Language treemap">', f'<rect width="{width}" height="{height}" rx="14" fill="#282a36"/>']
if not counts:
    parts.append('<text x="30" y="50" fill="#f8f8f2" font-size="22">No public repository language data</text>')
else:
    total = sum(counts.values())
    x = 0
    for index, (name, size) in enumerate(counts.items()):
        segment = width * size / total
        if index == len(counts) - 1:
            segment = width - x
        parts.append(f'<rect x="{x:.2f}" y="0" width="{segment:.2f}" height="{height}" fill="{colors[index % len(colors)]}" stroke="#282a36" stroke-width="3"/>')
        if segment > 65:
            font_size = min(20, max(11, segment / 8))
            parts.append(f'<text x="{x + segment / 2:.2f}" y="{height / 2:.0f}" font-family="sans-serif" font-weight="bold" font-size="{font_size:.0f}" text-anchor="middle" fill="#282a36">{html.escape(name)}</text>')
        x += segment
parts.append("</svg>")
out = Path("assets/language-treemap.svg")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(parts), encoding="utf-8")
