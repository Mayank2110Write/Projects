from flask import Flask, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
from email.utils import parsedate_to_datetime
import base64
import re
import pickle
import os

# Initialize Flask app
app = Flask(__name__)

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('E:\MAYANK IITJ\Data Science\Email assistant project\client_secret_172294059513-hoj8g1ougfn5lo651q5bnnp4dkbf2lq4.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_console()
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

# Load the pre-trained summarization model
with open('model.pkl', 'rb') as file:
    summarize_email = pickle.load(file)

# Helper function to clean email body
def clean_email_body(body):
    body = re.sub(r'<[^>]+>', '', body)  # Remove HTML tags
    body = body.replace('\n', ' ').strip()  # Normalize newlines and strip spaces
    return body

# Helper function to fetch emails received today
def fetch_emails_for_today():
    results = service.users().messages().list(userId='me', maxResults=100).execute()
    messages = results.get('messages', [])
    emails = []
    today = datetime.utcnow().date()

    for msg in messages:
        try:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg_data['payload']
            headers = payload.get('headers', [])
            subject, sender, date = '', '', ''

            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'From':
                    sender = header['value']
                if header['name'] == 'Date':
                    date = header['value']

            email_date = parsedate_to_datetime(date).date()

            if email_date == today:
                body = ''
                parts = payload.get('parts', [])
                if parts:
                    for part in parts:
                        if part.get('mimeType') == 'text/plain':
                            data = part['body']['data']
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                            break
                        elif part.get('mimeType') == 'text/html':
                            data = part['body']['data']
                            body = base64.urlsafe_b64decode(data).decode('utf-8')
                elif 'body' in payload and 'data' in payload['body']:
                    body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

                body = clean_email_body(body)
                if body.strip():
                    emails.append({'subject': subject, 'sender': sender, 'body': body})
        except Exception as e:
            print(f"Error processing email: {e}")
    return emails

@app.route('/fetch_emails', methods=['GET'])
def fetch_emails():
    try:
        emails = fetch_emails_for_today()
        processed_emails = []

        for email in emails:
            summary = summarize_email(email['body'])
            processed_emails.append({
                'subject': email['subject'],
                'sender': email['sender'],
                'summary': summary
            })

        return jsonify(processed_emails)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
