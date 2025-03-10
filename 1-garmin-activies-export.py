import os
import json
import logging
import pandas as pd
from garminconnect import Garmin
from datetime import datetime
import sys

# Configure logging to output to stdout
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

# Garmin credentials
EMAIL = os.getenv("GARMIN_EMAIL")
PASSWORD = os.getenv("GARMIN_PASSWORD")
NUM_ACTIVITIES_EXTRACT = os.getenv("NUM_ACTIVITIES_EXTRACT")
logging.info(f"EMAIL: {EMAIL}")
logging.info(f"NUM_ACTIVITIES_EXTRACT: {NUM_ACTIVITIES_EXTRACT}")

current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
logging.info(f"current_datetime: {current_datetime}")

OUTPUT_FILE = f"data/garmin_activities_{current_datetime}.csv"

# Authenticate Garmin
try:
    client = Garmin(EMAIL, PASSWORD)
    client.login()
    logging.info("Logged in successfully!")
except Exception as e:
    logging.error("Login failed:", e)
    exit()

# Fetch last 30 activities (change as needed)
try:
    activities = client.get_activities(0, NUM_ACTIVITIES_EXTRACT)
    logging.info(f"Retrieved {len(activities)} activities")
except Exception as e:
    logging.error("Error fetching activities:", e)
    exit()

# Process data
workouts = []
for activity in activities:
    activity_type = activity["activityType"]["typeKey"]
    if activity_type in ["treadmill_running", "running", "virtual_ride", "road_biking"]:
        workouts.append({
            "Activity ID": activity["activityId"],
            "Date": datetime.strptime(activity["startTimeLocal"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
            "Start Time": activity["startTimeLocal"],
            "Activity Type": activity_type,
            "Distance (km)": activity.get("distance", 0) / 1000,  # Convert meters to kilometers
            "Distance (mi)": activity.get("distance", 0) * 0.000621371,  # Convert meters to miles
            "Duration (min)": activity.get("duration", 0) / 60,  # Convert seconds to minutes
            "Calories": activity.get("calories", 0),
            "Avg HR": activity.get("averageHR", "N/A"),
            "Max HR": activity.get("maxHR", "N/A"),
            "Avg Pace (min/km)": (activity.get("duration", 0) / 60) / (activity.get("distance", 1) / 1000) if activity.get("distance", 0) else "N/A",
            "Avg Pace (min/mi)": (activity.get("duration", 0) / 60) / (activity.get("distance", 1) * 0.000621371) if activity.get("distance", 0) else "N/A",
            "HR Time in Zone 1 (min)": activity.get("hrTimeInZone_1", 0) / 60,
            "HR Time in Zone 2 (min)": activity.get("hrTimeInZone_2", 0) / 60,
            "HR Time in Zone 3 (min)": activity.get("hrTimeInZone_3", 0) / 60,
            "HR Time in Zone 4 (min)": activity.get("hrTimeInZone_4", 0) / 60,
            "HR Time in Zone 5 (min)": activity.get("hrTimeInZone_5", 0) / 60,
        })

# Convert to DataFrame
df = pd.DataFrame(workouts)

# Save to CSV
df.to_csv(OUTPUT_FILE, index=False)

logging.info(f"Workout history saved to '{OUTPUT_FILE}'")
