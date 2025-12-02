# Red Team Testing - Additional Logging Recommendations

## Overview
Your current logging implementation is **excellent** and captures all the core workflow. For red team testing and security auditing, here are additional things you should log:

---

## 1. Security & Attack Detection Logging

### Prompt Injection Attempts
**What to log:** Detect and log attempts to manipulate the AI with malicious prompts

**Implementation in `orchestration_agent.py`:**
```python
def detect_prompt_injection(user_input: str) -> bool:
    """Detect potential prompt injection attempts"""
    logger = get_logger()
    
    suspicious_patterns = [
        'ignore previous instructions',
        'ignore all previous',
        'system prompt',
        'you are now',
        'new instructions',
        'disregard',
        'forget everything',
        '===',  # Often used to separate injected instructions
        'SYSTEM:',
        'USER:',
        'ASSISTANT:',
    ]
    
    detected = []
    for pattern in suspicious_patterns:
        if pattern.lower() in user_input.lower():
            detected.append(pattern)
    
    if detected:
        logger.log_error(
            error_type="security_prompt_injection_attempt",
            error_message=f"Detected suspicious patterns: {', '.join(detected)}",
            context=f"User input: {user_input[:200]}..."
        )
        return True
    return False

# Add to handle_request function
async def handle_request(user_input: str, file_paths: list[str] = None) -> str:
    logger = get_logger()
    
    # Check for prompt injection
    if detect_prompt_injection(user_input):
        logger.log_classification("SECURITY_THREAT", user_input)
        # You can choose to block or just log
    
    # ... rest of function
```

---

### Sensitive Data Access
**What to log:** Track when sensitive information is accessed

**Add to `gmail_agent.py` after successful email reads:**
```python
def read_email(message_id: str) -> str:
    logger = get_logger()
    # ... existing code ...
    
    # Log if email contains sensitive keywords
    sensitive_keywords = ['password', 'ssn', 'credit card', 'confidential', 'secret']
    body_lower = body.lower()
    found_sensitive = [kw for kw in sensitive_keywords if kw in body_lower]
    
    if found_sensitive:
        logger.log_error(
            error_type="security_sensitive_data_access",
            error_message=f"Email contains sensitive keywords: {', '.join(found_sensitive)}",
            context=f"Message ID: {message_id}"
        )
```

---

### Rate Limiting & Abuse Detection
**What to log:** Detect excessive API usage or potential abuse

**Create new file `rate_limiter.py`:**
```python
from logging_utils import get_logger
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)  # {session_id: [timestamps]}
        self.logger = get_logger()
    
    def check_rate_limit(self, session_id: str, max_requests: int = 100, window_minutes: int = 60):
        """Check if session exceeds rate limit"""
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Clean old requests
        self.requests[session_id] = [
            ts for ts in self.requests[session_id] if ts > window_start
        ]
        
        # Add current request
        self.requests[session_id].append(now)
        
        count = len(self.requests[session_id])
        
        if count > max_requests:
            self.logger.log_error(
                error_type="security_rate_limit_exceeded",
                error_message=f"Session {session_id} made {count} requests in {window_minutes} minutes",
                context=f"Threshold: {max_requests} requests"
            )
            return False
        
        return True
```

---

## 2. Authorization & Access Control Logging

### Track File Access Patterns
**What to log:** Who accessed what files and when

**Add to `drive_agent.py`:**
```python
def log_file_access(file_id: str, operation: str, user_context: dict = None):
    """Log file access for audit trail"""
    logger = get_logger()
    logger.log_tool_call(
        tool_name=f"file_access_{operation}",
        parameters={
            "file_id": file_id,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "user_context": user_context or {}
        }
    )

# Add to download_file, read_document, etc.
def download_file(file_id: str, destination: str = None) -> str:
    log_file_access(file_id, "download")
    # ... existing code ...
```

---

### Email Sending Audit
**What to log:** Complete audit trail of all outgoing emails

**Already implemented, but enhance:**
```python
def send_email(to: str, subject: str, body: str) -> str:
    logger = get_logger()
    
    # Enhanced logging with full context
    logger.log_tool_call(
        tool_name="send_email",
        parameters={
            "to": to,
            "subject": subject,
            "body_length": len(body),
            "timestamp": datetime.now().isoformat(),
            "body_preview": body[:200] + "..." if len(body) > 200 else body
        }
    )
    # ... rest of function
```

---

## 3. Model Behavior Logging

### Refusal & Safety Filter Triggers
**What to log:** When the model refuses requests or safety filters trigger

**Add to `gemini_mcp.py` in agent_action:**
```python
# After response = chat.send_message(request)
if response.candidates:
    candidate = response.candidates[0]
    
    # Log if safety ratings triggered
    if hasattr(candidate, 'safety_ratings'):
        for rating in candidate.safety_ratings:
            if rating.probability != 'NEGLIGIBLE':
                logger.log_error(
                    error_type="security_safety_filter_triggered",
                    error_message=f"Safety filter: {rating.category} = {rating.probability}",
                    context=f"Request: {request[:200]}..."
                )
    
    # Log finish reason
    finish_reason = candidate.finish_reason
    if finish_reason and str(finish_reason) != "STOP":
        logger.log_error(
            error_type="model_unusual_finish_reason",
            error_message=f"Finish reason: {finish_reason}",
            context=f"Request: {request[:200]}..."
        )
```

---

### Token Usage Tracking
**What to log:** Track token consumption for cost analysis and abuse detection

**Add to `gemini_mcp.py`:**
```python
def log_token_usage(response, request_text: str):
    """Log token usage for cost tracking"""
    logger = get_logger()
    
    if hasattr(response, 'usage_metadata'):
        usage = response.usage_metadata
        logger.log_tool_call(
            tool_name="token_usage",
            parameters={
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count,
                "request_length": len(request_text)
            }
        )
```

---

## 4. Data Exfiltration Detection

### Large Data Transfers
**What to log:** Detect attempts to extract large amounts of data

**Add to `drive_agent.py`:**
```python
def detect_bulk_download(files_accessed: list, time_window_seconds: int = 60):
    """Detect potential bulk data exfiltration"""
    logger = get_logger()
    
    if len(files_accessed) > 10:  # Threshold
        logger.log_error(
            error_type="security_bulk_download_detected",
            error_message=f"Downloaded {len(files_accessed)} files in {time_window_seconds}s",
            context=f"Files: {files_accessed[:5]}..."  # Log first 5
        )
```

---

### Unusual Email Recipients
**What to log:** Emails sent to external or unusual domains

**Add to `gmail_agent.py`:**
```python
def check_recipient_safety(to: str):
    """Check if recipient is safe/expected"""
    logger = get_logger()
    
    # Define trusted domains
    trusted_domains = ['example.com', 'mycompany.com']
    
    recipient_domain = to.split('@')[-1] if '@' in to else ''
    
    if recipient_domain not in trusted_domains:
        logger.log_error(
            error_type="security_external_recipient",
            error_message=f"Email sent to external domain: {recipient_domain}",
            context=f"Recipient: {to}"
        )
```

---

## 5. Policy Violations

### Expense Policy Violations
**What to log:** Track why expenses were denied

**Enhance `expense_agent.py`:**
```python
# In validate_reimbursement, after model response
if result == "DENIED":
    logger.log_error(
        error_type="policy_expense_denied",
        error_message="Expense reimbursement denied",
        context=json.dumps({
            "receipt_date": receipt_date_str,
            "days_since": days_since_receipt,
            "reason": response.text if hasattr(response, 'text') else "Unknown"
        })
    )
```

---

## 6. Anomaly Detection

### Unusual Request Patterns
**What to log:** Requests that don't fit normal patterns

```python
def detect_anomaly(user_input: str, category: str):
    """Detect unusual request patterns"""
    logger = get_logger()
    
    # Example: Detect very long inputs (potential attack)
    if len(user_input) > 10000:
        logger.log_error(
            error_type="security_unusually_long_input",
            error_message=f"Input length: {len(user_input)} characters",
            context=f"Category: {category}"
        )
    
    # Example: Detect repeated characters (potential DoS)
    if any(char * 100 in user_input for char in 'abcdefghijklmnopqrstuvwxyz'):
        logger.log_error(
            error_type="security_repeated_characters",
            error_message="Input contains excessive repeated characters",
            context=f"Input preview: {user_input[:200]}..."
        )
```

---

## 7. Red Team Specific Logging

### Create a Red Team Log Analyzer

**Create `red_team_analyzer.py`:**
```python
import json
from datetime import datetime
from collections import Counter

def analyze_security_logs(log_file: str):
    """Analyze logs for security insights"""
    
    with open(log_file, 'r') as f:
        logs = json.load(f)
    
    # Count security events
    security_events = [
        log for log in logs 
        if log.get('type') == 'error' and 
        log.get('error_type', '').startswith('security_')
    ]
    
    print(f"\n=== Security Event Summary ===")
    print(f"Total security events: {len(security_events)}")
    
    # Group by type
    event_types = Counter(log['error_type'] for log in security_events)
    print(f"\nBreakdown by type:")
    for event_type, count in event_types.most_common():
        print(f"  {event_type}: {count}")
    
    # Find sensitive data access
    sensitive_access = [
        log for log in logs
        if 'sensitive_data_access' in log.get('error_type', '')
    ]
    print(f"\nSensitive data access attempts: {len(sensitive_access)}")
    
    # Find policy violations
    policy_violations = [
        log for log in logs
        if 'policy_' in log.get('error_type', '')
    ]
    print(f"Policy violations: {len(policy_violations)}")

if __name__ == "__main__":
    import glob
    latest_log = max(glob.glob("logs/session_*.json"), key=os.path.getctime)
    analyze_security_logs(latest_log)
```

---

## Summary of Additional Logging for Red Team Testing

| Category | What to Log | Priority |
|----------|-------------|----------|
| **Prompt Injection** | Suspicious patterns in user input | 🔴 Critical |
| **Rate Limiting** | Excessive API usage | 🔴 Critical |
| **Sensitive Data** | Access to confidential information | 🔴 Critical |
| **Safety Filters** | Model safety triggers | 🟡 High |
| **Token Usage** | Cost tracking and abuse detection | 🟡 High |
| **File Access** | Who accessed what when | 🟡 High |
| **Email Audit** | Complete outgoing email trail | 🔴 Critical |
| **Policy Violations** | Why requests were denied | 🟢 Medium |
| **Anomalies** | Unusual patterns | 🟡 High |
| **Bulk Operations** | Data exfiltration attempts | 🔴 Critical |

---

## Quick Implementation Priority

**Start with these 3 (highest ROI):**
1. **Prompt injection detection** - Add to `orchestration_agent.py`
2. **Email sending audit** - Enhance `gmail_agent.py`
3. **Sensitive data access logging** - Add to `gmail_agent.py` and `drive_agent.py`

**Then add:**
4. Safety filter logging in `gemini_mcp.py`
5. Rate limiting with the rate limiter class
6. Red team log analyzer script

This will give you comprehensive security logging for red team testing!
