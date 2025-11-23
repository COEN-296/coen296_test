import os
import base64
import smtplib
import imaplib
import email
from email.message import EmailMessage
from email.header import decode_header
import google.generativeai as genai
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Gemini Server")

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- Gmail Helpers (SMTP/IMAP) ---
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def list_emails_tool(max_results: int = 10, query: str = None):
    """List recent emails from the inbox."""
    if not GMAIL_USER or not GMAIL_PASSWORD: return "Error: GMAIL_USER or GMAIL_PASSWORD not set."
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        if status != "OK": return "No messages found."
        
        email_ids = messages[0].split()
        if not email_ids: return "No messages found."
        
        latest_email_ids = email_ids[-max_results:] # Get last N messages
        
        output = []
        for e_id in reversed(latest_email_ids): # Newest first
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
                            except:
                                subject = str(msg["Subject"])
                        
                        sender = msg.get("From", "(unknown)")
                        output.append(f"ID: {e_id.decode()} | From: {sender} | Subject: {subject}")
            except Exception as e:
                output.append(f"ID: {e_id.decode()} | Error: Could not parse email")
        
        mail.logout()
        return "\n".join(output) if output else "No emails found."
    except Exception as e: return f"Error: {e}"

def read_email_tool(message_id: str):
    """Read full content of an email by ID."""
    if not GMAIL_USER or not GMAIL_PASSWORD: return "Error: GMAIL_USER or GMAIL_PASSWORD not set."

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASSWORD)
        mail.select("inbox")
        
        _, msg_data = mail.fetch(message_id.encode(), "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break # Just get the first text part
        else:
            body = msg.get_payload(decode=True).decode()
            
        mail.logout()
        return f"Subject: {msg['Subject']}\nFrom: {msg['From']}\n\nBody:\n{body}"
    except Exception as e: return f"Error: {e}"

def send_email_tool(to: str, subject: str, body: str):
    """Send an email."""
    if not GMAIL_USER or not GMAIL_PASSWORD: return "Error: GMAIL_USER or GMAIL_PASSWORD not set."

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)
            
        return "Email sent successfully!"
    except Exception as e: return f"Error: {e}"

# Map of tool names to functions for execution
tools_map = {
    'list_emails': list_emails_tool,
    'read_email': read_email_tool,
    'send_email': send_email_tool
}

@mcp.tool()
def agent_action(request: str) -> str:
    """
    Ask the AI Agent to perform an action (e.g., "Check my emails", "Send an email to X").
    The Agent has access to Gmail tools and will use them to fulfill the request.
    
    Args:
        request: The user's natural language request.
    """
    if not API_KEY: return "Error: GEMINI_API_KEY not set."

    # 1. Initialize Model with Tools
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools=[list_emails_tool, read_email_tool, send_email_tool]
    )
    
    # 2. Start Chat Session
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    try:
        # 3. Send message to model (it will auto-call tools if needed)
        response = chat.send_message(request)
        return response.text
    except Exception as e:
        return f"Agent Error: {str(e)}"

@mcp.tool()
def ask_gemini(prompt: str) -> str:
    """Ask Gemini a general question (no tools)."""
    if not API_KEY: return "Error: GEMINI_API_KEY not set."
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"Error: {e}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
