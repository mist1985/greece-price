# 🏖️ Greece Vacation Price Tracker

**The Smart Way to Track Vacation Rental Prices!**

A semi-automated tool that helps you find and track the best vacation rental deals in Greece for your summer 2026 trip.

## Why This Approach?

❌ **Fully automated scraping** doesn't work well because:
- Websites actively block bots
- Requires constant maintenance when sites change
- Often against terms of service

✅ **This semi-automated approach** is better:
- Takes only 2-3 minutes of your time
- Always works (no bot detection)
- Legal and reliable
- Tracks prices over time automatically
- Beautiful visualizations

## Quick Start (3 Minutes!)

### Step 1: Setup (One Time Only)

```bash
cd /Users/mihajlo/Desktop/odmor
pip3 install -r requirements.txt
```

### Step 2: Start Tracking

```bash
python3 start_tracking.py
```

This will:
1. Generate pre-configured search links
2. Open them in your browser
3. Show you exactly what to do next!

## How It Works

### 🔍 Phase 1: Browse (2 minutes)

1. Run `python3 start_tracking.py`
2. Click through the search links that open
3. Browse properties on Airbnb and Booking.com
4. Copy URLs of properties you like

### 📋 Phase 2: Track (1 minute)

1. Open the tracker (link at bottom of search page)
2. Paste the property URL
3. Enter the price
4. Click "Add"

That's it! The property is now tracked.

### 🔄 Phase 3: Monitor (Ongoing)

1. Repeat every few days/weeks
2. Update prices for your tracked properties
3. Watch the trend graphs
4. Book when you see a good deal!

## Features

### 🎯 Smart Search Links
- Pre-configured for your exact dates
- All locations you care about (Vourvourou, Chalkidiki, Ionian)
- Correct number of guests
- Apartment filters already applied

### ⚡ Quick Add Interface
- Just paste URL + price
- Auto-detects Airbnb vs Booking.com
- Instant budget checking
- No forms to fill out!

### 📊 Price Tracking
- Automatic price history
- Shows increase/decrease trends
- Highlights budget-friendly options
- Beautiful charts over time

### 💰 Budget Management
- Set your €1500 budget
- See which properties fit
- Find the cheapest options
- Get alerts for price changes

### 💾 Data Management
- Auto-saves to your browser
- Export to JSON file
- Import previous data
- Never lose your tracking history

## File Overview

```
odmor/
├── start_tracking.py        # Main script - run this!
├── url_generator.py          # Generates search URLs
├── config.json               # Your trip settings
├── search_links.html         # Generated search links
├── vacation_tracker.html     # Main tracker interface
└── README_NEW.md            # This file
```

## Configuration

Edit `config.json` to customize:

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
    "Sivota, Ionian, Greece",
    "Lefkada, Ionian, Greece"
  ]
}
```

## Daily Workflow

### First Time (10-15 minutes):
```bash
python3 start_tracking.py  # Generates links
# Click through all search links
# Add 10-20 interesting properties to tracker
```

### Follow-up Checks (2-3 minutes):
```bash
# Open vacation_tracker.html
# Click each property link
# Update the price if it changed
# Watch for deals!
```

### When to Check:
- **Daily**: If you have time and want the best deal
- **Every 2-3 days**: Good balance
- **Weekly**: Minimum recommended

## Pro Tips

### 🎯 Finding Good Deals

1. **Track 10-20 properties** across different locations
2. **Check morning and evening** - prices change daily
3. **Track for 2-3 weeks** before booking to see patterns
4. **Book immediately** when you see a price drop

### 🏖️ Best Locations for Families

**Vourvourou** (Your dream!)
- Warm, shallow, turquoise waters
- Perfect for young kids
- Beautiful beaches
- Book early - very popular!

**Sithonia**
- Less touristy
- Pristine beaches
- Family-friendly

**Parga (Ionian)**
- Stunning town
- Calm waters
- Great for kids

**Sivota (Ionian)**
- Peaceful
- Crystal-clear water
- Safe swimming

### 💡 Booking Tips

1. **Properties under €1500** - Within your budget
2. **Check cancellation policy** - Free cancellation is best
3. **Read recent reviews** - Focus on families with kids
4. **Air conditioning is essential** - Greece in summer is hot!
5. **Distance to beach** - Closer is better with young kids

## Troubleshooting

**Q: The search links don't show any properties**

A: This is normal! The links open the search page on Airbnb/Booking.com. You'll see the properties there. Just adjust filters if needed.

**Q: I can't find prices on the websites**

A: Make sure your dates are entered correctly. Prices should show for each property. If not, try different dates or locations.

**Q: The tracker isn't saving my properties**

A: Make sure you're using the same browser each time. Data is saved in your browser's local storage.

**Q: Can I use this on my phone?**

A: Yes! The tracker works on mobile. Just bookmark the `vacation_tracker.html` file.

## Export Your Data

Want to keep a backup?

1. Open tracker
2. Click "Export Data"
3. Save the JSON file
4. Import it later with "Import Data"

## Comparison: Old vs New Approach

| Feature | Automated Scraping | This Tool |
|---------|-------------------|-----------|
| Reliability | ❌ Often breaks | ✅ Always works |
| Speed | 10-15 min per run | 2-3 min per check |
| Legality | ⚠️ Gray area | ✅ Totally legal |
| Accuracy | ⚠️ May miss prices | ✅ 100% accurate |
| Maintenance | ❌ Constant fixes | ✅ No maintenance |
| Price tracking | ✅ Yes | ✅ Yes |
| Charts | ✅ Yes | ✅ Yes |

## Success Story

**Example workflow:**

**Week 1**: Add 15 properties
- 5 in Vourvourou
- 5 in Sithonia
- 5 in Parga

**Week 2**: Check prices daily
- 3 properties went up €50-100
- 2 properties went down €30-50
- Identify the stable ones

**Week 3**: Keep monitoring
- One Vourvourou property drops €100!
- Book immediately!
- Save €100 vs original price

**Result**: Perfect vacation rental + saved money!

## Your Vacation Details

According to your config:

- **Dates**: June 25 - July 5, 2026 (10 nights)
- **Guests**: 2 adults + 2 children (ages 9 and 4)
- **Budget**: €1500 total (€150/night)
- **Goal**: Beachfront apartment in Vourvourou or nearby
- **Requirements**: Air conditioning, warm calm waters, kid-friendly

## Next Steps

1. **Now**: Run `python3 start_tracking.py`
2. **Today**: Browse and add 10-15 properties
3. **Tomorrow**: Check if any prices changed
4. **This Week**: Keep monitoring
5. **Next 2-3 Weeks**: Track trends
6. **When Ready**: Book the best deal!

## Support

Having issues? Check:

1. Python 3 is installed: `python3 --version`
2. Config file exists: `config.json`
3. Using modern browser (Chrome, Firefox, Safari)

## Final Thoughts

This tool saves you:
- ⏰ **Time**: 2-3 minutes vs 30+ minutes of manual checking
- 💰 **Money**: Track trends and book at the best price
- 😰 **Stress**: No worry about missing deals
- 📊 **Insight**: Visual trends show when to book

**Ready to find your perfect Greek vacation?**

```bash
python3 start_tracking.py
```

🏖️ **Καλές διακοπές!** (Happy vacation!)
