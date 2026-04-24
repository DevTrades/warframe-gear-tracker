# Warframe Gear Tracker
A Python command-line application for tracking Warframe mastery progress across all gear categories.

## Features
- Track owned and mastered status for all 803 masterable items
- Automatic sync with the Warframe API to keep the item list up to date
- Fuzzy name matching for item lookups and updates
- Bulk update multiple items at once
- Category filtering and mastery progress stats
- Built-in help menu

## Requirements
- Python 3.x
- requests library (`pip install requests`)

## How to Run
1. Install Python from https://www.python.org
2. Install dependencies: `pip install requests`
3. Run the program: `python Warframe_Gear_Tracker.py`
4. Or double click `launch.bat` on Windows

## Notes
Some modular weapon components such as Zaw blades, Kitgun parts, and Amp prisms
may not be automatically detected by the API and may need to be added manually
using option 1 from the main menu.