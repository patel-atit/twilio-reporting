import os
from twilio.rest import Client
from datetime import datetime, timedelta
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content,To, From

# Environment variables for Twilio and SendGrid
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')

# Initialize Twilio and SendGrid clients
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
sendgrid_client = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

def get_date_range(period):
    today = datetime.utcnow()
    if period == 'lastWeek':
        last_sunday = today - timedelta(days=today.weekday() + 1)
        last_monday = last_sunday - timedelta(days=6)
        start_date = last_monday
        end_date = last_sunday
    elif period == 'lastMonth':
        first_day_of_this_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        start_date = first_day_of_last_month
        end_date = last_day_of_last_month
    elif period == 'yearToDate':
        start_date = datetime(today.year, 1, 1)
        end_date = today
    else:
        raise ValueError('Invalid period specified')
    return start_date, end_date

def fetch_phone_numbers():
    phone_numbers = twilio_client.incoming_phone_numbers.list()
    return {pn.phone_number: pn.friendly_name for pn in phone_numbers}

def fetch_call_logs(start_date, end_date):
    calls = twilio_client.calls.list(
        start_time_after=start_date,
        start_time_before=end_date,
        limit=1000
    )
    return calls

def fetch_message_logs(start_date, end_date):
    messages = twilio_client.messages.list(
        date_sent_after=start_date,
        date_sent_before=end_date,
        limit=1000
    )
    return messages

def aggregate_stats(phone_numbers, calls, messages):
    phone_number_stats = {pn: {
        'friendly_name': phone_numbers[pn],
        'incoming_calls_count': 0,
        'incoming_calls_minutes': 0,
        'outgoing_calls_count': 0,
        'outgoing_calls_minutes': 0,
        'incoming_sms_count': 0,
        'outgoing_sms_count': 0,
        'incoming_mms_count': 0,
        'outgoing_mms_count': 0
    } for pn in phone_numbers}

    for call in calls:
        if call.to in phone_number_stats:
            phone_number_stats[call.to]['incoming_calls_count'] += 1
            phone_number_stats[call.to]['incoming_calls_minutes'] += int(call.duration or 0)
        if call._from in phone_number_stats:
            phone_number_stats[call._from]['outgoing_calls_count'] += 1
            phone_number_stats[call._from]['outgoing_calls_minutes'] += int(call.duration or 0)
    
    for message in messages:
        if message.to in phone_number_stats:
            if int(message.num_media) > 0:
                phone_number_stats[message.to]['incoming_mms_count'] += 1
            else:
                phone_number_stats[message.to]['incoming_sms_count'] += 1
        if message.from_ in phone_number_stats:
            if int(message.num_media) > 0:
                phone_number_stats[message.from_]['outgoing_mms_count'] += 1
            else:
                phone_number_stats[message.from_]['outgoing_sms_count'] += 1
    
    return phone_number_stats

def create_html_table(stats, period, start_date, end_date):
    html = f"<h3>Twilio Phone Number Statistics ({period} - {start_date} to {end_date})</h3>"
    html += '<table border="1" cellpadding="5" cellspacing="0">'
    html += '<tr><th>Phone Number</th><th>Friendly Name</th><th>Incoming Calls</th><th>Incoming Call Minutes</th><th>Outgoing Calls</th><th>Outgoing Call Minutes</th><th>Incoming SMS</th><th>Outgoing SMS</th><th>Incoming MMS</th><th>Outgoing MMS</th></tr>'
    
    for pn, data in stats.items():
        html += f"<tr><td>{pn}</td><td>{data['friendly_name']}</td><td>{data['incoming_calls_count']}</td><td>{data['incoming_calls_minutes']}</td><td>{data['outgoing_calls_count']}</td><td>{data['outgoing_calls_minutes']}</td><td>{data['incoming_sms_count']}</td><td>{data['outgoing_sms_count']}</td><td>{data['incoming_mms_count']}</td><td>{data['outgoing_mms_count']}</td></tr>"
    
    html += '</table>'
    return html

def send_email(html_content, period, start_date, end_date):
    subject = f"Twilio Usage Report: {period} ({start_date} to {end_date})"
    from_email = From(EMAIL_RECIPIENT)
    to_email = To(EMAIL_RECIPIENT)
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)
    response = sendgrid_client.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

def fetch_twilio_statistics(period):
    start_date, end_date = get_date_range(period)
    phone_numbers = fetch_phone_numbers()
    calls = fetch_call_logs(start_date, end_date)
    messages = fetch_message_logs(start_date, end_date)
    stats = aggregate_stats(phone_numbers, calls, messages)
    html_table = create_html_table(stats, period, start_date, end_date)
    send_email(html_table, period, start_date, end_date)

# Example usage:
fetch_twilio_statistics('lastWeek')
# fetch_twilio_statistics('lastMonth')
# fetch_twilio_statistics('yearToDate')
