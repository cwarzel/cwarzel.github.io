#!/usr/bin/env python3
"""
Fetches reviews from Letterboxd RSS feed and updates _data/log.yml.
Run this periodically to keep the Log page up to date.

Usage: python3 update_letterboxd.py
"""

import requests
import xml.etree.ElementTree as ET
import yaml
import re
from pathlib import Path

FEED_URL = "https://letterboxd.com/cwarzel/rss/"
LOG_PATH = Path("_data/log.yml")
MAX_ITEMS = 20


def fetch_feed(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def parse_reviews(feed_xml: str):
    """Parse Letterboxd RSS feed and extract reviews."""
    root = ET.fromstring(feed_xml)
    channel = root.find("channel")
    if channel is None:
        return []

    reviews = []
    for item in channel.findall("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        description_el = item.find("description")

        # Letterboxd namespace for ratings
        rating_el = item.find("{https://letterboxd.com}memberRating")
        film_year_el = item.find("{https://letterboxd.com}filmYear")
        watched_el = item.find("{https://letterboxd.com}watchedDate")

        if title_el is None or title_el.text is None:
            continue

        full_title = title_el.text.strip()

        # Parse title - format is usually "Film Name, Year - ★★★★"
        # Extract just the film name
        film_title = full_title.split(",")[0].strip()

        # Get year
        year = ""
        if film_year_el is not None and film_year_el.text:
            year = film_year_el.text.strip()

        # Get rating as stars
        rating = ""
        if rating_el is not None and rating_el.text:
            try:
                rating_num = float(rating_el.text)
                full_stars = int(rating_num)
                half_star = rating_num - full_stars >= 0.5
                rating = "★" * full_stars + ("½" if half_star else "")
            except:
                pass

        # Get review snippet from description
        note = ""
        if description_el is not None and description_el.text:
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', '', description_el.text)
            # Clean up whitespace
            text = ' '.join(text.split())
            # Truncate if too long
            if len(text) > 150:
                text = text[:147] + "..."
            note = text

        link = link_el.text.strip() if link_el is not None and link_el.text else ""

        reviews.append({
            "title": film_title,
            "year": year,
            "rating": rating,
            "note": note,
            "link": link
        })

    return reviews[:MAX_ITEMS]


def update_log(reviews):
    """Update the watching section in _data/log.yml"""
    if not LOG_PATH.exists():
        raise SystemExit(f"log.yml not found at {LOG_PATH.resolve()}")

    # Read existing log
    with open(LOG_PATH, 'r') as f:
        log_data = yaml.safe_load(f) or {}

    # Update watching section
    watching = []
    for r in reviews:
        entry = {"title": r["title"]}
        if r["year"]:
            entry["year"] = r["year"]
        if r["rating"]:
            entry["rating"] = r["rating"]
        if r["note"]:
            entry["note"] = r["note"]
        watching.append(entry)

    log_data["watching"] = watching

    # Write back
    with open(LOG_PATH, 'w') as f:
        yaml.dump(log_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Updated {len(watching)} films in log.yml")


def main():
    print("Fetching Letterboxd feed...")
    xml_text = fetch_feed(FEED_URL)

    print("Parsing reviews...")
    reviews = parse_reviews(xml_text)

    if not reviews:
        print("No reviews found.")
        return

    print(f"Found {len(reviews)} reviews")
    update_log(reviews)
    print("Done! Now commit and push the changes.")


if __name__ == "__main__":
    main()
