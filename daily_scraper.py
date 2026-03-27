#!/usr/bin/env python3
"""
Daily Vacation Price Scraper
Runs at 9:15 AM CET via cron. Scrapes Airbnb and Booking.com search pages,
extracts real property links + prices, and writes tracker_data.js so that
vacation_tracker.html shows live data without any manual work.
"""

import hashlib
import json
import re
import time
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# ── Configuration ────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = BASE_DIR / "config.json"
DATA_FILE   = BASE_DIR / "tracker_data.js"
LOG_FILE    = BASE_DIR / "scraper.log"

def generate_urls(config: Dict[str, Any]) -> List[Dict]:
    airbnb_base = "https://www.airbnb.com/s/{}/homes?checkin={}&checkout={}&adults={}&children={}&search_type=filter_change&currency=EUR&display_currency=EUR&price_filter_input_type=0&display_total_price=true"
    booking_base = "https://www.booking.com/searchresults.html?ss={}&checkin={}&checkout={}&group_adults={}&group_children={}&no_rooms=1&selected_currency=EUR&show_fullcard_price=1"
    
    locations = [
        "Vourvourou, Chalkidiki", "Sithonia, Chalkidiki", 
        "Kassandra, Chalkidiki", "Parga, Ionian", 
        "Sivota, Ionian", "Lefkada, Ionian"
    ]
    urls = []
    
    # Build AirBnB query params
    a_params = ""
    if config.get("bedrooms"): a_params += f"&min_bedrooms={config['bedrooms']}"
    if config.get("ac"): a_params += "&amenities%5B%5D=5"
    if config.get("kitchen"): a_params += "&amenities%5B%5D=8"
    if config.get("parking"): a_params += "&amenities%5B%5D=9"
    if config.get("beachfront"): a_params += "&amenities%5B%5D=122"
    
    # Build Booking query params
    b_nflt = []
    if config.get("ac"): b_nflt.append("roomfacility=11")
    if config.get("kitchen"): b_nflt.append("roomfacility=17")
    if config.get("parking"): b_nflt.append("facility=2")
    if config.get("beachfront"): b_nflt.append("hotelfacility=314")
    
    b_params = ""
    if b_nflt:
        joined = ";".join([x.replace("=", "%3D") for x in b_nflt])
        b_params = f"&nflt={joined}"
        
    checkin = config.get("checkin", "2026-06-25")
    checkout = config.get("checkout", "2026-07-05")
    adults = config.get("adults", 2)
    children = config.get("children", 2)
        
    for loc in locations:
        a_loc = loc.replace(" ", "%20").replace(",", "%2C")
        b_loc = loc.replace(" ", "+").replace(",", "")
        
        url_a = airbnb_base.format(a_loc, checkin, checkout, adults, children) + a_params
        url_b = booking_base.format(b_loc, checkin, checkout, adults, children) + b_params
        
        urls.append({"platform": "airbnb", "location": loc, "url": url_a})
        urls.append({"platform": "booking", "location": loc, "url": url_b})
        
    return urls

# ─────────────────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config() -> Dict[str, Any]:
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)


def extract_price(text: str) -> float:
    """Parse a price string (EUR, MKD, USD) → float in EUR."""
    if not text:
        return 0.0

    text = text.replace('\xa0', '').replace(' ', '').upper()

    conversion_rate = 1.0
    if "MKD" in text or "ДЕН" in text:
        conversion_rate = 1 / 61.5
    elif "USD" in text or "US$" in text:
        conversion_rate = 1 / 1.08

    cleaned = re.sub(r"[^\d.,]", " ", text)
    nums = []
    for t in cleaned.split():
        if not t:
            continue
        if "," in t and "." in t:
            if t.rfind(".") > t.rfind(","):
                # 1,234.56 — comma is thousands, dot is decimal
                t = t.replace(",", "")
            else:
                # 1.234,56 — dot is thousands, comma is decimal
                t = t.replace(".", "").replace(",", ".")
        elif "," in t:
            parts = t.split(",")
            if len(parts) == 2 and len(parts[-1]) == 3:
                t = t.replace(",", "")   # thousands comma: 3,061 → 3061
            else:
                t = t.replace(",", ".")  # decimal comma: 3,5 → 3.5
        elif "." in t:
            parts = t.split(".")
            if len(parts) == 2 and len(parts[-1]) == 3:
                t = t.replace(".", "")   # thousands dot: 3.061 → 3061
            # else normal decimal dot — leave as-is
        try:
            val = float(t)
            nums.append(val)
        except ValueError:
            pass

    if not nums:
        return 0.0

    converted = [v * conversion_rate for v in nums if (v * conversion_rate) > 20.0]
    if converted:
        return max(converted)
    return 0.0


def load_existing_data() -> List[Dict]:
    """Read the current listings from tracker_data.js if it exists."""
    if not DATA_FILE.exists():
        return []
    content = DATA_FILE.read_text(encoding="utf-8")
    m = re.search(r"window\.__TRACKER_DATA__\s*=\s*(\[.*?\]);", content, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            return []
    return []


def write_tracker_data(listings: List[Dict], last_updated: str):
    """Write tracker_data.js with the current listings."""
    payload = json.dumps(listings, indent=2, ensure_ascii=False)
    js = f"""// Auto-generated by daily_scraper.py — do not edit manually
// Last updated: {last_updated}
window.__TRACKER_DATA__ = {payload};
window.__LAST_UPDATED__ = "{last_updated}";
"""
    DATA_FILE.write_text(js, encoding="utf-8")
    log(f"✅ Wrote {len(listings)} listings to tracker_data.js")


def scrape_airbnb(search: Dict, budget: int, checkin: str, checkout: str) -> List[Dict]:
    """Scrape an Airbnb search results page and return listing dicts."""
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    listings = []
    url = search["url"]
    location = search["location"]
    log(f"  🏠 Airbnb → {location}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                ],
            )
            ctx = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                locale="en-GB",
                timezone_id="Europe/Skopje",
                geolocation={"latitude": 41.9981, "longitude": 21.4254},
                permissions=["geolocation"],
            )
            ctx.set_default_timeout(60_000)
            page = ctx.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            except PWTimeout:
                log("    ⚠️  Timeout loading page, continuing with what loaded")

            time.sleep(4)

            # Scroll to trigger lazy-load
            for _ in range(4):
                page.evaluate("window.scrollBy(0, 900)")
                time.sleep(0.8)

            # Try multiple card selectors
            cards = []
            for sel in [
                '[data-testid="card-container"]',
                '[itemprop="itemListElement"]',
                'div[data-testid="listing-card"]',
            ]:
                try:
                    found = page.locator(sel).all()
                    if found:
                        cards = found
                        log(f"    Found {len(found)} cards ({sel})")
                        break
                except Exception:
                    continue

            if not cards:
                log("    ⚠️  No cards found on Airbnb page")
                browser.close()
                return listings

            now = datetime.now().isoformat()
            for i, card in enumerate(cards[:15]):
                try:
                    link_el = card.locator("a").first
                    if not link_el.count():
                        continue
                    href = link_el.get_attribute("href") or ""
                    if not href:
                        continue
                    full_url = (
                        f"https://www.airbnb.com{href}"
                        if href.startswith("/")
                        else href
                    )
                    # Use canonical URL for hashing and merging
                    canonical_url = full_url.split("?")[0]

                    # Title
                    title = f"Airbnb Property {i+1}"
                    for tsel in [
                        '[data-testid="listing-card-title"]',
                        'div[data-testid="listing-card-title"]',
                        "div.t1jojoys",
                        "span.t1jojoys",
                    ]:
                        try:
                            el = card.locator(tsel).first
                            if el.count():
                                t = el.inner_text().strip()
                                if t:
                                    title = t
                                    break
                        except Exception:
                            continue

                    # Price (total for stay) — scan ALL selectors and take the max,
                    # so the total price (large) beats per-night (small) even if
                    # per-night is found first.
                    price = 0.0
                    for psel in [
                        '[data-testid="price-availability-row"]',
                        "span._tyxjp1",
                        "span._1y74zjx",
                        "div._1jo4hgw",
                        "span.a8jt5op",
                        "div._wmq1k2",
                    ]:
                        try:
                            el = card.locator(psel).first
                            if el.count():
                                candidate = extract_price(el.inner_text())
                                if candidate > price:
                                    price = candidate
                        except Exception:
                            continue

                    # Fallback: search full card text for "NUMBER total" pattern
                    if price == 0:
                        try:
                            full_text = card.inner_text()
                            m = re.search(
                                r'([\d]{1,3}(?:[.,][\d]{3})*)\s*(?:total)',
                                full_text, re.IGNORECASE
                            )
                            if m:
                                candidate = extract_price(m.group(1))
                                if candidate > price:
                                    price = candidate
                        except Exception:
                            pass

                    # If the extracted value is implausibly low for a total stay price,
                    # treat it as per-night and multiply. Threshold: €150/night min.
                    nights = (
                        datetime.strptime(checkout, "%Y-%m-%d")
                        - datetime.strptime(checkin, "%Y-%m-%d")
                    ).days
                    if 0 < price < nights * 150:
                        log(f"    ℹ️  Per-night heuristic applied: €{price:.0f}/night → €{price*nights:.0f} total")
                        price = price * nights
                    if price > nights * 1500:
                        log(f"    ⚠️  Price €{price:.0f} exceeds sanity cap, discarding")
                        price = 0.0

                    listings.append({
                        "id": int(hashlib.md5(canonical_url.encode()).hexdigest(), 16) % 1_000_000,
                        "title": title,
                        "platform": "airbnb",
                        "location": location,
                        "url": full_url,
                        "priceHistory": [{"price": price, "date": now}],
                        "addedAt": now,
                    })
                    log(f"    ✓ {title[:50]} — €{price:.0f}")
                except Exception as ex:
                    log(f"    ⚠️  Card {i+1} error: {str(ex)[:80]}")

            browser.close()
    except Exception as ex:
        log(f"  ❌ Airbnb scrape failed: {str(ex)[:120]}")

    return listings


def scrape_booking(search: Dict, budget: int, checkin: str, checkout: str) -> List[Dict]:
    """Scrape a Booking.com search results page and return listing dicts."""
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

    listings = []
    url = search["url"]
    location = search["location"]
    log(f"  🏨 Booking.com → {location}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                ],
            )
            ctx = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                locale="en-GB",
                timezone_id="Europe/Skopje",
                geolocation={"latitude": 41.9981, "longitude": 21.4254},
                permissions=["geolocation"],
            )
            ctx.set_default_timeout(60_000)
            page = ctx.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            except PWTimeout:
                log("    ⚠️  Timeout loading page, continuing with what loaded")

            # Accept cookie popup if present
            for cookie_sel in [
                'button:has-text("Accept")',
                'button[id="onetrust-accept-btn-handler"]',
                'button:has-text("Agree")',
            ]:
                try:
                    btn = page.locator(cookie_sel).first
                    if btn.count() and btn.is_visible(timeout=3000):
                        btn.click()
                        time.sleep(1)
                        break
                except Exception:
                    pass

            time.sleep(4)

            for _ in range(4):
                page.evaluate("window.scrollBy(0, 900)")
                time.sleep(0.8)

            cards = []
            for sel in [
                '[data-testid="property-card"]',
                "div[data-testid=\"property-card\"]",
                "div.sr_property_block",
            ]:
                try:
                    found = page.locator(sel).all()
                    if found:
                        cards = found
                        log(f"    Found {len(found)} cards ({sel})")
                        break
                except Exception:
                    continue

            if not cards:
                log("    ⚠️  No cards found on Booking.com page")
                browser.close()
                return listings

            now = datetime.now().isoformat()
            for i, card in enumerate(cards[:15]):
                try:
                    # Link + title
                    link_el = card.locator(
                        'a[data-testid="title-link"], a.hotel_name_link'
                    ).first
                    if not link_el.count():
                        link_el = card.locator("a").first
                    if not link_el.count():
                        continue

                    href = link_el.get_attribute("href") or ""
                    full_url = (
                        f"https://www.booking.com{href}"
                        if href.startswith("/")
                        else href
                    )
                    canonical_url = full_url.split("?")[0]

                    title = link_el.inner_text().strip() or f"Booking.com Property {i+1}"

                    # Price
                    price = 0.0
                    for psel in [
                        '[data-testid="prco-total-price"]',
                        '[data-testid="price-and-discounted-price"]',
                        '[data-testid="prco-inline-available-price"]',
                        '.bui-price-display__value',
                        'div.prco-valign-middle-helper',
                    ]:
                        try:
                            # Use .last to get the deepest/discounted price span, not outer wrapper
                            el = card.locator(psel).last
                            if el.count():
                                candidate = extract_price(el.inner_text())
                                if candidate > price:
                                    price = candidate
                        except Exception:
                            continue

                    # Same per-night guard as Airbnb
                    nights = (
                        datetime.strptime(checkout, "%Y-%m-%d")
                        - datetime.strptime(checkin, "%Y-%m-%d")
                    ).days
                    if 0 < price < nights * 150:
                        log(f"    ℹ️  Per-night heuristic applied: €{price:.0f}/night → €{price*nights:.0f} total")
                        price = price * nights
                    if price > nights * 1500:
                        log(f"    ⚠️  Price €{price:.0f} exceeds sanity cap, discarding")
                        price = 0.0

                    listings.append({
                        "id": int(hashlib.md5(canonical_url.encode()).hexdigest(), 16) % 1_000_000,
                        "title": title,
                        "platform": "booking",
                        "location": location,
                        "url": full_url,
                        "priceHistory": [{"price": price, "date": now}],
                        "addedAt": now,
                    })
                    log(f"    ✓ {title[:50]} — €{price:.0f}")
                except Exception as ex:
                    log(f"    ⚠️  Card {i+1} error: {str(ex)[:80]}")

            browser.close()
    except Exception as ex:
        log(f"  ❌ Booking.com scrape failed: {str(ex)[:120]}")

    return listings


def merge_listings(existing: List[Dict], fresh: List[Dict]) -> List[Dict]:
    """
    Merge fresh scrape results into existing data.
    - New listings are added.
    - Existing listings get a new price-history entry appended (once per day).
    - Any listing not seen in the fresh batch retains its last entry.
    """
    import re as _re

    def normalise_url(u: str) -> str:
        """Strip query string and Booking.com locale suffixes for stable keying."""
        base = u.split("?")[0]
        # Booking.com: /hotel/gr/name.en-gb.html → /hotel/gr/name.html
        base = _re.sub(r'\.[a-z]{2}(?:-[a-z]{2})?\.html$', '.html', base)
        return base

    by_url: Dict[str, Dict] = {normalise_url(item["url"]): item for item in existing}

    for item in fresh:
        key = normalise_url(item["url"])
        # Recompute ID using stable hashlib (not Python's randomised hash())
        stable_id = int(hashlib.md5(key.encode()).hexdigest(), 16) % 1_000_000
        item["id"] = stable_id

        if key in by_url:
            new_price = item["priceHistory"][0]["price"] if item["priceHistory"] else 0
            if new_price > 0:
                today = item["priceHistory"][0]["date"][:10]
                existing_dates = {e["date"][:10] for e in by_url[key]["priceHistory"]}
                if today not in existing_dates:
                    # New day — append new price point
                    by_url[key]["priceHistory"].append(item["priceHistory"][0])
                else:
                    # Same day re-run — overwrite today's entry with latest price
                    for e in by_url[key]["priceHistory"]:
                        if e["date"][:10] == today:
                            e["price"] = new_price
                            e["date"] = item["priceHistory"][0]["date"]
                            break
            by_url[key]["url"] = item["url"]
            by_url[key]["id"] = stable_id
        else:
            by_url[key] = item

    result = list(by_url.values())
    for item in result:
        item["priceHistory"].sort(key=lambda e: e["date"])
    return result


def main():
    log("=" * 60)
    log("🏖️  VACATION PRICE SCRAPER — DAILY RUN")
    log("=" * 60)
    log("[PROGRESS] 0% - Starting Engine")

    config = load_config()
    budget: int = config.get("budget", 1500)
    checkin: str = config.get("checkin", "2026-06-25")
    checkout: str = config.get("checkout", "2026-07-05")
    
    urls_to_scrape = generate_urls(config)

    # Load what we already have
    existing = load_existing_data()
    log(f"📂 Loaded {len(existing)} existing listings")

    fresh: List[Dict] = []
    
    total = len(urls_to_scrape)
    for i, search in enumerate(urls_to_scrape):
        pct = int(((i) / total) * 100)
        log(f"[PROGRESS] {pct}% - Scraping {search['platform'].title()} {search['location']}")
        try:
            if search["platform"] == "airbnb":
                results = scrape_airbnb(search, budget, checkin, checkout)
            else:
                results = scrape_booking(search, budget, checkin, checkout)
            fresh.extend(results)
            time.sleep(3)   # polite pause between searches
        except Exception as ex:
            log(f"  ❌ Unexpected error: {str(ex)[:120]}")
            continue

    log(f"\n📊 Fresh listings scraped: {len(fresh)}")

    # Merge and save
    log("[PROGRESS] 99% - Merging Results")
    merged = merge_listings(existing, fresh)
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_tracker_data(merged, last_updated)

    log("=" * 60)
    log(f"✅ Done. {len(merged)} total listings in tracker_data.js")
    log("[PROGRESS] 100% - Done")
    log("=" * 60)


if __name__ == "__main__":
    main()
