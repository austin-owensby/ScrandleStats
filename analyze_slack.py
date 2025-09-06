from datetime import datetime

with open("slack.csv") as f:
    lines = f.readlines()

dates: dict[str, list[int]] = {}

# Loop over our results from Slack and group them by date
for line in lines:
    parts = line.split(",")

    # Parse the Unix timestamp into a local date
    date = datetime.fromtimestamp(float(parts[0])).strftime("%Y-%m-%d")

    if date not in dates:
        dates[date] = []

    score = int(parts[1])

    # Add this score to the list of scores for this date
    dates[date] = dates[date] + [score]

# Now get an average for each date from Slack
for date in dates:
    average = sum(dates[date]) / len(dates[date])

    # This could be more efficient with a single write instead of on each loop, but it's a one off short running script so I'm not worrying about it
    with open("slack-averages.csv", "a") as f:
        f.write(f"{date},{average}\n")
