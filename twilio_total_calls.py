import os
from twilio.rest import Client

# Retrieve Twilio credentials from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Initialize a variable to hold the count of calls
total_calls = 0

# Fetch and iterate over calls in pages to manage memory for large datasets
for calls in client.calls.stream(page_size=100):  # Adjust page_size as needed
    total_calls += 1

print(f"Total number of calls in the account: {total_calls}")
