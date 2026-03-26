#!/bin/bash

# Greece Vacation Tracker - Quick Start Script
# Just run this file to get started!

clear

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║          🏖️  GREECE VACATION PRICE TRACKER  🏖️                   ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Starting your vacation planning assistant..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Run the tracker
python3 start_tracking.py

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                         🎉 READY TO GO! 🎉                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 For detailed instructions, see README_NEW.md"
echo ""
echo "💡 Quick Tips:"
echo "   • Run this script anytime to regenerate search links"
echo "   • Bookmark the tracker page in your browser"
echo "   • Check prices every few days for best deals"
echo ""
