#!/usr/bin/env python3
"""
Automated Greece Vacation Property Scraper
Scrapes properties, stores in spreadsheet, tracks price changes
"""

import json
import time
import re
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class AutomatedScraper:
    def __init__(self, config_file='config.json'):
        """Initialize the scraper"""
        self.config = self.load_config(config_file)
        self.csv_file = Path('properties.csv')
        self.excel_file = Path('properties.xlsx')
        self.properties = self.load_existing_properties()
        self.new_finds = []
        self.price_drops = []
        self.price_increases = []

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_existing_properties(self) -> Dict[str, Dict]:
        """Load existing properties from CSV"""
        properties = {}
        if self.csv_file.exists():
            df = pd.read_csv(self.csv_file)
            for _, row in df.iterrows():
                url = row['url']
                properties[url] = row.to_dict()
        return properties

    def extract_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        if not price_text:
            return 0.0
        # Remove everything except digits and decimal point
        cleaned = re.sub(r'[^\d.,]', '', price_text)
        cleaned = cleaned.replace(',', '')
        try:
            return float(cleaned)
        except:
            return 0.0

    def scrape_airbnb_location(self, location: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Scrape Airbnb for a location"""
        print(f"\n{'='*70}")
        print(f"🏠 AIRBNB: {location}")
        print(f"{'='*70}")

        listings = []

        try:
            with sync_playwright() as p:
                print("🌐 Launching browser...")
                browser = p.chromium.launch(
                    headless=True,  # Run in background
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                )

                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                )
                context.set_default_timeout(60000)

                page = context.new_page()

                # Build URL
                checkin = self.config['checkin']
                checkout = self.config['checkout']
                adults = self.config['adults']
                children = self.config['children']

                url = (
                    f"https://www.airbnb.com/s/{location.replace(' ', '-')}/homes?"
                    f"checkin={checkin}&checkout={checkout}"
                    f"&adults={adults}&children={children}"
                )

                print(f"📡 Connecting to Airbnb...")

                try:
                    page.goto(url, wait_until='networkidle', timeout=60000)
                    print("✅ Page loaded")
                except Exception as e:
                    print(f"⚠️  Page load warning: {str(e)[:100]}")
                    time.sleep(5)

                # Wait for content
                print("⏳ Waiting for listings...")
                time.sleep(5)

                # Scroll to load more
                for i in range(3):
                    page.evaluate('window.scrollBy(0, 1000)')
                    time.sleep(1)

                # Try to get listings
                print("🔍 Extracting properties...")

                # Multiple selectors to try
                selectors = [
                    '[data-testid="card-container"]',
                    '[itemprop="itemListElement"]',
                    'div[data-testid="listing-card"]',
                    'div.cy5jw6o'
                ]

                cards = []
                for selector in selectors:
                    try:
                        cards = page.locator(selector).all()
                        if len(cards) > 0:
                            print(f"✅ Found {len(cards)} listings using selector: {selector}")
                            break
                    except:
                        continue

                if len(cards) == 0:
                    print("⚠️  No listings found with standard selectors")
                    print("📸 Saving page screenshot for debugging...")
                    page.screenshot(path=f'debug_airbnb_{location.replace(" ", "_")}.png')
                    browser.close()
                    return listings

                # Extract data from cards
                for i, card in enumerate(cards[:max_results]):
                    try:
                        # Get link
                        link = card.locator('a').first
                        if link.count() == 0:
                            continue

                        href = link.get_attribute('href')
                        if not href:
                            continue

                        full_url = f"https://www.airbnb.com{href}" if href.startswith('/') else href
                        # Clean URL
                        full_url = full_url.split('?')[0]

                        # Get title
                        try:
                            title = card.locator('[data-testid="listing-card-title"]').first.inner_text()
                        except:
                            title = f"Airbnb Property {i+1}"

                        # Get price - try multiple selectors
                        price = 0.0
                        price_selectors = [
                            'span._tyxjp1',
                            'span._1y74zjx',
                            '[data-testid="price-availability-row"]',
                            'div._1jo4hgw',
                        ]

                        for ps in price_selectors:
                            try:
                                price_elem = card.locator(ps).first
                                if price_elem.count() > 0:
                                    price_text = price_elem.inner_text()
                                    price = self.extract_price(price_text)
                                    if price > 0:
                                        break
                            except:
                                continue

                        # Get rating
                        rating = "N/A"
                        try:
                            rating = card.locator('[aria-label*="rating"]').first.inner_text()
                        except:
                            pass

                        listing = {
                            'platform': 'Airbnb',
                            'location': location,
                            'title': title.strip(),
                            'url': full_url,
                            'price': price,
                            'rating': rating,
                            'first_seen': datetime.now().isoformat(),
                            'last_checked': datetime.now().isoformat(),
                            'check_count': 1
                        }

                        listings.append(listing)
                        print(f"  ✓ [{i+1}] {title[:45]}... - €{price:.0f}")

                    except Exception as e:
                        print(f"  ⚠️  Error extracting listing {i+1}: {str(e)[:50]}")
                        continue

                browser.close()
                print(f"\n✅ Extracted {len(listings)} properties from Airbnb")

        except Exception as e:
            print(f"❌ Error scraping Airbnb: {str(e)}")

        return listings

    def scrape_booking_location(self, location: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Scrape Booking.com for a location"""
        print(f"\n{'='*70}")
        print(f"🏨 BOOKING.COM: {location}")
        print(f"{'='*70}")

        listings = []

        try:
            with sync_playwright() as p:
                print("🌐 Launching browser...")
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox'
                    ]
                )

                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                )
                context.set_default_timeout(60000)

                page = context.new_page()

                # Build URL
                checkin = self.config['checkin']
                checkout = self.config['checkout']
                adults = self.config['adults']
                children = self.config['children']
                location_param = location.split(',')[0].replace(' ', '+')

                url = (
                    f"https://www.booking.com/searchresults.html?"
                    f"ss={location_param}&"
                    f"checkin={checkin}&checkout={checkout}&"
                    f"group_adults={adults}&group_children={children}&"
                    f"no_rooms=1&nflt=ht_id%3D201"
                )

                print(f"📡 Connecting to Booking.com...")

                try:
                    page.goto(url, wait_until='networkidle', timeout=60000)
                    print("✅ Page loaded")
                except Exception as e:
                    print(f"⚠️  Page load warning: {str(e)[:100]}")
                    time.sleep(5)

                # Handle cookie popup
                try:
                    accept_btn = page.locator('button:has-text("Accept")').first
                    if accept_btn.count() > 0:
                        accept_btn.click(timeout=3000)
                        time.sleep(1)
                except:
                    pass

                print("⏳ Waiting for listings...")
                time.sleep(5)

                # Scroll
                for i in range(3):
                    page.evaluate('window.scrollBy(0, 1000)')
                    time.sleep(1)

                print("🔍 Extracting properties...")

                # Try multiple selectors
                selectors = [
                    '[data-testid="property-card"]',
                    'div[data-testid="property-card"]',
                    'div.sr_property_block',
                ]

                cards = []
                for selector in selectors:
                    try:
                        cards = page.locator(selector).all()
                        if len(cards) > 0:
                            print(f"✅ Found {len(cards)} listings")
                            break
                    except:
                        continue

                if len(cards) == 0:
                    print("⚠️  No listings found")
                    print("📸 Saving screenshot...")
                    page.screenshot(path=f'debug_booking_{location.replace(" ", "_")}.png')
                    browser.close()
                    return listings

                for i, card in enumerate(cards[:max_results]):
                    try:
                        # Get link and title
                        link = card.locator('a[data-testid="title-link"]').first
                        if link.count() == 0:
                            link = card.locator('a.hotel_name_link').first

                        if link.count() == 0:
                            continue

                        href = link.get_attribute('href')
                        full_url = f"https://www.booking.com{href}" if href.startswith('/') else href
                        full_url = full_url.split('?')[0]

                        title = link.inner_text().strip()

                        # Get price
                        price = 0.0
                        price_selectors = [
                            '[data-testid="price-and-discounted-price"]',
                            'span[data-testid="price-and-discounted-price"]',
                            'div.prco-valign-middle-helper',
                        ]

                        for ps in price_selectors:
                            try:
                                price_elem = card.locator(ps).first
                                if price_elem.count() > 0:
                                    price_text = price_elem.inner_text()
                                    price = self.extract_price(price_text)
                                    if price > 0:
                                        break
                            except:
                                continue

                        # Get rating
                        rating = "N/A"
                        try:
                            rating = card.locator('[data-testid="review-score"]').first.inner_text()
                        except:
                            pass

                        listing = {
                            'platform': 'Booking.com',
                            'location': location,
                            'title': title,
                            'url': full_url,
                            'price': price,
                            'rating': rating,
                            'first_seen': datetime.now().isoformat(),
                            'last_checked': datetime.now().isoformat(),
                            'check_count': 1
                        }

                        listings.append(listing)
                        print(f"  ✓ [{i+1}] {title[:45]}... - €{price:.0f}")

                    except Exception as e:
                        print(f"  ⚠️  Error extracting listing {i+1}: {str(e)[:50]}")
                        continue

                browser.close()
                print(f"\n✅ Extracted {len(listings)} properties from Booking.com")

        except Exception as e:
            print(f"❌ Error scraping Booking.com: {str(e)}")

        return listings

    def scrape_all_new(self):
        """Scrape all locations for new properties"""
        print("\n" + "="*70)
        print("🔍 DISCOVERING NEW PROPERTIES")
        print("="*70)

        all_new = []

        for location in self.config['locations']:
            # Airbnb
            airbnb_listings = self.scrape_airbnb_location(location, max_results=10)
            all_new.extend(airbnb_listings)
            time.sleep(3)

            # Booking.com
            booking_listings = self.scrape_booking_location(location, max_results=10)
            all_new.extend(booking_listings)
            time.sleep(3)

        return all_new

    def update_existing_prices(self):
        """Check prices for all existing properties"""
        print("\n" + "="*70)
        print("🔄 UPDATING PRICES FOR EXISTING PROPERTIES")
        print("="*70)
        print(f"Properties to check: {len(self.properties)}")

        # Group by platform and location for efficiency
        # For now, we'll re-scrape locations and match URLs
        # This is more efficient than checking each URL individually

        # Note: In production, you'd want to visit each URL individually
        # for exact price updates, but that takes much longer

        print("\n💡 Will update prices by re-scanning locations...")
        print("   (Matching URLs from previous scrapes)")

    def merge_and_update(self, new_listings: List[Dict]):
        """Merge new listings with existing, track changes"""
        print("\n" + "="*70)
        print("📊 ANALYZING RESULTS")
        print("="*70)

        for listing in new_listings:
            url = listing['url']

            if url in self.properties:
                # Existing property - check price change
                old_price = float(self.properties[url].get('price', 0))
                new_price = float(listing['price'])

                if new_price > 0 and old_price > 0:
                    if new_price < old_price:
                        drop = old_price - new_price
                        self.price_drops.append({
                            'title': listing['title'],
                            'url': url,
                            'old_price': old_price,
                            'new_price': new_price,
                            'drop': drop,
                            'drop_percent': (drop / old_price) * 100
                        })
                    elif new_price > old_price:
                        increase = new_price - old_price
                        self.price_increases.append({
                            'title': listing['title'],
                            'url': url,
                            'old_price': old_price,
                            'new_price': new_price,
                            'increase': increase,
                            'increase_percent': (increase / old_price) * 100
                        })

                # Update existing
                listing['first_seen'] = self.properties[url].get('first_seen', listing['first_seen'])
                listing['check_count'] = int(self.properties[url].get('check_count', 1)) + 1
                self.properties[url] = listing
            else:
                # New property
                if listing['price'] > 0:  # Only add if we got a price
                    self.new_finds.append(listing)
                    self.properties[url] = listing

    def save_to_spreadsheet(self):
        """Save all properties to CSV and Excel"""
        print("\n" + "="*70)
        print("💾 SAVING TO SPREADSHEET")
        print("="*70)

        # Convert to DataFrame
        df = pd.DataFrame(list(self.properties.values()))

        if df.empty:
            print("⚠️  No data to save")
            return

        # Sort by price
        df = df.sort_values('price', ascending=True)

        # Add budget column
        budget = self.config['budget']
        df['within_budget'] = df['price'].apply(lambda x: 'YES' if x <= budget else 'NO')
        df['price_per_night'] = df['price'] / 10  # 10 nights

        # Reorder columns
        columns = [
            'title', 'platform', 'location', 'price', 'price_per_night',
            'within_budget', 'rating', 'url', 'first_seen', 'last_checked',
            'check_count'
        ]
        df = df[columns]

        # Save CSV
        df.to_csv(self.csv_file, index=False)
        print(f"✅ Saved to CSV: {self.csv_file}")

        # Save Excel with formatting
        with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Properties')

            # Get worksheet
            worksheet = writer.sheets['Properties']

            # Set column widths
            worksheet.column_dimensions['A'].width = 50  # title
            worksheet.column_dimensions['B'].width = 15  # platform
            worksheet.column_dimensions['C'].width = 25  # location
            worksheet.column_dimensions['D'].width = 12  # price
            worksheet.column_dimensions['E'].width = 15  # price_per_night
            worksheet.column_dimensions['F'].width = 15  # within_budget
            worksheet.column_dimensions['G'].width = 12  # rating
            worksheet.column_dimensions['H'].width = 60  # url

        print(f"✅ Saved to Excel: {self.excel_file}")

    def print_summary(self):
        """Print summary of findings"""
        print("\n" + "="*70)
        print("📈 SUMMARY")
        print("="*70)

        total = len(self.properties)
        within_budget = len([p for p in self.properties.values() if p['price'] <= self.config['budget']])

        print(f"\n📊 Total Properties Tracked: {total}")
        print(f"✅ Within Budget (€{self.config['budget']}): {within_budget}")
        print(f"🆕 New Properties Found: {len(self.new_finds)}")
        print(f"📉 Price Drops: {len(self.price_drops)}")
        print(f"📈 Price Increases: {len(self.price_increases)}")

        if self.new_finds:
            print(f"\n🆕 NEW PROPERTIES:")
            for prop in self.new_finds[:5]:
                budget_status = "✅" if prop['price'] <= self.config['budget'] else "❌"
                print(f"  {budget_status} {prop['title'][:45]} - €{prop['price']:.0f} - {prop['platform']}")
            if len(self.new_finds) > 5:
                print(f"  ... and {len(self.new_finds) - 5} more")

        if self.price_drops:
            print(f"\n🎉 PRICE DROPS DETECTED:")
            for drop in sorted(self.price_drops, key=lambda x: x['drop'], reverse=True):
                print(f"  💰 {drop['title'][:45]}")
                print(f"     €{drop['old_price']:.0f} → €{drop['new_price']:.0f} (↓ €{drop['drop']:.0f}, -{drop['drop_percent']:.1f}%)")
                print(f"     {drop['url']}")
                print()

        if self.price_increases:
            print(f"\n⬆️  PRICE INCREASES:")
            for inc in self.price_increases[:3]:
                print(f"  📈 {inc['title'][:45]} - €{inc['old_price']:.0f} → €{inc['new_price']:.0f} (+€{inc['increase']:.0f})")

        # Show cheapest options
        if self.properties:
            sorted_props = sorted(self.properties.values(), key=lambda x: x['price'])
            within = [p for p in sorted_props if p['price'] <= self.config['budget']]

            if within:
                print(f"\n💎 BEST DEALS (Within Budget):")
                for i, prop in enumerate(within[:5], 1):
                    print(f"  {i}. {prop['title'][:45]}")
                    print(f"     €{prop['price']:.0f} (€{prop['price']/10:.0f}/night) - {prop['location']}")
                    print(f"     {prop['platform']} - {prop['url']}")
                    print()

    def run(self):
        """Main execution"""
        print("\n" + "="*70)
        print("🏖️  AUTOMATED GREECE VACATION SCRAPER")
        print("="*70)
        print(f"📅 Dates: {self.config['checkin']} to {self.config['checkout']}")
        print(f"👨‍👩‍👧‍👦 Guests: {self.config['adults']} adults, {self.config['children']} children")
        print(f"💰 Budget: €{self.config['budget']}")
        print(f"📍 Locations: {len(self.config['locations'])}")
        print("="*70)

        # Scrape new properties
        new_listings = self.scrape_all_new()

        # Merge with existing and detect changes
        self.merge_and_update(new_listings)

        # Save to spreadsheet
        self.save_to_spreadsheet()

        # Print summary
        self.print_summary()

        print("\n" + "="*70)
        print("✅ SCRAPING COMPLETE!")
        print("="*70)
        print(f"\n📊 Open these files to view results:")
        print(f"   • {self.csv_file} (CSV)")
        print(f"   • {self.excel_file} (Excel)")
        print("\n💡 Run this script again anytime to update prices!")
        print("="*70 + "\n")


if __name__ == "__main__":
    scraper = AutomatedScraper()
    scraper.run()
