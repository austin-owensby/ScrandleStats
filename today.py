from datetime import datetime
import math
from utils import getScoreData, getMatchupsForDate, calculateRating, getHistoricalData, saveHistoricalData

historical_data = getHistoricalData()
date_formatted = datetime.today().strftime("%Y-%m-%d")

if date_formatted in historical_data:
    rating = historical_data[date_formatted]
else:
    score_data = getScoreData()
    matchup_data = getMatchupsForDate(datetime.today())
    rating = calculateRating(score_data, matchup_data)
    saveHistoricalData([(date_formatted, rating)])

if len(historical_data) == 0:
    print("Unable to calculate a relative difficulty")
else:
    is_friday = datetime.today().weekday() == 4

    # Fridays are outliers in difficulty starting on 2025-05-16
    first_difficult_friday = datetime(year=2025, month=5, day=16)
    min_value = rating
    max_value = rating
    
    for historical_data_point in historical_data:
        date = datetime.strptime(historical_data_point, "%Y-%m-%d")
        value = historical_data[historical_data_point]

        if is_friday and date >= first_difficult_friday and date.weekday() == 4:
            # Do calculations based on these outlier Friday values
            if value < min_value:
                min_value = value
            
            if value > max_value:
                max_value = value
        elif not is_friday and (date < first_difficult_friday or date.weekday() != 4):
            # Do calculations on a normal day
            if value < min_value:
                min_value = value
            
            if value > max_value:
                max_value = value

    if min_value == max_value:
        print("Unable to calculate a relative difficulty")
    else:
        difficulty = 10 * (rating - min_value) / (max_value - min_value)
        difficulty_description = "That's "

        if difficulty < 2.0:
            difficulty_description += "pretty easy."
        elif difficulty < 4.0:
            difficulty_description += "an easy one."
        elif difficulty < 6.0:
            difficulty_description += "especially average."
        elif difficulty < 8.0:
            difficulty_description += "a little tricky."
        else:
            difficulty_description += "a tough one!"

        # Based on historical Slack data + a trend line with an R^2 of 0.702, predict what people will score
        prediction = 62.1 * (rating ** -0.87)
        
        print(f"Today's Scrandle is a relative difficulty of {round(difficulty, 2)} from 0 to 10. {difficulty_description}{' (for a Friday)' if is_friday else ''}. :crystal_ball: I predict you will have score around {math.floor(prediction)} or {math.ceil(prediction)}.")
