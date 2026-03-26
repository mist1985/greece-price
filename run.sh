#!/bin/bash

# Greece Vacation Scraper Runner Script

echo "========================================"
echo "🏖️  Greece Vacation Property Scraper"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if dependencies are installed
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
    echo "🌐 Installing Playwright browsers..."
    playwright install chromium
    echo ""
fi

echo "🚀 Starting scraper..."
echo ""

# Run the scraper
python3 vacation_scraper.py

echo ""
echo "========================================"
echo "✅ Done! Opening report..."
echo "========================================"

# Open the report (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open vacation_report.html
else
    echo "Report saved to: vacation_report.html"
    echo "Open it in your browser to view results."
fi
