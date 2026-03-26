#!/usr/bin/env python3
"""
URL Generator for Airbnb and Booking.com
Generates pre-configured search URLs based on your travel criteria
"""

import json
from urllib.parse import quote
from datetime import datetime


class URLGenerator:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def generate_airbnb_url(self, location):
        """Generate Airbnb search URL"""
        checkin = self.config['checkin']
        checkout = self.config['checkout']
        adults = self.config['adults']
        children = self.config['children']

        # URL encode the location
        location_encoded = quote(location)

        url = (
            f"https://www.airbnb.com/s/{location_encoded}/homes?"
            f"checkin={checkin}&"
            f"checkout={checkout}&"
            f"adults={adults}&"
            f"children={children}&"
            f"search_type=filter_change"
        )

        return url

    def generate_booking_url(self, location):
        """Generate Booking.com search URL"""
        checkin = self.config['checkin']
        checkout = self.config['checkout']
        adults = self.config['adults']
        children = self.config['children']

        # Extract main location name
        location_main = location.split(',')[0].strip()
        location_encoded = quote(location_main)

        url = (
            f"https://www.booking.com/searchresults.html?"
            f"ss={location_encoded}&"
            f"checkin={checkin}&"
            f"checkout={checkout}&"
            f"group_adults={adults}&"
            f"group_children={children}&"
            f"no_rooms=1&"
            f"nflt=ht_id%3D201"  # Apartments filter
        )

        return url

    def generate_all_urls(self):
        """Generate all URLs for all locations"""
        urls = {
            'generated_at': datetime.now().isoformat(),
            'trip_details': {
                'checkin': self.config['checkin'],
                'checkout': self.config['checkout'],
                'adults': self.config['adults'],
                'children': self.config['children'],
                'budget': self.config['budget']
            },
            'locations': []
        }

        for location in self.config['locations']:
            location_data = {
                'name': location,
                'airbnb_url': self.generate_airbnb_url(location),
                'booking_url': self.generate_booking_url(location)
            }
            urls['locations'].append(location_data)

        return urls

    def generate_html_links(self):
        """Generate HTML page with clickable links"""
        urls_data = self.generate_all_urls()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Greece Vacation Search Links</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }}

        h1 {{
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}

        .trip-info {{
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}

        .trip-info h2 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .trip-detail {{
            color: #666;
            margin: 5px 0;
        }}

        .instructions {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }}

        .instructions h3 {{
            color: #856404;
            margin-bottom: 10px;
        }}

        .instructions ol {{
            margin-left: 20px;
            color: #856404;
        }}

        .instructions li {{
            margin: 8px 0;
        }}

        .location-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            transition: all 0.3s;
        }}

        .location-card:hover {{
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transform: translateY(-3px);
        }}

        .location-name {{
            font-size: 1.5em;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .link-section {{
            margin: 15px 0;
        }}

        .platform-label {{
            font-weight: 600;
            color: #666;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .link-container {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .search-link {{
            flex: 1;
            padding: 15px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            text-align: center;
            transition: all 0.3s;
            display: block;
        }}

        .search-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .search-link.airbnb {{
            background: linear-gradient(135deg, #ff5a5f 0%, #fc3d43 100%);
        }}

        .search-link.booking {{
            background: linear-gradient(135deg, #003580 0%, #00224f 100%);
        }}

        .copy-btn {{
            padding: 15px 20px;
            background: #10b981;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .copy-btn:hover {{
            background: #059669;
            transform: translateY(-2px);
        }}

        .next-step {{
            background: #d1fae5;
            border: 2px solid #10b981;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            text-align: center;
        }}

        .next-step h3 {{
            color: #065f46;
            margin-bottom: 10px;
        }}

        .next-step p {{
            color: #047857;
            margin-bottom: 15px;
        }}

        .tracker-link {{
            display: inline-block;
            padding: 15px 30px;
            background: #10b981;
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s;
        }}

        .tracker-link:hover {{
            background: #059669;
            transform: translateY(-2px);
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}

            h1 {{
                font-size: 1.8em;
            }}

            .link-container {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏖️ Greece Vacation Search Links</h1>
        <p class="subtitle">Click the links below to search for properties</p>

        <div class="trip-info">
            <h2>📅 Your Trip Details</h2>
            <div class="trip-detail"><strong>Dates:</strong> {urls_data['trip_details']['checkin']} to {urls_data['trip_details']['checkout']}</div>
            <div class="trip-detail"><strong>Guests:</strong> {urls_data['trip_details']['adults']} adults, {urls_data['trip_details']['children']} children</div>
            <div class="trip-detail"><strong>Budget:</strong> €{urls_data['trip_details']['budget']}</div>
        </div>

        <div class="instructions">
            <h3>📋 How to Use</h3>
            <ol>
                <li><strong>Click each link below</strong> to open the search in a new tab</li>
                <li><strong>Browse properties</strong> that fit your budget</li>
                <li><strong>Found something interesting?</strong> Copy the URL and price</li>
                <li><strong>Go to the tracker</strong> (link at bottom) and paste the details</li>
                <li><strong>Repeat</strong> this process daily/weekly to track price changes!</li>
            </ol>
        </div>
"""

        for location in urls_data['locations']:
            html += f"""
        <div class="location-card">
            <div class="location-name">
                📍 {location['name']}
            </div>

            <div class="link-section">
                <div class="platform-label">🏠 Airbnb</div>
                <div class="link-container">
                    <a href="{location['airbnb_url']}" target="_blank" class="search-link airbnb">
                        Search on Airbnb →
                    </a>
                    <button class="copy-btn" onclick="copyToClipboard('{location['airbnb_url']}')">
                        📋 Copy URL
                    </button>
                </div>
            </div>

            <div class="link-section">
                <div class="platform-label">🏨 Booking.com</div>
                <div class="link-container">
                    <a href="{location['booking_url']}" target="_blank" class="search-link booking">
                        Search on Booking.com →
                    </a>
                    <button class="copy-btn" onclick="copyToClipboard('{location['booking_url']}')">
                        📋 Copy URL
                    </button>
                </div>
            </div>
        </div>
"""

        html += """
        <div class="next-step">
            <h3>✅ Done Browsing?</h3>
            <p>Now add the properties you found to your tracker!</p>
            <a href="vacation_tracker.html" class="tracker-link">
                Open Price Tracker →
            </a>
        </div>
    </div>

    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('✅ URL copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        }
    </script>
</body>
</html>"""

        with open('search_links.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print("✅ Search links page generated: search_links.html")
        return urls_data


if __name__ == "__main__":
    print("=" * 70)
    print("🔗 URL GENERATOR")
    print("=" * 70)

    generator = URLGenerator()
    urls = generator.generate_html_links()

    print(f"\n📊 Generated links for {len(urls['locations'])} locations")
    print(f"📅 Trip: {urls['trip_details']['checkin']} to {urls['trip_details']['checkout']}")
    print(f"💰 Budget: €{urls['trip_details']['budget']}")
    print("\n" + "=" * 70)
    print("✅ Open 'search_links.html' in your browser to start searching!")
    print("=" * 70)
