import os
from datetime import datetime, timedelta
from twilio.rest import Client

# Authorization setup
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

# Define the EventType we're interested in
event_type = 'phone-number.updated'

# Calculate the time 24 hours ago from now for recent updates
twenty_four_hours_ago = datetime.utcnow() - timedelta(days=1)

# Fetch events of type 'phone-number.updated' in the last 24 hours
all_events = []
events_generator = client.monitor.v1.events.stream(
    event_type=event_type,
    start_date=twenty_four_hours_ago,
    limit=50  # This specifies the number of events per page
)

# Iterate through the generator to collect all events
for event in events_generator:
    all_events.append(event)

# Print details of each event
for event in all_events:
    print(f"Event SID: {event.sid}")
    print(f"Event Type: {event.event_type}")
    print(f"Resource SID: {event.resource_sid}")
    print(f"Event Date: {event.event_date}")
    print(f"Description: {event.event_data}")
    print("------")
