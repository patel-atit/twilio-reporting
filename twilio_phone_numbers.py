from twilio.rest import Client
import os
import csv
from datetime import datetime

# Initialize Twilio client using environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Fetch all phone numbers associated with your account
phone_numbers = client.incoming_phone_numbers.list()

# Print each phone number and its friendly name
for record in phone_numbers:
    print(f"{record.friendly_name}, {record.phone_number}")

