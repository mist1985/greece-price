# 🏖️ Greece Vacation Property Scraper

Automatically scrape and track vacation rental prices from Airbnb and Booking.com for your dream summer vacation in Greece!

## Features

✅ **Automated Scraping** - Scrapes Airbnb and Booking.com automatically
✅ **Price Tracking** - Tracks price changes over time
✅ **Budget Filtering** - Highlights properties within your budget
✅ **Multiple Locations** - Search across multiple Greek destinations
✅ **Beautiful Reports** - Generates interactive HTML reports with charts
✅ **Historical Data** - Keeps history of all price checks

## Setup Instructions

### 1. Install Python

Make sure you have Python 3.8 or higher installed:

```bash
python3 --version
```

### 2. Install Dependencies

```bash
# Install required Python packages
pip3 install -r requirements.txt

# Install Playwright browsers (required for web scraping)
playwright install chromium
```

### 3. Configure Your Search

Edit `config.json` to customize your search:

```json
{
  "checkin": "2026-06-25",
  "checkout": "2026-07-05",
  "adults": 2,
  "children": 2,
  "budget": 1500,
  "locations": [
    "Vourvourou, Chalkidiki, Greece",
    "Sithonia, Chalkidiki, Greece",
    "Kassandra, Chalkidiki, Greece",
    "Parga, Ionian, Greece",
    "Sivota, Ionian, Greece"
  ],
  "max_listings_per_location": 10
}
```

**Configuration Options:**

- `checkin` / `checkout`: Your travel dates (YYYY-MM-DD format)
- `adults` / `children`: Number of guests
- `budget`: Maximum budget in EUR for the entire stay
- `locations`: List of locations to search
- `max_listings_per_location`: How many listings to scrape per location

## Usage

### Run the Scraper

```bash
python3 vacation_scraper.py
```

The script will:
1. Open browser windows (Chromium) to visit Airbnb and Booking.com
2. Search each location with your criteria
3. Extract listing details (name, price, URL, rating)
4. Save data to `listings_data.json`
5. Generate an HTML report at `vacation_report.html`

**First run takes 5-10 minutes** depending on number of locations.

### View Results

Open the generated report in your browser:

```bash
open vacation_report.html
```

Or just double-click `vacation_report.html` in Finder.

### Track Price Changes

Run the scraper regularly (daily or weekly):

```bash
python3 vacation_scraper.py
```

Each run:
- Updates prices for previously found listings
- Finds new listings
- Tracks price changes over time
- Updates charts and graphs

### Schedule Automatic Updates

To run automatically, add a cron job (macOS/Linux):

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /Users/mihajlo/Desktop/odmor && /usr/local/bin/python3 vacation_scraper.py
```

Or use macOS Automator to create a daily task.

## Files Overview

```
odmor/
├── vacation_scraper.py      # Main scraper script
├── report_generator.py      # HTML report generator
├── config.json              # Your search configuration
├── requirements.txt         # Python dependencies
├── listings_data.json       # Scraped data (auto-generated)
├── vacation_report.html     # Latest report (auto-generated)
└── README.md               # This file
```

## Understanding the Report

The HTML report shows:

**Summary Cards**
- Total listings found
- How many are within budget
- How many are over budget
- Your budget limit

**Filters**
- Filter by budget (all/within/over)
- Filter by platform (Airbnb/Booking.com)
- Filter by location
- Sort by price or date added

**Listing Cards**
- Property name and platform
- Current price (total for your stay)
- Price per night
- Price changes (↑ increased, ↓ decreased)
- Location and rating
- Direct link to view property

**Price Trends Chart**
- Visual graph showing price changes over time
- Compare multiple properties
- Identify pricing patterns

## Tips for Best Results

### Location Tips

- **Vourvourou**: Beautiful beaches, family-friendly, turquoise waters
- **Sithonia**: Less touristy than Kassandra, pristine beaches
- **Kassandra**: More developed, lots of amenities
- **Parga (Ionian)**: Stunning town, excellent for families
- **Sivota (Ionian)**: Peaceful, crystal-clear waters
- **Lefkada (Ionian)**: Amazing beaches, easily accessible

### Scraping Tips

1. **Run during off-peak hours** (early morning) for faster scraping
2. **Don't run too frequently** - once or twice per day is enough
3. **Be patient** - First run takes time to build the database
4. **Check manually too** - Some properties may not appear in automated searches

### Finding Good Deals

1. **Track for 2-3 weeks** to see pricing patterns
2. **Book when prices drop** - the chart shows trends
3. **Compare platforms** - same property may be cheaper on different platform
4. **Act fast** - good deals disappear quickly

## Troubleshooting

**Browser windows open but nothing happens**

- The sites may have changed their layout
- Try updating Playwright: `pip3 install --upgrade playwright && playwright install`

**No listings found**

- Check your dates are in the future
- Try broader locations (e.g., "Chalkidiki" instead of "Vourvourou")
- Increase `max_listings_per_location` in config

**Script crashes or errors**

- Make sure you have stable internet connection
- Close other programs using too much memory
- Run with fewer locations first to test

**Listings show €0 price**

- The price extraction failed (site layout changed)
- You can manually add prices to `listings_data.json`
- Or check the property URL directly

## Privacy & Ethics

- This scraper is for **personal use only**
- Respects robots.txt and reasonable rate limits
- Uses delays between requests to not overload servers
- Does not circumvent paywalls or access restricted content
- Follows terms of service for personal research

## Legal Notice

This tool is provided for educational and personal use. Users are responsible for complying with the terms of service of Airbnb and Booking.com. Web scraping may be against their ToS. Use at your own risk.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Python and dependencies are up to date
3. Make sure Playwright browsers are installed: `playwright install`
4. Check `listings_data.json` for any error messages

## Future Enhancements

Potential features to add:

- [ ] Email notifications when prices drop
- [ ] More detailed property information (photos, amenities)
- [ ] Price predictions using historical data
- [ ] Mobile-friendly report
- [ ] Export to PDF or spreadsheet
- [ ] Support for more booking platforms

---

**Happy vacation planning! 🌊☀️**

For the best experience in Greece with kids:
- Book early for popular areas like Vourvourou
- Look for properties with air conditioning (essential in summer)
- Check proximity to beach (kids + long walks = not ideal)
- Read reviews about family-friendliness
- Consider places with pools for extra entertainment
