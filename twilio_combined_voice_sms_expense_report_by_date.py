from twilio.rest import Client
import os
import csv
from datetime import datetime

# Initialize Twilio client using environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Fetch all phone numbers from the Twilio account and create an array of these numbers
twilio_numbers_array = [num.phone_number for num in client.incoming_phone_numbers.list()]
# Convert the array into a set for faster lookup
twilio_numbers_set = set(twilio_numbers_array)

# Define the date range for March
start_date = "2024-04-03"
end_date = "2024-04-10"  # Cover the whole of March

# Initialize the structure to hold expenses grouped by date and phone number
expenses_by_date = {}

# Helper function to add or update expenses in the nested dictionary
def add_expense(date_str, phone_number, cost, is_sms, direction):
    if phone_number not in twilio_numbers_set:  # Skip if the number isn't one of yours
        return
    if date_str not in expenses_by_date:
        expenses_by_date[date_str] = {}
    if phone_number not in expenses_by_date[date_str]:
        expenses_by_date[date_str][phone_number] = {"voice_expenses": 0, "sms_expenses": 0, "call_count": 0, "sms_count": 0}
    
    expense_key = "sms_expenses" if is_sms else "voice_expenses"
    count_key = "sms_count" if is_sms else "call_count"
    
    # Add expenses and counts only if the direction is outgoing or for incoming communications to your numbers
    if direction == "outgoing" or (direction == "incoming" and phone_number in twilio_numbers_set):
        expenses_by_date[date_str][phone_number][expense_key] += cost
        expenses_by_date[date_str][phone_number][count_key] += 1

# Process voice calls
for call in client.calls.list(start_time_after=start_date, start_time_before=end_date):
    call_date_str = call.start_time.strftime('%Y-%m-%d')
    call_cost = float(call.price) if call.price else 0
    # Determine the direction based on whether the 'from' number is one of your Twilio numbers
    direction = "outgoing" if call._from in twilio_numbers_set else "incoming"
    add_expense(call_date_str, call._from, call_cost, is_sms=False, direction=direction)
    # Handle incoming calls to your numbers from outside
    if call.to in twilio_numbers_set and call._from not in twilio_numbers_set:
        add_expense(call_date_str, call.to, call_cost, is_sms=False, direction="incoming")

# Process SMS messages
for message in client.messages.list(date_sent_after=start_date, date_sent_before=end_date):
    message_date_str = message.date_sent.strftime('%Y-%m-%d')
    sms_cost = float(message.price) if message.price else 0
    direction = "outgoing" if message.from_ in twilio_numbers_set else "incoming"
    add_expense(message_date_str, message.from_, sms_cost, is_sms=True, direction=direction)
    # Handle incoming messages to your numbers from outside
    if message.to in twilio_numbers_set and message.from_ not in twilio_numbers_set:
        add_expense(message_date_str, message.to, sms_cost, is_sms=True, direction="incoming")

# Prepare the CSV output
headers = ['Date', 'Phone Number', 'Voice Expenses ($)', 'SMS Expenses ($)', 'Total Expenses ($)', 'Call Count', 'SMS Count', 'Total Count']
with open('twilio_expenses_by_date_and_number.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    
    for date, numbers in expenses_by_date.items():
        for number, details in numbers.items():
            total_expenses = details["voice_expenses"] + details["sms_expenses"]
            total_count = details["call_count"] + details["sms_count"]
            writer.writerow([
                date, number, details["voice_expenses"], details["sms_expenses"],
                total_expenses, details["call_count"], details["sms_count"], total_count
            ])

print("Twilio expenses report by date and phone number generated: 'twilio_expenses_by_date_and_number.csv'")
