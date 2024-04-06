import os
from twilio.rest import Client
import csv

# Load Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Prompt user for the Twilio phone number
twilio_phone_number = input("Enter the Twilio phone number: ").strip()

# Fetch messages sent from the provided Twilio phone number
messages = client.messages.list(from_=twilio_phone_number)

# Define the CSV file name
csv_file_name = f"{twilio_phone_number.replace('+', '')}_messages.csv"

# Write the messages to a CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Date Sent', 'To', 'Body'])

    # Write each message
    for message in messages:
        writer.writerow([message.date_sent, message.to, message.body])

print(f"Messages have been written to {csv_file_name}")
