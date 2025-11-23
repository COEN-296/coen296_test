import os
import imaplib
import smtplib
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

print("🔍 Checking credentials...")
print(f"GMAIL_USER: {GMAIL_USER if GMAIL_USER else '❌ NOT SET'}")
print(f"GMAIL_PASSWORD: {'✅ SET' if GMAIL_PASSWORD else '❌ NOT SET'}")

if not GMAIL_USER or not GMAIL_PASSWORD:
    print("\n❌ Please add GMAIL_USER and GMAIL_PASSWORD to your .env file")
    exit(1)

print("\n📧 Testing IMAP connection (reading emails)...")
try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    email_count = len(messages[0].split()) if messages[0] else 0
    mail.logout()
    print(f"✅ IMAP connection successful! Found {email_count} emails in inbox.")
except Exception as e:
    print(f"❌ IMAP connection failed: {e}")

print("\n📤 Testing SMTP connection (sending emails)...")
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASSWORD)
    print("✅ SMTP connection successful!")
except Exception as e:
    print(f"❌ SMTP connection failed: {e}")

print("\n✅ All connection tests complete!")
