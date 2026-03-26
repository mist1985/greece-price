"""
HTML Report Generator for Vacation Scraper
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import json


class ReportGenerator:
    def __init__(self, history: Dict[str, Any], config: Dict[str, Any]):
        self.history = history
        self.config = config
        self.output_file = Path("vacation_report.html")

    def generate(self):
        """Generate the HTML report"""
        print(f"\n📊 Generating report...")

        # Sort listings by price
        listings = sorted(
            self.history['listings'],
            key=lambda x: x.get('current_price', float('inf'))
        )

        # Filter by budget
        within_budget = [l for l in listings if l.get('current_price', 0) <= self.config['budget']]
        over_budget = [l for l in listings if l.get('current_price', float('inf')) > self.config['budget']]

        html = self.generate_html(listings, within_budget, over_budget)

        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ Report saved to {self.output_file}")
        print(f"   Within budget: {len(within_budget)} listings")
        print(f"   Over budget: {len(over_budget)} listings")

    def get_price_change(self, listing: Dict[str, Any]) -> tuple:
        """Get price change information"""
        price_history = listing.get('price_history', [])
        if len(price_history) < 2:
            return 0, 0, 'same'

        current = price_history[-1]['price']
        previous = price_history[-2]['price']
        change = current - previous
        change_percent = (change / previous * 100) if previous > 0 else 0

        if change > 0:
            return change, change_percent, 'up'
        elif change < 0:
            return change, change_percent, 'down'
        else:
            return 0, 0, 'same'

    def generate_html(self, listings: List[Dict], within_budget: List[Dict], over_budget: List[Dict]) -> str:
        """Generate the HTML content"""

        # Prepare data for JavaScript
        listings_json = json.dumps(listings, ensure_ascii=False)

        last_scrape = "Never"
        if self.history.get('scrape_history'):
            last_scrape_time = datetime.fromisoformat(self.history['scrape_history'][-1]['timestamp'])
            last_scrape = last_scrape_time.strftime("%B %d, %Y at %I:%M %p")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Greece Vacation Properties Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            max-width: 1400px;
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
            font-size: 3em;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.2em;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}

        .summary-card.green {{
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }}

        .summary-card.red {{
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        }}

        .summary-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}

        .summary-value {{
            font-size: 2.5em;
            font-weight: 700;
        }}

        .filters {{
            background: #f8f9ff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-group {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .filter-btn.active {{
            background: #667eea;
            color: white;
        }}

        .filter-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }}

        select {{
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
        }}

        .listings-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}

        .listing-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 20px;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
        }}

        .listing-card:hover {{
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transform: translateY(-5px);
        }}

        .listing-card.budget-ok {{
            border-color: #10b981;
            background: #f0fdf4;
        }}

        .listing-card.budget-over {{
            border-color: #ef4444;
            background: #fef2f2;
        }}

        .listing-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}

        .listing-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            flex: 1;
            margin-right: 10px;
        }}

        .platform-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            white-space: nowrap;
        }}

        .platform-airbnb {{
            background: #ff5a5f;
            color: white;
        }}

        .platform-booking {{
            background: #003580;
            color: white;
        }}

        .listing-location {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .listing-price {{
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
            margin: 15px 0;
        }}

        .price-per-night {{
            font-size: 0.5em;
            color: #666;
            font-weight: 400;
        }}

        .price-change {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}

        .price-up {{
            background: #fee;
            color: #dc2626;
        }}

        .price-down {{
            background: #efe;
            color: #059669;
        }}

        .listing-rating {{
            display: flex;
            align-items: center;
            gap: 5px;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}

        .listing-meta {{
            color: #999;
            font-size: 0.85em;
            margin-top: auto;
            padding-top: 15px;
            border-top: 1px solid #e0e0e0;
        }}

        .listing-link {{
            display: inline-block;
            margin-top: 15px;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .listing-link:hover {{
            background: #5568d3;
            transform: translateY(-2px);
        }}

        .chart-section {{
            margin: 40px 0;
            padding: 30px;
            background: #f8f9ff;
            border-radius: 15px;
        }}

        .chart-section h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}

        .no-results {{
            text-align: center;
            padding: 60px;
            color: #666;
            font-size: 1.2em;
        }}

        .update-info {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}

            h1 {{
                font-size: 2em;
            }}

            .listings-grid {{
                grid-template-columns: 1fr;
            }}

            .summary {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏖️ Greece Vacation Properties</h1>
        <p class="subtitle">Summer 2026 - {self.config['checkin']} to {self.config['checkout']}</p>

        <!-- Summary Cards -->
        <div class="summary">
            <div class="summary-card">
                <div class="summary-label">Total Listings Found</div>
                <div class="summary-value">{len(listings)}</div>
            </div>
            <div class="summary-card green">
                <div class="summary-label">Within Budget</div>
                <div class="summary-value">{len(within_budget)}</div>
            </div>
            <div class="summary-card red">
                <div class="summary-label">Over Budget</div>
                <div class="summary-value">{len(over_budget)}</div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Your Budget</div>
                <div class="summary-value">€{self.config['budget']}</div>
            </div>
        </div>

        <!-- Filters -->
        <div class="filters">
            <div class="filter-group">
                <button class="filter-btn active" onclick="filterBudget('all')">All Listings</button>
                <button class="filter-btn" onclick="filterBudget('within')">Within Budget</button>
                <button class="filter-btn" onclick="filterBudget('over')">Over Budget</button>
            </div>
            <div class="filter-group">
                <label>Platform:</label>
                <select id="platformFilter" onchange="applyFilters()">
                    <option value="all">All Platforms</option>
                    <option value="airbnb">Airbnb</option>
                    <option value="booking">Booking.com</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Location:</label>
                <select id="locationFilter" onchange="applyFilters()">
                    <option value="all">All Locations</option>
                    {self._generate_location_options()}
                </select>
            </div>
            <div class="filter-group">
                <label>Sort by:</label>
                <select id="sortFilter" onchange="applyFilters()">
                    <option value="price-asc">Price: Low to High</option>
                    <option value="price-desc">Price: High to Low</option>
                    <option value="recent">Recently Added</option>
                </select>
            </div>
        </div>

        <!-- Listings Grid -->
        <div id="listingsContainer" class="listings-grid">
            {self._generate_listing_cards(listings)}
        </div>

        <!-- Charts -->
        {self._generate_charts_html(listings)}

        <!-- Update Info -->
        <div class="update-info">
            <p><strong>Last updated:</strong> {last_scrape}</p>
            <p>Total scrapes: {len(self.history.get('scrape_history', []))}</p>
            <p>Run <code>python vacation_scraper.py</code> to update data</p>
        </div>
    </div>

    <script>
        const allListings = {listings_json};
        let currentFilter = 'all';

        function filterBudget(type) {{
            currentFilter = type;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            applyFilters();
        }}

        function applyFilters() {{
            const platform = document.getElementById('platformFilter').value;
            const location = document.getElementById('locationFilter').value;
            const sort = document.getElementById('sortFilter').value;
            const budget = {self.config['budget']};

            let filtered = allListings.filter(listing => {{
                // Budget filter
                if (currentFilter === 'within' && listing.current_price > budget) return false;
                if (currentFilter === 'over' && listing.current_price <= budget) return false;

                // Platform filter
                if (platform !== 'all' && listing.platform !== platform) return false;

                // Location filter
                if (location !== 'all' && !listing.location.includes(location)) return false;

                return true;
            }});

            // Sort
            if (sort === 'price-asc') {{
                filtered.sort((a, b) => a.current_price - b.current_price);
            }} else if (sort === 'price-desc') {{
                filtered.sort((a, b) => b.current_price - a.current_price);
            }} else if (sort === 'recent') {{
                filtered.sort((a, b) => new Date(b.first_seen) - new Date(a.first_seen));
            }}

            renderListings(filtered);
        }}

        function renderListings(listings) {{
            const container = document.getElementById('listingsContainer');

            if (listings.length === 0) {{
                container.innerHTML = '<div class="no-results">No listings match your filters</div>';
                return;
            }}

            container.innerHTML = listings.map(listing => {{
                const budget = {self.config['budget']};
                const nights = {self.config.get('nights', 10)};
                const isWithinBudget = listing.current_price <= budget;
                const pricePerNight = (listing.current_price / nights).toFixed(0);

                let priceChangeHtml = '';
                if (listing.price_history && listing.price_history.length > 1) {{
                    const current = listing.price_history[listing.price_history.length - 1].price;
                    const previous = listing.price_history[listing.price_history.length - 2].price;
                    const change = current - previous;
                    if (change !== 0) {{
                        const changeClass = change > 0 ? 'price-up' : 'price-down';
                        const arrow = change > 0 ? '↑' : '↓';
                        priceChangeHtml = `<span class="price-change ${{changeClass}}">${{arrow}} €${{Math.abs(change).toFixed(0)}}</span>`;
                    }}
                }}

                const firstSeen = new Date(listing.first_seen).toLocaleDateString();
                const checksCount = listing.price_history ? listing.price_history.length : 1;

                return `
                    <div class="listing-card ${{isWithinBudget ? 'budget-ok' : 'budget-over'}}">
                        <div class="listing-header">
                            <div class="listing-title">${{listing.title}}</div>
                            <span class="platform-badge platform-${{listing.platform}}">
                                ${{listing.platform === 'airbnb' ? 'Airbnb' : 'Booking.com'}}
                            </span>
                        </div>

                        <div class="listing-location">
                            📍 ${{listing.location}}
                        </div>

                        ${{listing.rating && listing.rating !== 'N/A' ? `
                            <div class="listing-rating">
                                ⭐ ${{listing.rating}}
                            </div>
                        ` : ''}}

                        <div class="listing-price">
                            €${{listing.current_price.toFixed(0)}}
                            ${{priceChangeHtml}}
                            <span class="price-per-night">€${{pricePerNight}}/night</span>
                        </div>

                        <div class="listing-meta">
                            First seen: ${{firstSeen}} | Tracked ${{checksCount}} time(s)
                        </div>

                        <a href="${{listing.url}}" target="_blank" class="listing-link">
                            View Property →
                        </a>
                    </div>
                `;
            }}).join('');
        }}

        // Initialize
        renderListings(allListings);
    </script>
</body>
</html>"""

        return html

    def _generate_location_options(self) -> str:
        """Generate location filter options"""
        locations = set()
        for listing in self.history['listings']:
            location = listing.get('location', '')
            if location:
                # Extract main location name
                main_location = location.split(',')[0].strip()
                locations.add(main_location)

        options = [f'<option value="{loc}">{loc}</option>' for loc in sorted(locations)]
        return '\n'.join(options)

    def _generate_listing_cards(self, listings: List[Dict]) -> str:
        """This is handled by JavaScript in the HTML"""
        return ''  # JavaScript will render dynamically

    def _generate_charts_html(self, listings: List[Dict]) -> str:
        """Generate chart section if there's price history"""
        has_history = any(
            len(listing.get('price_history', [])) > 1
            for listing in listings
        )

        if not has_history:
            return ''

        return """
        <div class="chart-section">
            <h2>📈 Price Trends</h2>
            <canvas id="priceChart"></canvas>
        </div>

        <script>
            // Price trend chart
            const ctx = document.getElementById('priceChart');
            if (ctx) {
                const datasets = allListings
                    .filter(l => l.price_history && l.price_history.length > 1)
                    .slice(0, 10)  // Top 10 for readability
                    .map((listing, index) => {
                        const colors = ['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'];
                        const color = colors[index % colors.length];

                        return {
                            label: listing.title.substring(0, 30) + '...',
                            data: listing.price_history.map(entry => ({
                                x: new Date(entry.scraped_at),
                                y: entry.price
                            })),
                            borderColor: color,
                            backgroundColor: color + '20',
                            tension: 0.4
                        };
                    });

                new Chart(ctx, {
                    type: 'line',
                    data: { datasets },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: true, position: 'top' },
                            title: { display: true, text: 'Price History (Top 10 Listings)' }
                        },
                        scales: {
                            x: {
                                type: 'time',
                                time: { unit: 'day' },
                                title: { display: true, text: 'Date' }
                            },
                            y: {
                                title: { display: true, text: 'Price (EUR)' },
                                beginAtZero: false
                            }
                        }
                    }
                });
            }
        </script>
        """


if __name__ == "__main__":
    # For testing
    import json
    with open('listings_data.json', 'r') as f:
        history = json.load(f)
    with open('config.json', 'r') as f:
        config = json.load(f)

    generator = ReportGenerator(history, config)
    generator.generate()
