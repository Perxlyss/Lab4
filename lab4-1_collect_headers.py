#!/usr/bin/env python3
# lab4-1_collect_headers.py
import requests, json, sys

def collect(urls, out_file="headers.json"):
    results = []
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            results.append({
                "url": url,
                "status": r.status_code,
                "final_url": r.url,
                "server": r.headers.get("Server"),
                "content_type": r.headers.get("Content-Type"),
                "content_length": r.headers.get("Content-Length")
            })
        except requests.exceptions.RequestException as e:
            results.append({"url": url, "error": str(e)})
    with open(out_file, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Wrote {len(results)} entries to {out_file}")

if __name__ == '__main__':
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python lab1_collect_headers.py <url1> <url2> ...")
        sys.exit(1)
    collect(urls)