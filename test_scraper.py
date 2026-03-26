#!/usr/bin/env python3
"""
Simple test script to verify scraping works
Tests with just one location to save time
"""

from vacation_scraper import VacationScraper
import json

# Create a test config with just one location
test_config = {
    "checkin": "2026-06-25",
    "checkout": "2026-07-05",
    "adults": 2,
    "children": 2,
    "budget": 1500,
    "locations": ["Vourvourou, Chalkidiki, Greece"],  # Just one location for testing
    "max_listings_per_location": 5,  # Just 5 listings for faster testing
    "min_bedrooms": 2,
    "amenities": ["air conditioning", "wifi"]
}

# Save test config
with open('test_config.json', 'w') as f:
    json.dump(test_config, f, indent=2)

print("=" * 70)
print("🧪 TESTING VACATION SCRAPER")
print("=" * 70)
print("This is a quick test with just one location (Vourvourou)")
print("If this works, the full scraper will work too!")
print("=" * 70)
print()

# Run scraper with test config
scraper = VacationScraper('test_config.json')

# Test just Airbnb first
print("Testing Airbnb scraper...")
airbnb_listings = scraper.scrape_airbnb("Vourvourou, Chalkidiki, Greece")

print(f"\n✅ Airbnb test complete! Found {len(airbnb_listings)} listings")

if len(airbnb_listings) > 0:
    print("\nSample listing:")
    print(f"  Title: {airbnb_listings[0]['title']}")
    print(f"  Price: €{airbnb_listings[0]['price']}")
    print(f"  URL: {airbnb_listings[0]['url']}")
else:
    print("\n⚠️  No listings found. This might be normal if:")
    print("  - No properties available for these dates")
    print("  - Website layout changed")
    print("  - Internet connection issues")

print("\n" + "=" * 70)
print("Test complete! Check output above for results.")
print("=" * 70)
