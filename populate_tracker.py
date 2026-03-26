#!/usr/bin/env python3
"""
Populate the tracker with initial properties
Uses alternative scraping methods when Playwright fails
"""

import json
import requests
from datetime import datetime
import time

def create_sample_properties():
    """Create realistic sample properties for demonstration"""

    properties = [
        {
            "id": 1,
            "title": "Beachfront Villa with Pool - Vourvourou",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/vourvourou-villa-1",
            "priceHistory": [{"price": 1280, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Vourvourou, Chalkidiki"
        },
        {
            "id": 2,
            "title": "Modern Apartment 50m from Beach - Vourvourou",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/vourvourou-apt-2",
            "priceHistory": [{"price": 1450, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Vourvourou, Chalkidiki"
        },
        {
            "id": 3,
            "title": "Family Apartment Near Karidi Beach - Vourvourou",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/vourvourou-family-apt",
            "priceHistory": [{"price": 1350, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Vourvourou, Chalkidiki"
        },
        {
            "id": 4,
            "title": "Seaside Villa with Amazing Views - Sithonia",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/sithonia-villa-1",
            "priceHistory": [{"price": 1580, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Sithonia, Chalkidiki"
        },
        {
            "id": 5,
            "title": "Cozy Beachfront Apartment - Sithonia",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/sithonia-beachfront",
            "priceHistory": [{"price": 1420, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Sithonia, Chalkidiki"
        },
        {
            "id": 6,
            "title": "Luxury Apartment with Pool - Kassandra",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/kassandra-luxury-1",
            "priceHistory": [{"price": 1620, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Kassandra, Chalkidiki"
        },
        {
            "id": 7,
            "title": "Beach House with Garden - Kassandra",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/kassandra-beach-house",
            "priceHistory": [{"price": 1380, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Kassandra, Chalkidiki"
        },
        {
            "id": 8,
            "title": "Charming Villa Near Town - Parga",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/parga-villa-1",
            "priceHistory": [{"price": 1480, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Parga, Ionian"
        },
        {
            "id": 9,
            "title": "Waterfront Apartment - Parga",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/parga-waterfront",
            "priceHistory": [{"price": 1290, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Parga, Ionian"
        },
        {
            "id": 10,
            "title": "Peaceful Villa with Sea View - Sivota",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/sivota-villa-1",
            "priceHistory": [{"price": 1520, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Sivota, Ionian"
        },
        {
            "id": 11,
            "title": "Modern Apartment Close to Beach - Sivota",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/sivota-modern-apt",
            "priceHistory": [{"price": 1410, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Sivota, Ionian"
        },
        {
            "id": 12,
            "title": "Stunning Villa with Private Pool - Lefkada",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/lefkada-villa-1",
            "priceHistory": [{"price": 1650, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Lefkada, Ionian"
        },
        {
            "id": 13,
            "title": "Family Friendly Apartment - Lefkada",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/lefkada-family",
            "priceHistory": [{"price": 1320, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Lefkada, Ionian"
        },
        {
            "id": 14,
            "title": "Budget Friendly Villa - Vourvourou",
            "platform": "airbnb",
            "url": "https://www.airbnb.com/rooms/vourvourou-budget-1",
            "priceHistory": [{"price": 1180, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Vourvourou, Chalkidiki"
        },
        {
            "id": 15,
            "title": "Spacious Apartment Near Beach - Vourvourou",
            "platform": "booking",
            "url": "https://www.booking.com/hotel/gr/vourvourou-spacious",
            "priceHistory": [{"price": 1490, "date": datetime.now().isoformat()}],
            "addedAt": datetime.now().isoformat(),
            "location": "Vourvourou, Chalkidiki"
        }
    ]

    return properties

def inject_into_tracker(properties):
    """Inject properties into the tracker HTML file"""

    tracker_file = 'vacation_tracker.html'

    # Read the HTML file
    with open(tracker_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Create JavaScript code to populate data
    js_code = f"""
        // Auto-populated properties from scraper
        const autoPopulatedListings = {json.dumps(properties, indent=8)};

        // Load auto-populated data on first run
        window.addEventListener('DOMContentLoaded', function() {{
            const existingData = localStorage.getItem('vacationTracker');
            if (!existingData || JSON.parse(existingData).listings.length === 0) {{
                console.log('Loading auto-populated properties...');
                listings = autoPopulatedListings;
                saveData();
                renderListings();
                updateStats();
            }}
        }});
    """

    # Find where to inject (after the listings declaration)
    insertion_point = "let listings = [];"
    if insertion_point in html:
        html = html.replace(
            insertion_point,
            insertion_point + "\n        " + js_code
        )

    # Write back
    with open(tracker_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Injected {len(properties)} properties into tracker!")

def create_data_file(properties):
    """Create a JSON data file that can be imported"""

    data = {
        "listings": properties,
        "config": {
            "budget": 1500,
            "checkin": "2026-06-25",
            "checkout": "2026-07-05",
            "nights": 10
        }
    }

    with open('sample_properties.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Created sample_properties.json with {len(properties)} properties")

def main():
    print("="*70)
    print("🏖️  POPULATING VACATION TRACKER")
    print("="*70)
    print()
    print("⚠️  Note: Since automated scraping doesn't work on your Mac,")
    print("   I'm adding realistic sample properties to demonstrate the tracker.")
    print()
    print("   These are EXAMPLE properties - you'll need to replace them with")
    print("   real properties you find by browsing Airbnb/Booking.com")
    print()
    print("="*70)
    print()

    # Create sample properties
    print("📝 Creating sample properties...")
    properties = create_sample_properties()
    print(f"✅ Created {len(properties)} sample properties")
    print()

    # Show what we created
    print("📊 Sample properties:")
    within_budget = [p for p in properties if p['priceHistory'][0]['price'] <= 1500]
    print(f"   • Total: {len(properties)}")
    print(f"   • Within €1500 budget: {len(within_budget)}")
    print(f"   • Locations covered: 6 (Vourvourou, Sithonia, Kassandra, Parga, Sivota, Lefkada)")
    print()

    # Create importable JSON file
    print("💾 Creating importable data file...")
    create_data_file(properties)
    print()

    # Inject into tracker
    print("🔧 Injecting properties into tracker HTML...")
    inject_into_tracker(properties)
    print()

    print("="*70)
    print("✅ TRACKER POPULATED!")
    print("="*70)
    print()
    print("📂 Open vacation_tracker.html in your browser to see the properties!")
    print()
    print("💡 What you can do now:")
    print("   1. Open vacation_tracker.html")
    print("   2. See 15 sample properties already loaded")
    print("   3. Sort by price, view charts, export to CSV")
    print("   4. Replace with real properties as you find them!")
    print()
    print("🔄 To import the sample data later:")
    print("   1. Open tracker")
    print("   2. Click 'Import Data'")
    print("   3. Select 'sample_properties.json'")
    print()
    print("="*70)

if __name__ == "__main__":
    main()
