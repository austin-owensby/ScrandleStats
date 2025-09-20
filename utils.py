from datetime import datetime
import json
import os
import urllib.request

BASE_URL = "https://scrandle.com/"
HEADERS = {
    "User-Agent": "python (+via https://github.com/austin-owensby/ScrandleStats by austin_owensby@hotmail.com)"
}

def getMatchupsForDate(date: datetime):
    """For a given date, get the scran matchups"""
    date_formatted = date.strftime("%Y-%m-%d")
    request = urllib.request.Request(f"{BASE_URL}history/{date_formatted}", headers=HEADERS)
    with urllib.request.urlopen(request) as response:
        response_string = response.read().decode()
        matchup_data: list[list[any]] = json.loads(response_string)["data"]

    return matchup_data

def calculateRating(matchup_data: list[list[any]]):
    """Given the score data for all scrans and the daily matchup, calculate a rating based on weighted matchups"""

    ratings = []

    for matchup in matchup_data:
        diff = abs(matchup[0]["rating"] - matchup[1]["rating"])

        # Any adjustments to these variable should result in deleting the old `historical_data.csv` file
        #   and rerunning the `all.py` script
        max_possible_diff = 100
        average_diff = 28
        power = 2

        # This is based off of a parabola where a diff of 100 has a modifier of 0
        #   and an average diff of 28 has a modifier of 1.
        #   This means that smaller diffs have a higher modifier
        # If this does not weigh harder problems enough, we can increase the power
        rating_item = ((max_possible_diff - diff) / (max_possible_diff - average_diff)) ** power
        ratings.append(rating_item)

    rating = sum(ratings)

    return rating

def getHistoricalData():
    """Gets a dictionary of cached historical data"""
    historical_data: dict[str, float] = {}

    file_path = "historical_data.csv"
    file_exists = os.path.isfile(file_path)

    if file_exists:
        with open(file_path) as f:
            content = f.read()
            historical_data = { line.split(",")[0] : float(line.split(",")[1]) for line in content.splitlines() }

    return historical_data

def saveHistoricalData(data: list[tuple[str, float]]):
    """Saves new historical data to the cache"""
    file_path = "historical_data.csv"

    with open(file_path, "a") as f:
        for line in data:
            print(f"{line[0]},{line[1]}", file=f)
