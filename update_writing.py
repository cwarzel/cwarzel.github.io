#!/usr/bin/env python3
"""
Fetches articles from The Atlantic RSS feed and updates writing.html.
Run this periodically to keep the Writing page up to date.

Usage: python update_writing.py
"""

import requests
import datetime
import html
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://www.theatlantic.com/feed/author/charlie-warzel/"
WRITING_PATH = Path("writing.html")
MAX_ITEMS = 50


def fetch_feed(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_items(feed_xml: str):
    """
    Return a list of dicts: {title, link, date}
    Supports both RSS and Atom feeds.
    """
    root = ET.fromstring(feed_xml)
    items = []

    # Try RSS first
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_el = item.find("pubDate")

            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            link = link_el.text.strip() if link_el is not None and link_el.text else ""
            pub_raw = pub_el.text.strip() if pub_el is not None and pub_el.text else ""

            date_str = ""
            if pub_raw:
                try:
                    dt = datetime.datetime.strptime(pub_raw, "%a, %d %b %Y %H:%M:%S %z")
                    date_str = dt.strftime("%B %-d, %Y")
                except Exception:
                    date_str = ""

            if title and link:
                items.append({"title": title, "link": link, "date": date_str})

        if items:
            return items

    # Try Atom
    for entry in root.findall(".//{*}entry"):
        title_el = entry.find("{*}title")
        link_el = entry.find("{*}link")
        date_el = entry.find("{*}updated") or entry.find("{*}published")

        title = title_el.text.strip() if title_el is not None and title_el.text else ""
        link = link_el.attrib.get("href", "").strip() if link_el is not None else ""

        date_str = ""
        if date_el is not None and date_el.text:
            raw = date_el.text.strip()
            try:
                if raw.endswith("Z"):
                    raw = raw.replace("Z", "+00:00")
                dt = datetime.datetime.fromisoformat(raw)
                date_str = dt.strftime("%B %-d, %Y")
            except Exception:
                date_str = ""

        if title and link:
            items.append({"title": title, "link": link, "date": date_str})

    return items


def build_list_html(items):
    parts = []
    for item in items[:MAX_ITEMS]:
        title = html.escape(item["title"])
        link = html.escape(item["link"])
        date = item["date"] or ""

        if date:
            li = f'  <li>\n    <a href="{link}">{title}</a>\n    <time>{date}</time>\n  </li>'
        else:
            li = f'  <li>\n    <a href="{link}">{title}</a>\n  </li>'
        parts.append(li)

    return "\n".join(parts)


def update_writing():
    if not WRITING_PATH.exists():
        raise SystemExit(f"writing.html not found at {WRITING_PATH.resolve()}")

    print("Fetching feed...")
    xml_text = fetch_feed(FEED_URL)
    items = parse_items(xml_text)

    if not items:
        raise SystemExit("No items found in feed; not updating writing.html.")

    print(f"Found {len(items)} articles")
    list_html = build_list_html(items)

    print("Reading writing.html...")
    original = WRITING_PATH.read_text(encoding="utf-8")

    # Find the article list and replace its contents
    marker_start = '<ul class="post-list" id="article-list">'
    marker_end = '</ul>'

    if marker_start in original:
        before, _, rest = original.partition(marker_start)
        _, _, after = rest.partition(marker_end)
        new_content = before + marker_start + "\n" + list_html + "\n" + marker_end + after
    else:
        raise SystemExit("Could not find article-list marker in writing.html")

    print("Writing updated writing.html...")
    WRITING_PATH.write_text(new_content, encoding="utf-8")
    print(f"Done! Updated with {min(len(items), MAX_ITEMS)} articles.")


if __name__ == "__main__":
    update_writing()
