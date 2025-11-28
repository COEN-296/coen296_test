import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

print(f"Testing with: {GMAIL_USER}")

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    print(f"Search status: {status}")
    
    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} emails")
    
    latest_email_ids = email_ids[-5:]  # Get last 5
    
    for e_id in reversed(latest_email_ids):
        print(f"\nProcessing email ID: {e_id.decode()}")
        try:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Safely decode subject
                    subject = "(no subject)"
                    if msg["Subject"]:
                        try:
                            decoded = decode_header(msg["Subject"])[0]
                            if isinstance(decoded[0], bytes):
                                subject = decoded[0].decode(decoded[1] if decoded[1] else "utf-8")
                            else:
                                subject = decoded[0]
                        except Exception as e:
                            print(f"  Subject decode error: {e}")
                            subject = str(msg["Subject"])
                    
                    sender = msg.get("From", "(unknown)")
                    print(f"  From: {sender}")
                    print(f"  Subject: {subject}")
        except Exception as e:
            print(f"  Error processing email: {e}")
    
    mail.logout()
    print("\n✅ Test complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
