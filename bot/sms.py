from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

# Create a Twilio client object
client = Client(account_sid, auth_token)

# Send an SMS message


def send_sms(to_number, message):
    client.messages.create(
        to=to_number,
        from_='<YOUR_TWILIO_PHONE_NUMBER>',
        body=message
    )
