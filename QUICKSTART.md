# 🚀 Quick Start Guide

Get up and running in 3 minutes!

## Step 1: Install Dependencies

Open Terminal and run:

```bash
cd /Users/mihajlo/Desktop/odmor
pip3 install -r requirements.txt
playwright install chromium
```

Wait for installation to complete (2-3 minutes).

## Step 2: Run the Scraper

**Option A: Use the convenient script**

```bash
./run.sh
```

**Option B: Run directly**

```bash
python3 vacation_scraper.py
```

## Step 3: View Results

The script will automatically open `vacation_report.html` in your browser.

If not, double-click the file in Finder.

## What Happens?

1. Browser windows will open (Chromium)
2. Script visits Airbnb and Booking.com
3. Searches for properties in:
   - Vourvourou, Chalkidiki
   - Sithonia, Chalkidiki
   - Kassandra, Chalkidiki
   - Parga, Ionian
   - Sivota, Ionian
   - Lefkada, Ionian

4. Saves data to `listings_data.json`
5. Generates `vacation_report.html`

**First run takes 5-10 minutes** - be patient!

## Track Price Changes

Run the script again anytime:

```bash
./run.sh
```

It will:
- Update prices for existing listings
- Find new listings
- Show price changes in the report

## Customize Search

Edit `config.json` to change:
- Dates
- Number of guests
- Budget
- Locations to search

## Need Help?

See `README.md` for full documentation.

---

**Pro Tip**: Run the scraper daily for best price tracking!
