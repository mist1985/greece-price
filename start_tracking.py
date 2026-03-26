#!/usr/bin/env python3
"""
Greece Vacation Tracker - Start Script
Generates search links and opens the tracker
"""

import webbrowser
import os
from url_generator import URLGenerator


def main():
    print("=" * 70)
    print("🏖️  GREECE VACATION TRACKER")
    print("=" * 70)
    print()

    # Generate search links
    print("📝 Step 1: Generating search links...")
    generator = URLGenerator()
    urls_data = generator.generate_html_links()

    print(f"✅ Generated links for {len(urls_data['locations'])} locations")
    print()

    # Check if tracker exists
    if not os.path.exists('vacation_tracker.html'):
        print("❌ Error: vacation_tracker.html not found!")
        return

    print("📝 Step 2: Opening in your browser...")
    print()

    # Open search links page
    search_links_path = os.path.abspath('search_links.html')
    webbrowser.open(f'file://{search_links_path}')

    print("=" * 70)
    print("✅ ALL SET!")
    print("=" * 70)
    print()
    print("📖 HOW TO USE:")
    print()
    print("1. 🔍 SEARCH LINKS page just opened in your browser")
    print("   - Click each link to browse properties")
    print("   - Find properties you like")
    print()
    print("2. 📋 When you find a property:")
    print("   - Copy the URL from your browser")
    print("   - Note the total price")
    print()
    print("3. 📊 Go to the TRACKER (click link at bottom of search page)")
    print("   - Paste the URL")
    print("   - Enter the price")
    print("   - Click 'Add'")
    print()
    print("4. 🔄 TRACK PRICES:")
    print("   - Repeat this process daily/weekly")
    print("   - Update prices for existing properties")
    print("   - Watch the price trends!")
    print()
    print("=" * 70)
    print()
    print("💡 TIP: Bookmark both pages for easy access!")
    print()
    print("⚡ Quick links:")
    print(f"   Search Links: file://{search_links_path}")
    print(f"   Tracker: file://{os.path.abspath('vacation_tracker.html')}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
