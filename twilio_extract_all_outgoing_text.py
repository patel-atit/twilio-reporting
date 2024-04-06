from twilio.rest import Client
import os
import csv
from datetime import datetime

# Initialize Twilio client using environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Fetch all phone numbers from the Twilio account and create a set for faster lookup
twilio_numbers_set = {num.phone_number for num in client.incoming_phone_numbers.list()}

# Function to fetch and save incoming messages to a CSV file
def fetch_and_save_messages():
    # Define the CSV file name with the current date and time to avoid overwriting files
    csv_filename = f"twilio_messages_outbound_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Open a new CSV file to write
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['From', 'To', 'Date Sent', 'Message Body'])

        # Iterate over each Twilio number in the account
        for twilio_number in twilio_numbers_set:
            # Fetch messages sent to the Twilio number
            messages = client.messages.list(from_=twilio_number)
            for msg in messages:
                # Write each message's details to the CSV file
                writer.writerow([msg.from_, msg.to, msg.date_sent, msg.body])

    print(f"Messages saved to {csv_filename}")

# Execute the function to fetch and save messages
fetch_and_save_messages()
