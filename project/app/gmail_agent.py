import os.path
import base64
from email.message import EmailMessage
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Gmail Agent")

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json not found. Please download it from Google Cloud Console.")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

@mcp.tool()
def list_emails(max_results: int = 10, query: str = None) -> str:
    """
    List emails from the user's mailbox.
    
    Args:
        max_results: Maximum number of emails to return (default 10).
        query: Gmail search query (e.g., 'is:unread', 'from:boss@example.com').
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', maxResults=max_results, q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            return "No messages found."

        output = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(no subject)')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '(unknown)')
            output.append(f"ID: {message['id']} | From: {sender} | Subject: {subject}")
        
        return "\n".join(output)

    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def read_email(message_id: str) -> str:
    """
    Read the full content of a specific email.
    
    Args:
        message_id: The ID of the email to read (from list_emails).
    """
    try:
        service = get_gmail_service()
        msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        
        # Extract body
        payload = msg['payload']
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode()
        elif 'body' in payload:
             data = payload['body'].get('data')
             if data:
                 body = base64.urlsafe_b64decode(data).decode()
        
        headers = payload['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(no subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(unknown)')
        
        return f"From: {sender}\nSubject: {subject}\n\nBody:\n{body}"

    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email.
    
    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Email body content.
    """
    try:
        service = get_gmail_service()
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['From'] = 'me' # Special value for authenticated user
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}
        
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        return f"Email sent successfully! Message Id: {send_message['id']}"

    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def create_label(label_name: str) -> str:
    """
    Create a new label in Gmail.
    
    Args:
        label_name: The name of the new label.
    """
    try:
        service = get_gmail_service()
        label = {'name': label_name}
        created_label = service.users().labels().create(userId='me', body=label).execute()
        return f"Label created: {created_label['id']} ({created_label['name']})"
    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def apply_label(message_id: str, label_id: str) -> str:
    """
    Apply a label to an email.
    
    Args:
        message_id: The ID of the email.
        label_id: The ID of the label to apply (or the name if it's a system label like 'INBOX').
    """
    try:
        service = get_gmail_service()
        # First, we might need to look up the label ID if a name was passed, 
        # but for simplicity we assume the user might pass the ID or we try to use it directly.
        # Ideally, we would list labels to find the ID from the name.
        
        # Simple lookup for common system labels if user passes names
        if label_id.upper() in ['INBOX', 'SPAM', 'TRASH', 'UNREAD', 'STARRED']:
            label_id = label_id.upper()

        body = {'addLabelIds': [label_id]}
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        return f"Label '{label_id}' applied to message {message_id}"
    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
