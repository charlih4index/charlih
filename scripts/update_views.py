#!/usr/bin/env python3
"""Update YouTube view counts in K/KTV.md and Y/Youtube.md (run daily via GitHub Actions)."""
import json
import os
import re
import sys
import urllib.request

MD_PATH = "K/KTV.md"
YOUTUBE_MD_PATH = "Y/Youtube.md"
API_URL = "https://www.googleapis.com/youtube/v3/videos"

# Video ids appear as youtu.be/<id>, youtube.com/shorts/<id> or
# youtube.com/watch?v=<id> (the www. prefix is optional in the match).
VIDEO_ID_RE = re.compile(r"(?:youtu\.be/|youtube\.com/(?:shorts/|watch\?v=))([\w-]{11})")


def fetch_views(ids, key):
    """Fetch {video_id: viewCount} for ids, 50 per API call."""
    views = {}
    for i in range(0, len(ids), 50):
        chunk = ",".join(ids[i : i + 50])
        url = f"{API_URL}?part=statistics&id={chunk}&key={key}"
        with urllib.request.urlopen(url) as r:
            data = json.load(r)
        if "error" in data:
            sys.exit(f"API error: {data['error'].get('message')}")
        for item in data.get("items", []):
            views[item["id"]] = item["statistics"]["viewCount"]
    return views


def update_top5(md, views):
    """Update the Viewed column of the Top 5 table in Y/Youtube.md.

    Only table rows with a numeric No and a numeric Viewed cell are touched.
    The video id is read from the Video column only, so a youtu.be link in
    the Promote MV column can never be mistaken for the row's video.
    Rows whose title contains '|' (extra columns) are left alone.
    Returns (new_text, rows_changed).
    """
    out, changed = [], 0
    for line in md.splitlines(keepends=True):
        cols = line.rstrip("\n").split("|")
        # Top 5 rows split into 8 parts:
        # ['', ' 1 ', cover, ' [title](url) ', ' date ', ' 94 ', promote, '']
        if len(cols) == 8 and cols[1].strip().isdigit() and cols[5].strip().isdigit():
            m = VIDEO_ID_RE.search(cols[3])
            if m and m.group(1) in views:
                cols[5] = f" {views[m.group(1)]} "
                changed += 1
                line = "|".join(cols) + ("\n" if line.endswith("\n") else "")
        out.append(line)
    return "".join(out), changed


def main():
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("error: YOUTUBE_API_KEY is not set")
    # K/KTV.md: Viewed is the last column (existing behavior, unchanged).
    md = open(MD_PATH, encoding="utf-8").read()
    ids = sorted(set(re.findall(r"https://youtu\.be/([\w-]{11})", md)))
    print(f"found {len(ids)} video ids")
    views = fetch_views(ids, key)
    print(f"got counts for {len(views)} videos")
    changed = 0
    out = []
    for line in md.splitlines(keepends=True):
        m = re.search(r"https://youtu\.be/([\w-]{11})", line)
        if m and m.group(1) in views:
            body = line.rstrip("\n")
            new_body, n = re.subn(r"\| (\d+) \|$", f"| {views[m.group(1)]} |", body)
            if n:
                changed += 1
                line = new_body + ("\n" if line.endswith("\n") else "")
        out.append(line)
    open(MD_PATH, "w", encoding="utf-8").write("".join(out))
    print(f"updated {changed} rows in {MD_PATH}")
    # Y/Youtube.md: Viewed is the 5th column of the Top 5 table.
    md = open(YOUTUBE_MD_PATH, encoding="utf-8").read()
    ids = sorted(set(VIDEO_ID_RE.findall(md)))
    print(f"found {len(ids)} video ids in {YOUTUBE_MD_PATH}")
    views = fetch_views(ids, key)
    print(f"got counts for {len(views)} videos")
    md, changed = update_top5(md, views)
    open(YOUTUBE_MD_PATH, "w", encoding="utf-8").write(md)
    print(f"updated {changed} rows in {YOUTUBE_MD_PATH}")


if __name__ == "__main__":
    main()
