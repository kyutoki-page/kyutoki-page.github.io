#!/usr/bin/env python3
"""Download the published Wix pages listed in the public sitemap."""

import argparse
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


SITE_HOST = "elemake2026.wixsite.com"
SITEMAP_INDEX = f"https://{SITE_HOST}/page/sitemap.xml"
ASSET_DOMAINS = "elemake2026.wixsite.com,wixstatic.com,parastorage.com"
REPO_ROOT = Path(__file__).resolve().parents[1]


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


def fetch_xml(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; static-site-sync/1.0)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return ET.fromstring(response.read())


def public_page_urls():
    sitemap_queue = [SITEMAP_INDEX]
    visited_sitemaps = set()
    page_urls = set()

    while sitemap_queue:
        sitemap_url = sitemap_queue.pop()
        if sitemap_url in visited_sitemaps:
            continue
        visited_sitemaps.add(sitemap_url)
        root = fetch_xml(sitemap_url)
        root_type = local_name(root.tag)

        if root_type == "sitemapindex":
            for entry in root:
                if local_name(entry.tag) != "sitemap":
                    continue
                loc = next((child.text for child in entry if local_name(child.tag) == "loc"), None)
                if loc:
                    sitemap_queue.append(loc)
        elif root_type == "urlset":
            for entry in root:
                if local_name(entry.tag) != "url":
                    continue
                loc = next((child.text for child in entry if local_name(child.tag) == "loc"), None)
                if not loc:
                    continue
                parsed = urlparse(loc)
                if parsed.scheme == "https" and parsed.hostname == SITE_HOST and parsed.path.startswith("/page"):
                    page_urls.add(loc)

    return sorted(page_urls)


def sync_pages(output_dir, page_urls):
    output_dir.mkdir(parents=True, exist_ok=True)
    if any(output_dir.iterdir()):
        raise RuntimeError(f"Output directory is not empty: {output_dir}")

    index_file = REPO_ROOT / "site-copy" / "index.html"
    (output_dir / "index.html").write_bytes(index_file.read_bytes())

    command = [
        "wget",
        "--page-requisites",
        "--convert-links",
        "--adjust-extension",
        "--span-hosts",
        f"--domains={ASSET_DOMAINS}",
        f"--directory-prefix={output_dir}",
        "-nv",
        *page_urls,
    ]
    subprocess.run(command, check=True)

    badge = re.compile(r'<div id="WIX_ADS"[^>]*>.*?</a></div>', re.DOTALL)
    for html_file in output_dir.rglob("*.html"):
        contents = html_file.read_text(encoding="utf-8")
        html_file.write_text(badge.sub("", contents), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--list-only", action="store_true")
    args = parser.parse_args()

    page_urls = public_page_urls()
    if not page_urls:
        raise RuntimeError("The public Wix sitemap contained no eligible pages")

    if args.list_only:
        print("\n".join(page_urls))
        print(f"Found {len(page_urls)} public pages")
        return

    if args.output_dir is None:
        parser.error("--output-dir is required unless --list-only is used")
    sync_pages(args.output_dir.resolve(), page_urls)


if __name__ == "__main__":
    main()