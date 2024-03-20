from twilio.rest import Client
import os
import csv

# Initialize Twilio client using environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Get all phone numbers from the Twilio account
twilio_numbers = {
    num.phone_number: {
        "voice_expenses": 0, "sms_expenses": 0,
        "call_count": 0, "sms_count": 0
    }
    for num in client.incoming_phone_numbers.list()
}

# Define the date range
start_date = "2024-03-01"
end_date = "2024-03-18"

# Fetch and process voice calls
for call in client.calls.list(start_time_after=start_date, start_time_before=end_date):
    call_cost = float(call.price) if call.price else 0
    if call._from in twilio_numbers:
        twilio_numbers[call._from]["voice_expenses"] += call_cost
        twilio_numbers[call._from]["call_count"] += 1
    if call.to in twilio_numbers:
        twilio_numbers[call.to]["voice_expenses"] += call_cost
        twilio_numbers[call.to]["call_count"] += 1

# Fetch and process SMS messages
for message in client.messages.list(date_sent_after=start_date, date_sent_before=end_date):
    sms_cost = float(message.price) if message.price else 0
    if message.from_ in twilio_numbers:
        twilio_numbers[message.from_]["sms_expenses"] += sms_cost
        twilio_numbers[message.from_]["sms_count"] += 1
    if message.to in twilio_numbers:
        twilio_numbers[message.to]["sms_expenses"] += sms_cost
        twilio_numbers[message.to]["sms_count"] += 1

# Prepare the CSV output
headers = [
    'Phone Number', 'Voice Expenses ($)', 'SMS Expenses ($)',
    'Total Expenses ($)', 'Call Count', 'SMS Count', 'Total Count'
]
with open('twilio_expenses_and_counts.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    for number, details in twilio_numbers.items():
        total_expenses = details["voice_expenses"] + details["sms_expenses"]
        total_count = details["call_count"] + details["sms_count"]
        writer.writerow([
            number, details["voice_expenses"], details["sms_expenses"],
            total_expenses, details["call_count"], details["sms_count"], total_count
        ])

print("Twilio expenses and counts report generated: 'twilio_expenses_and_counts.csv'")
