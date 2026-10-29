import requests

sites = [
    "https://sekol.ninja",
    "https://www.mahoningctc.com",
    "https://www.python.org",
    "https://httpbin.org/status/404",
    "https://this-site-is-fake-xyz123.com",
    "https://www.github.com",
    "https://www.facebook.com",
]

for url in sites:
    try:
        response = requests.get(url, timeout=5)
        status = "UP" if response.ok else "DOWN"
        elapsed = response.elapsed.total_seconds()
        print(f"[{status}] {url} -> {response.status_code} ({elapsed:.2f}s)")
    except requests.exceptions.RequestException:
        print(f"[DOWN] {url} -> could not connect")
