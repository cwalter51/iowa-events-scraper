# Iowa Events Scraper 🌽

Automated scraper for Iowa events - sports, festivals, fairs, concerts, and more!

## Features

- **163+ events** across Iowa
- **34 county fairs** with real 2026 dates
- **Major venues**: TBK Bank Sports Complex, Xtream Arena, Wells Fargo Arena, Adventureland
- **Pro sports**: Iowa Heartlanders, Iowa Wild, Iowa Wolves
- **Races**: Dam to Dam, Bix 7, Turkey Trot
- **Festivals**: Hinterland, Iowa State Fair, RAGBRAI, and more
- **Auto-updates weekly** via GitHub Actions

## Output Files

| File | Description |
|------|-------------|
| `iowa_events.csv` | Spreadsheet format for Power BI/Excel |
| `iowa_events.json` | JSON format for web apps |

## Automation

This scraper runs automatically every **Monday at 6 AM Central** via GitHub Actions.

To run manually:
1. Go to **Actions** tab
2. Click **Scrape Iowa Events**
3. Click **Run workflow**

## Local Usage

```bash
python scraper_v5_comprehensive.py
```

## Power BI Integration

1. Get the raw CSV URL from GitHub:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/iowa-events-scraper/main/iowa_events.csv
   ```
2. In Power BI: **Get Data** → **Web** → Paste URL
3. Set up **Scheduled Refresh** to pull weekly updates
