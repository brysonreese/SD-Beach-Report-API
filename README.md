# SD Beach Report API

A FastAPI backend that aggregates San Diego beach water quality data from the California Beach Watch state database.

## What it does
- Scrapes beach advisory and closure data from CA Beach Watch on a scheduled interval
- Stores historical records in a local SQLite database
- Exposes clean REST endpoints for the SD Beach Report iOS app

## Stack
- Python / FastAPI
- SQLAlchemy + SQLite
- APScheduler
- BeautifulSoup4 / Pandas

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Data source
[California Beach Watch](https://www.waterboards.ca.gov/water_issues/programs/beaches/search_beach_advisory.html)
