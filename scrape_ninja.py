import requests
from bs4 import BeautifulSoup

urls = [
    "https://sekol.ninja/articles/",
    "https://sekol.ninja/about-me/",
]
headers = {
    "Accept-Encoding": "identity",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
}

for url in urls:
    print(f"\n{'=' * 60}\nPAGE: {url}")
    try:
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        print(f"Could not load {url}: {error}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    print("TITLE:", soup.title.get_text(strip=True) if soup.title else "Not found")
    print("H1:", soup.h1.get_text(strip=True) if soup.h1 else "Not found")

    h2_tags = soup.find_all("h2")
    print("H2 tags found:", len(h2_tags))
    print("\nSECTION HEADINGS:")
    for h2 in h2_tags:
        print(" -", h2.get_text(strip=True))

    print("\nARTICLE TITLES:")
    for title in soup.select("h2.entry-title"):
        print(" -", title.get_text(strip=True))

    print("\nLINKS:")
    seen = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if "sekol.ninja" in href and href not in seen:
            seen.add(href)
            print(" -", anchor.get_text(strip=True), "->", href)