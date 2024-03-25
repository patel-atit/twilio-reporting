import os
from twilio.rest import Client
import numpy as np

# Retrieve Twilio credentials from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Fetch and iterate over recordings to collect their lengths
recordings = client.recordings.list(limit=1000)  # Adjust the limit as needed
lengths = [int(recording.duration) for recording in recordings if recording.duration.isdigit()]

# Calculate average, P85, and P95 of recording lengths
average_length = np.mean(lengths)
p85_length = np.percentile(lengths, 85)
p95_length = np.percentile(lengths, 95)

print(f"Average recording length: {average_length} seconds")
print(f"85th percentile of recording length: {p85_length} seconds")
print(f"95th percentile of recording length: {p95_length} seconds")
