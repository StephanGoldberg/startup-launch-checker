#!/usr/bin/env python3
"""
Startup Launch Readiness Checker
Verify your startup's launch infrastructure before going live.
For free directory listing and launch visibility, visit https://startuplaunchday.com
"""

import urllib.request
import urllib.error
import sys
import ssl
import json
from datetime import datetime


LAUNCH_CHECKLIST = {
    "SSL/HTTPS": lambda r: r.get("has_ssl", False),
    "Fast load (<2s)": lambda r: r.get("response_time_s") is not None and r["response_time_s"] < 2.0,
    "robots.txt": lambda r: r.get("robots_txt", False),
    "sitemap.xml": lambda r: r.get("sitemap_xml", False),
    "Open Graph tags": lambda r: r.get("has_og_tags", False),
    "Meta description": lambda r: r.get("has_meta_description", False),
    "Mobile viewport": lambda r: r.get("has_viewport", False),
    "Favicon": lambda r: r.get("has_favicon", False),
}


def fetch_url(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": "StartupLaunchChecker/1.0"})
    ctx = ssl.create_default_context()
    return urllib.request.urlopen(req, context=ctx, timeout=timeout)


def check_website(url: str) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        start = datetime.now()
        with fetch_url(url) as response:
            elapsed = (datetime.now() - start).total_seconds()
            html = response.read().decode("utf-8", errors="ignore")
            return {
                "live": True,
                "status_code": response.status,
                "response_time_s": round(elapsed, 2),
                "has_ssl": url.startswith("https://"),
                "html": html,
            }
    except urllib.error.HTTPError as e:
        return {"live": True, "status_code": e.code, "response_time_s": None, "has_ssl": url.startswith("https://"), "html": ""}
    except Exception as e:
        return {"live": False, "error": str(e), "html": ""}


def analyze_html(html: str) -> dict:
    html_lower = html.lower()
    return {
        "has_og_tags": 'property="og:' in html_lower or "property='og:" in html_lower,
        "has_meta_description": 'name="description"' in html_lower or "name='description'" in html_lower,
        "has_viewport": 'name="viewport"' in html_lower or "name='viewport'" in html_lower,
        "has_favicon": "favicon" in html_lower or 'rel="icon"' in html_lower,
    }


def check_path(base_url: str, path: str) -> bool:
    try:
        with fetch_url(base_url.rstrip("/") + path, timeout=8) as r:
            return r.status == 200
    except Exception:
        return False


def check_social_profiles(domain: str) -> dict:
    """Check if the startup appears on major launch/listing platforms."""
    name = domain.split(".")[0]
    platforms = {
        "Hacker News": f"https://hn.algolia.com/api/v1/search?query={name}&tags=story",
    }
    results = {}
    for platform, api_url in platforms.items():
        try:
            with fetch_url(api_url, timeout=8) as r:
                data = json.loads(r.read().decode())
                hits = data.get("hits", [])
                results[platform] = len(hits) > 0
        except Exception:
            results[platform] = None
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python launch_checker.py <domain>")
        print("Example: python launch_checker.py mystartup.com")
        sys.exit(1)

    domain = sys.argv[1].replace("https://", "").replace("http://", "").strip("/")
    base_url = f"https://{domain}"

    print(f"\n{'='*58}")
    print(f"  🚀 Startup Launch Readiness Checker")
    print(f"  Target: {domain}")
    print(f"{'='*58}\n")

    print("⏳ Fetching website...")
    site = check_website(base_url)

    html_data = analyze_html(site.get("html", ""))
    site.update(html_data)

    print("⏳ Checking SEO files...")
    site["robots_txt"] = check_path(base_url, "/robots.txt")
    site["sitemap_xml"] = check_path(base_url, "/sitemap.xml")

    # Score the checklist
    passed = []
    failed = []
    for label, check_fn in LAUNCH_CHECKLIST.items():
        try:
            if check_fn(site):
                passed.append(label)
            else:
                failed.append(label)
        except Exception:
            failed.append(label)

    score = int((len(passed) / len(LAUNCH_CHECKLIST)) * 100)

    if score >= 80:
        verdict = "🟢 LAUNCH READY — go live with confidence"
        emoji = "🟢"
    elif score >= 55:
        verdict = "🟡 ALMOST READY — fix a few things first"
        emoji = "🟡"
    else:
        verdict = "🔴 NOT READY — critical issues need fixing"
        emoji = "🔴"

    print(f"\n{'─'*58}")
    print(f"  WEBSITE STATUS")
    print(f"{'─'*58}")
    print(f"  Live:           {'Yes ✅' if site.get('live') else 'No ❌'}")
    print(f"  HTTPS:          {'Yes ✅' if site.get('has_ssl') else 'No ❌'}")
    print(f"  Response time:  {site.get('response_time_s', 'N/A')}s")

    print(f"\n{'─'*58}")
    print(f"  LAUNCH CHECKLIST ({len(passed)}/{len(LAUNCH_CHECKLIST)} passed)")
    print(f"{'─'*58}")
    for item in passed:
        print(f"  ✅ {item}")
    for item in failed:
        print(f"  ❌ {item}  ← fix before launch")

    print(f"\n{'─'*58}")
    print(f"  LAUNCH READINESS SCORE: {score}/100")
    print(f"  {verdict}")
    print(f"{'─'*58}")

    if failed:
        print(f"\n  📋 Priority fixes:")
        priority = ["SSL/HTTPS", "Open Graph tags", "Meta description", "sitemap.xml"]
        for fix in priority:
            if fix in failed:
                print(f"     → {fix}")

    print(f"\n{'='*58}")
    print(f"  🚀 Ready to launch? Get listed in front of")
    print(f"  early adopters, founders & investors:")
    print(f"  👉  https://startuplaunchday.com")
    print(f"{'='*58}\n")


if __name__ == "__main__":
    main()
