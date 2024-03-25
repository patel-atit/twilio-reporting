import os
from twilio.rest import Client
from collections import defaultdict
from datetime import datetime

# Retrieve Twilio credentials from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Prepare dictionaries to hold the count of recordings and total duration per month
recordings_by_month = defaultdict(int)
duration_by_month = defaultdict(float)  # Store durations in minutes

# Fetch recordings, considering pagination
recordings = client.recordings.stream()

for recording in recordings:
    # Extract month and year from recording.date_created
    month_year = recording.date_created.strftime('%Y-%m')
    # Increment the count for this month and year
    recordings_by_month[month_year] += 1
    # Sum the duration of each recording in minutes
    if recording.duration.isdigit():
        duration_by_month[month_year] += int(recording.duration) / 60

# Print the results
for month_year in sorted(recordings_by_month):
    print(f"{month_year}: {recordings_by_month[month_year]} recordings, Total duration: {duration_by_month[month_year]:.2f} minutes")
