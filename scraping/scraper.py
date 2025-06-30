import os
import time
import random
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from blacklist import BLACKLISTED


ROOT_URLS = ["https://lifeindenmark.borger.dk", "https://skat.dk/en-us/individuals"]
DOMAINS = [urlparse(url).netloc for url in ROOT_URLS]
visited = set()


def save_html(url: str, html: str):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        path = "index"
    filename = f"{parsed.netloc}_{path.replace('/', '_')}.html"
    save_dir = "documents/html"
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)


def extract_links(url: str, html: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        parsed = urlparse(href)
        if any(parsed.netloc.endswith(domain) for domain in DOMAINS):
            # Build the blacklist key in the same format as BLACKLISTED
            path = parsed.path.strip("/")
            if not path:
                path = "index"
            blacklist_key = f"{parsed.netloc}_{path.replace('/', '_')}.html"
            if blacklist_key not in BLACKLISTED:
                clean_url = parsed.scheme + "://" + parsed.netloc + parsed.path
                links.add(clean_url)
    return links


def html_to_text(url: str, html: str) -> str:
    # apparently this works better than the haystack implementation with the trafilatura library
    soup = BeautifulSoup(html, "html.parser")
    tags_to_remove = [
        "script",
        "style",
        "head",
        "meta",
        "noscript",
        "iframe",
        "footer",
        "nav",
        "form",
        "input",
        "button",
    ]
    for tag in soup(tags_to_remove):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Remove cookie-related lines
    if "lifeindenmark.borger.dk" in url:
        start = None
        end = None
        for i, line in enumerate(lines):
            if start is None and "Accept cookies" in line:
                start = i
            if start is not None and "Cookies and lifeindenmark.dk" in line:
                end = i
                break
        if start is not None and end is not None and end >= start:
            del lines[start : end + 1]
    elif "skat.dk" in url:
        start = None
        end = None
        for i, line in enumerate(lines):
            if start is None and "We use cookies" in line:
                start = i
            if start is not None and "Go to content" in line:
                end = i
                break
        if start is not None and end is not None and end >= start:
            del lines[start : end + 1]

    return "\n".join(lines)


def crawl(page, url: str, root_url: str, delay_range=(1, 3)):
    if url in visited:
        return
    print(f"Crawling: {url}")
    visited.add(url)
    try:
        page.goto(url, timeout=10000)
        # Try to accept cookie banner if it appears
        locator = page.locator("button:has-text('Accept all')")
        if locator.is_visible():
            locator.click(timeout=3000)
        html = page.content()
        save_html(url, html)
        text = html_to_text(url, html)
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if not path:
            path = "index"
        filename = f"{parsed.netloc}_{path.replace('/', '_')}.txt"
        save_dir = "documents/txt"
        os.makedirs(save_dir, exist_ok=True)
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {url.replace('_', '/')}\n\n")
            f.write(text)
        print(f"Saved text content to {filepath}")
        links = extract_links(url, html)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    for link in links:
        if link.startswith(root_url) and link not in visited:
            time.sleep(random.uniform(*delay_range))
            crawl(page, link, root_url, delay_range)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Starting web scraping...")
        start = time.time()

        for root_url in ROOT_URLS:
            root = root_url.split("?")[0]  # Remove query param for root_url match
            crawl(page, root_url, root)

        end = time.time()
        print(f"\nWeb scraping completed in {((end - start) / 60):.0f} minutes.")
        print(f"Total unique links found: {len(visited)}\n")
        browser.close()


if __name__ == "__main__":
    main()
