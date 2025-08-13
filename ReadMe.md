# Scrandle Stats
Based off of the [Scrandle](https://scrandle.com/) game which has a daily matchup of 2 different football stadium foods.

This scripts allows us to determine how hard a daily matchup was by comparing the average difference in a days matchup scores to the history of existing days.

This was just a fun side project, please be respectful of the site and don't spam it. I do my best to cache data where possible to reduce network traffic.

## Requirements
[Python](https://www.python.org/) (I haven't tested a specific version, but I used the latest available at the time, 3.13.6)

And that's it, no extra pip libraries to install :)

## Running
### Individual day
1. `python today.py`

Calculates the individual day's diff and if present, the relative difficulty based on other days. This takes into account Fridays being outliers and ranks them on their own range.

### All days
1. `python all.py`

This populates missing diffs back to the start (4/20/2025) so that we can calculate a relative difficulty for an individual day

For the sake of reducing network traffic, I've checked in my latest historical_data.csv file since past data shouldn't change.