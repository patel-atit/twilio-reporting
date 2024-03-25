import os
from datetime import datetime, timedelta
from twilio.rest import Client

# Initialize Twilio client using environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Calculate the date range for the last 30 days
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=30)


# Format dates in 'YYYY-MM-DD' format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Original list of categories provided
original_categories = [
    "agent-conference", "answering-machine-detection", "amazon-polly",
    "calls", "calls-inbound", "calls-inbound-local", "calls-inbound-mobile",
    "calls-inbound-tollfree", "calls-outbound", "calls-sip", "calls-sip-inbound",
    "calls-sip-outbound", "calls-client", "calls-globalconference", "calls-media-stream-minutes",
    "calls-pay-verb-transactions", "call-progess-events", "calls-recordings",
    "programmablevoice-platform", "programmablevoiceconnectivity", "programmablevoiceconn-sip",
    "programmablevoiceconn-sip-inbound", "programmablevoiceconn-sip-outbound",
    "programmablevoiceconn-clientsdk", "pstnconnectivity", "pstnconnectivity-inbound",
    "pstnconnectivity-outbound", "recordings", "recordingstorage", "speech-recognition",
    "transcriptions", "tts-google", "virtual-agent", "voice-intelligence",
    "voice-intelligence-transcription", "voice-intelligence-operators", "voice-insights",
    "voice-insights-ptsn-insights-on-demand-minute", "voice-insights-sip-trunking-insights-on-demand-minute",
    "a2p-registration-fees", "sms", "sms-inbound", "sms-inbound-longcode", "sms-inbound-shortcode",
    "sms-outbound", "sms-outbound-longcode", "sms-outbound-shortcode", "sms-messages-carrierfees",
    "mms", "mms-inbound", "mms-inbound-longcode", "mms-inbound-shortcode", "mms-outbound",
    "mms-outbound-longcode", "mms-outbound-shortcode", "mms-messages-carrierfees", "mediastorage",
    # New categories added
    "pfax-minutes", "pfax-pages", "phonenumbers"
]

# Remove duplicates
categories = list(set(original_categories))

# Initialize a dictionary to hold total costs for each category
category_costs = {category: 0 for category in categories}

# Fetch and process usage for each category
for category in categories:
    usage_records = client.usage.records.list(category=category, start_date=start_date_str, end_date=end_date_str)
    for record in usage_records:
        category_costs[category] += float(record.price)

# Print detailed analysis
print(f"Detailed charges analysis over the last 30 days (from {start_date_str} to {end_date_str}):")
for category, cost in category_costs.items():
    if cost > 0:  # Print only categories with costs
        print(f"{category.replace('_', ' ').title()}: ${cost:.2f}")
