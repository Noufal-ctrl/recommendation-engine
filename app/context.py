from datetime import datetime

def get_context():
    now = datetime.now()
    hour = now.hour
    month = now.month

    if 5 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    elif 17 <= hour < 21:
        time_of_day = "evening"
    else:
        time_of_day = "night"

    if month in (12, 1, 2):
        season = "winter"
    elif month in (3, 4, 5):
        season = "summer"
    elif month in (6, 7, 8, 9):
        season = "monsoon"
    else:
        season = "autumn"

    return {"time_of_day": time_of_day, "season": season}


SEASON_BOOST = {
    "winter": ["Thermal Base Layer", "Sleeping Bag"],
    "summer": ["Insulated Water Bottle", "Trail Running Shoes"],
    "monsoon": ["Rain Jacket", "Pro Hiking Boots"],
    "autumn": ["Camping Backpack", "Fitness Tracker Watch"],
}