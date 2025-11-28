"""
Simple demo of the Gmail Agent capabilities.
This directly calls the email functions to show they work.
"""
import os
from dotenv import load_dotenv
load_dotenv()

# Import the functions from gemini_mcp
import sys
sys.path.insert(0, 'app')
from gemini_mcp import list_emails_tool, send_email_tool, read_email_tool

print("=" * 60)
print("Gmail Agent Demo")
print("=" * 60)

# Test 1: List emails
print("\n📧 Test 1: Listing your emails...")
result = list_emails_tool(max_results=5)
print(result)

# Test 2: Send email
print("\n" + "=" * 60)
print("📤 Test 2: Sending a test email to yourself...")
gmail_user = os.getenv("GMAIL_USER")
if gmail_user:
    result = send_email_tool(
        to=gmail_user,
        subject="Direct Test from Gmail Agent",
        body="This email was sent directly from the Gmail Agent functions!"
    )
    print(result)
else:
    print("⚠️ GMAIL_USER not set")

print("\n" + "=" * 60)
print("✅ Demo complete!")
print("=" * 60)
