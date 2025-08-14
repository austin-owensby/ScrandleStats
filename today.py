from datetime import datetime
from utils import getScoreData, getMatchupsForDate, calculateAverageDifference, getHistoricalData, saveHistoricalData

historical_data = getHistoricalData()
date_formatted = datetime.today().strftime("%Y-%m-%d")

if date_formatted in historical_data:
    average = historical_data[date_formatted]
else:
    score_data = getScoreData()
    matchup_data = getMatchupsForDate(datetime.today())
    average = calculateAverageDifference(score_data, matchup_data)
    saveHistoricalData([(date_formatted, average)])

if len(historical_data) == 0:
    print(f"Today's Scrandle diff average is {round(average, 2)}")
else:
    is_friday = datetime.today().weekday() == 4

    # Fridays are outliers in difficulty starting on 2025-05-16
    first_difficult_friday = datetime(year=2025, month=5, day=16)
    min_value = 100
    max_value = 0
    
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
        print(f"Today's Scrandle diff average is {round(average, 2)}")
    else:
        difficulty = 10 - 10 * (average - min_value) / (max_value - min_value)
        print(f"Today's Scrandle diff average is {round(average, 2)} which makes it a relative difficulty of {round(difficulty, 2)} from 0 to 10{' (for a Friday)' if is_friday else ''}")
