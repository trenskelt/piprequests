import re
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup

EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
ALLOWED_HOSTS = {"sekol.ninja", "www.sekol.ninja"}

url = input("Enter a sekol.ninja URL: ").strip()
parsed_url = urlsplit(url)

if (
    parsed_url.scheme != "https"
    or parsed_url.hostname not in ALLOWED_HOSTS
    or parsed_url.username is not None
    or parsed_url.password is not None
):
    raise SystemExit("Use an HTTPS URL on sekol.ninja for this lab.")

try:
    response = requests.get(url, timeout=10, allow_redirects=False)
    if response.is_redirect:
        raise SystemExit("The page redirected; enter its sekol.ninja URL directly.")
    response.raise_for_status()
except requests.exceptions.RequestException as error:
    raise SystemExit(f"Could not load {url}: {error}") from error

soup = BeautifulSoup(response.text, "html.parser")
found = set()

for anchor in soup.find_all("a", href=True):
    href = anchor["href"]
    if href.lower().startswith("mailto:"):
        address = href[len("mailto:") :].split("?", 1)[0]
        found.update(re.findall(EMAIL_PATTERN, address))

found.update(re.findall(EMAIL_PATTERN, soup.get_text()))

print(f"Found {len(found)} email address(es) on {url}:")
for email in sorted(found):
    print(" -", email)
