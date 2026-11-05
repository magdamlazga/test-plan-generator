"""
Small helpers that download a web page and pull out what a tester needs:
its links, its visible text, and its forms with their input fields.
"""

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
TIMEOUT = 15        # seconds to wait for a page
TEXT_LIMIT = 2_000  # characters of page text to keep per page

SKIP_LINK_PREFIXES = ("#", "mailto:", "tel:", "javascript:")


def load_page(url):
    """Download a page and return it parsed, ready to search."""
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def get_links(url):
    """Return the unique links on a page, without anchors, email or phone links."""
    page = load_page(url)
    links = {a.get("href") for a in page.find_all("a")}
    return sorted(link for link in links if link and not link.startswith(SKIP_LINK_PREFIXES))


def get_page_text(page):
    """Return the page title and visible text, without scripts, styles or images."""
    title = page.title.string.strip() if page.title and page.title.string else "No title"
    if not page.body:
        return title
    for tag in page.body(["script", "style", "img", "svg"]):
        tag.decompose()
    text = page.body.get_text(separator="\n", strip=True)
    return (title + "\n\n" + text)[:TEXT_LIMIT]


def get_forms(page):
    """Describe every form on the page: its fields, their types and which are required."""
    lines = []
    for i, form in enumerate(page.find_all("form"), 1):
        lines.append(f"Form {i} (action={form.get('action', '')}, method={form.get('method', 'get')})")
        for field in form.find_all(["input", "select", "textarea", "button"]):
            if field.get("type") == "hidden":
                continue  # CSRF tokens and similar - not useful for test design
            name = field.get("name") or field.get("id") or field.get_text(strip=True)
            lines.append(
                f"  - {field.name} type={field.get('type', field.name)} name={name}"
                f" required={field.has_attr('required')} placeholder={field.get('placeholder', '')}"
            )
    return "\n".join(lines) or "No forms on this page."


def read_page_for_testing(url):
    """Return a page's text and its forms as one block of text for the LLM.
    Forms are read first, because get_page_text removes parts of the page."""
    page = load_page(url)
    forms = get_forms(page)
    return "### Page text\n" + get_page_text(page) + "\n### Forms\n" + forms + "\n"
