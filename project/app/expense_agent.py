# This script uses an LLM to automate expense validation:
# 1. Accepts two PDF files as input:
#    - receipt.pdf: contains itemized expenses
#    - policy.pdf: contains the company’s expense policy rules
# 2. The LLM reads and interprets both documents.
# 3. It compares each expense in receipts.pdf against the rules in policy.pdf.
# 4. The output is a decision for each expense (Approved / Not Approved)

# --> Do this before running: pip install google-generativeai

import os
import fitz  # PyMuPDF
import google.generativeai as genai
from datetime import datetime

# Configure API key (UPDATE IT)
genai.configure(api_key="") 

directory = os.getcwd()
receipt_path = os.path.join(directory, "receipt.pdf")
policy_path = os.path.join(directory, "policy.pdf")

def read_pdf_text(pdf_path):
    """Extract all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Read both PDFs
receipt_text = read_pdf_text(receipt_path)
policy_text = read_pdf_text(policy_path)

# Step 1: Ask Gemini to extract the receipt date
date_prompt = f"""
Extract only the receipt date from the following text.
Return the date in ISO format (YYYY-MM-DD) if possible.
If no date is found, reply with 'UNKNOWN'.

Receipt text:
{receipt_text}
"""

model = genai.GenerativeModel("gemini-2.0-flash")
date_response = model.generate_content(date_prompt)
receipt_date_str = date_response.text.strip()

# Step 2: Compute days since policy if date is valid
policy_date = datetime.now()
days_since_policy = None
receipt_date = None

try:
    if receipt_date_str != "UNKNOWN":
        receipt_date = datetime.strptime(receipt_date_str, "%Y-%m-%d")
        days_since_policy = (policy_date - receipt_date).days
except Exception as e:
    print("Could not parse receipt date:", e)

# Step 3: Build main prompt
current_date = datetime.now().strftime("%Y-%m-%d")

main_prompt = f"""
You are an expense auditor.
Date of analysis: {current_date}

Here is the company policy document:

{policy_text}

Here are the receipts with expenses:

{receipt_text}
"""

if receipt_date:
    main_prompt += f"""
The receipt is dated {receipt_date_str}, which is {days_since_policy} days after the purchase ({policy_date.strftime("%Y-%m-%d")}).
"""

main_prompt += """
Task: Compare each expense against the policy.
Output whether each expense is APPROVED or NOT APPROVED, with a brief justification. Add a list of only the approved items if any. However, if the receipt violate date constraints, no item should finally be approved (even if individually they would).
"""

# Call Gemini again with enriched prompt
response = model.generate_content(main_prompt)

print("***Expense Approval Analysis***")
print(response.text)

# Save to output.txt
output_file = os.path.join(directory, "output.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"\nResults saved to {output_file}")
       




