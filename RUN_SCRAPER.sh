#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
#  Greece Vacation Scraper — manual run
#  Runs daily_scraper.py, then opens vacation_tracker.html in the browser.
# ─────────────────────────────────────────────────────────────────────────────

DIR="$(cd "$(dirname "$0")" && pwd)"

clear
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          🏖️  GREECE VACATION SCRAPER — MANUAL RUN  🏖️             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Script: ${DIR}/daily_scraper.py"
echo "Output: ${DIR}/tracker_data.js"
echo ""
read -p "Press ENTER to start (takes ~5–10 minutes)…"
echo ""

"${DIR}/.venv/bin/python" "${DIR}/daily_scraper.py"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                        ✅ SCRAPE DONE! ✅                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Opening index.html…"
open "${DIR}/index.html"

