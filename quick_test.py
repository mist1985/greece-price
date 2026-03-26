#!/usr/bin/env python3
"""Quick test of the scraper with just one location"""

from auto_scraper import AutomatedScraper
import json

# Create a minimal config for testing
test_config = {
    "checkin": "2026-06-25",
    "checkout": "2026-07-05",
    "adults": 2,
    "children": 2,
    "budget": 1500,
    "locations": ["Vourvourou, Greece"]
}

# Save test config
with open('test_config_temp.json', 'w') as f:
    json.dump(test_config, f)

print("=" * 70)
print("🧪 QUICK TEST - One Location Only")
print("=" * 70)
print("\nTesting: Vourvourou, Greece")
print("This will take about 2 minutes...\n")

scraper = AutomatedScraper('test_config_temp.json')

# Test just Airbnb for Vourvourou
print("Testing Airbnb scraper...")
listings = scraper.scrape_airbnb_location("Vourvourou, Greece", max_results=3)

print(f"\n{'=' * 70}")
print(f"TEST RESULTS:")
print(f"{'=' * 70}")
print(f"Found {len(listings)} properties")

if len(listings) > 0:
    print("\n✅ SUCCESS! Scraper is working!")
    print("\nSample property:")
    for listing in listings[:1]:
        print(f"  Title: {listing['title']}")
        print(f"  Price: €{listing['price']}")
        print(f"  URL: {listing['url']}")
else:
    print("\n⚠️  No properties found. This could mean:")
    print("  1. No available properties for these dates")
    print("  2. Website layout changed")
    print("  3. Network issues")
    print("\nCheck debug_airbnb_Vourvourou_Greece.png for screenshot")

print("\n" + "=" * 70)
print("If successful, run the full scraper with: python3 auto_scraper.py")
print("=" * 70)
