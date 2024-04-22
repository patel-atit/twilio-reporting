import os
import csv
from twilio.rest import Client
from collections import defaultdict
from datetime import datetime, timezone

# Retrieve Twilio credentials from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Prepare dictionaries to hold the count of recordings and total duration per month
recordings_by_month = defaultdict(int)
duration_by_month = defaultdict(float)  # Store durations in minutes
recordings_info_before_2024 = []  # List to store recording IDs and dates for calls before Jan 1, 2024

# Fetch recordings, considering pagination
recordings = client.recordings.stream()

for recording in recordings:
    # Extract month and year from recording.date_created
    month_year = recording.date_created.strftime('%Y-%m')
    # Check if recording is before Jan 1, 2024, adjusting for timezone
    if recording.date_created < datetime(2024, 1, 1, tzinfo=timezone.utc):
        recordings_info_before_2024.append((recording.sid, recording.date_created))
    # Increment the count for this month and year
    recordings_by_month[month_year] += 1
    # Calculate the duration rounded up to the nearest minute
    if recording.duration.isdigit():
        raw_duration = int(recording.duration)
        adjusted_duration = (raw_duration + 59) // 60  # Rounds up to next minute
        duration_by_month[month_year] += adjusted_duration

# Writing to CSV
csv_file_path = 'recordings_before_2024.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Recording ID', 'Date Created'])
    # Write the recording details
    for recording_id, recording_date in recordings_info_before_2024:
        writer.writerow([recording_id, recording_date.strftime('%Y-%m-%d %H:%M:%S')])

# Print the results
for month_year in sorted(recordings_by_month):
    print(f"{month_year}: {recordings_by_month[month_year]} recordings, Total duration: {duration_by_month[month_year]:.2f} minutes")

print(f"Recording IDs and dates for calls before Jan 1, 2024 have been saved to {csv_file_path}")
