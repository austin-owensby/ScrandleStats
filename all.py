from datetime import datetime, timedelta
import time
from utils import getMatchupsForDate, calculateRating, getHistoricalData, saveHistoricalData


START_DATE = datetime(2025, 4, 20)
today = datetime.today()

date = START_DATE

historical_data = getHistoricalData()

new_data = []

while date <= today:
    date_formatted = date.strftime("%Y-%m-%d")

    # Only get the days matchup if we don't already have it
    if date_formatted not in historical_data:
        matchup_data = getMatchupsForDate(date)
        rating = calculateRating(matchup_data)
        new_data.append((date_formatted, rating))
        print(f"Processed date {date_formatted}")

        # Rate limiting to avoid spamming the server
        time.sleep(0.5)

    date += timedelta(days=1)

if len(new_data) > 0:
    saveHistoricalData(new_data)
