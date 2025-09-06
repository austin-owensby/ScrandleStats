from datetime import datetime
from http.client import HTTPResponse
import json
import os
import re
import urllib.request

BASE_URL = "https://scrandle.com/"
HEADERS = {
    "User-Agent": "python (+via https://github.com/austin-owensby/ScrandleStats by austin_owensby@hotmail.com)"
}

def getScoreData():
    """Get the data for each scran"""
    # First, check the javascript url from Scrandle in case a new version was deployed with more data
    request = urllib.request.Request(BASE_URL, headers=HEADERS)
    response: HTTPResponse

    with urllib.request.urlopen(request) as response:
        response_string = response.read().decode()
        javascript_url: str = re.search("src=\"(bundle\\.\\w+\\.js)\"", response_string).group(1)

    # Next, check if we've already cached this javascript file to prevent spamming the server
    folder = "javascript"
    file_path = f"{folder}/{javascript_url}"

    folder_exists = os.path.isdir(folder)
    if not folder_exists:
        os.mkdir(folder)

    file_exists = os.path.isfile(file_path)

    content: str

    if file_exists:
        with open(file_path) as f:
            content = f.read()
    else:
        # Delete the old file
        for filename in os.listdir(folder):
            os.remove(f"{folder}/{filename}")

        request = urllib.request.Request(BASE_URL + javascript_url, headers=HEADERS)
        with urllib.request.urlopen(request) as response:
            response_string = response.read().decode()
            content: str = re.search("JSON\\.parse\\('(.+)'\\)", response_string).group(1)

            # Save the file for reuse
            with open(file_path, "x") as f:
                f.write(content)

    # Next parse the JSON data from the javascript
    # Fix some escaped characters that don't play well with python's JSON parser
    content = content.replace("\\\\\"", "'")
    content = content.replace("\\'", "'")

    score_data: list[dict] = json.loads(content)

    return score_data

def getMatchupsForDate(date: datetime):
    """For a given date, get the scran matchups"""
    date_formatted = date.strftime("%Y-%m-%d")
    request = urllib.request.Request(f"{BASE_URL}/games/{date_formatted}.json", headers=HEADERS)
    with urllib.request.urlopen(request) as response:
        response_string = response.read().decode()
        matchup_data: list[list[str]] = json.loads(response_string)

    return matchup_data

def calculateRating(score_data: list[dict], matchup_data: list[list[str]]):
    """Given the score data for all scrans and the daily matchup, calculate a rating based on weighted matchups"""
    # 1. Collect a list of unique scran ids
    unique_scans = []

    for matchup in matchup_data:
        if matchup[0] not in unique_scans:
            unique_scans.append(matchup[0])
        if matchup[1] not in unique_scans:
            unique_scans.append(matchup[1])

    # 2. Find the matchup data for the scrans
    matchup_score_data = {}
    for score in score_data:
        # Check if we've found all our match ups
        if len(unique_scans) == len(matchup_score_data):
            break

        # If we find a match, record it
        if score["id"] in unique_scans:
            matchup_score_data[score["id"]] = score["rating"]

    # 3. Tally score based on differences
    ratings = []

    for matchup in matchup_data:
        diff = abs(matchup_score_data[matchup[0]] - matchup_score_data[matchup[1]])

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
