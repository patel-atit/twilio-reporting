from twilio.rest import Client
from collections import defaultdict
import os

# Retrieve Twilio credentials from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_ACCOUNT_TOKEN')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Prepare dictionaries to hold the count of recordings and total duration per month and phone number
recordings_by_month = defaultdict(lambda: defaultdict(int))
duration_by_month = defaultdict(lambda: defaultdict(float))  # Store durations in minutes

# Fetch recordings, considering pagination
recordings = client.recordings.stream()

for recording in recordings:
    try:
        # Extract month and year from recording.date_created
        month_year = recording.date_created.strftime('%Y-%m')
        # Retrieve the call using the call_sid associated with the recording
        call = client.calls(recording.call_sid).fetch()
        # Extract receiving phone number from the call
        phone_number = call.to
        # Increment the count for this month, year, and phone number
        recordings_by_month[month_year][phone_number] += 1
        # Calculate the duration rounded up to the nearest minute
        if recording.duration.isdigit():
            raw_duration = int(recording.duration)
            adjusted_duration = (raw_duration + 59) // 60  # Rounds up to next minute
            duration_by_month[month_year][phone_number] += adjusted_duration
    except Exception as e:
        # If an error occurs, skip this recording and continue with the next
        print(f"Skipping a recording due to an error: {e}")

# Print the results formatted with month-year as a header
for month_year in sorted(recordings_by_month.keys()):
    print(f"{month_year}:")
    for phone_number in recordings_by_month[month_year]:
        num_recordings = recordings_by_month[month_year][phone_number]
        total_duration = duration_by_month[month_year][phone_number]
        print(f"    {phone_number}: {num_recordings} recordings, Total duration: {total_duration:.2f} minutes")
