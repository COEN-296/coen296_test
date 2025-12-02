import os
import json
from datetime import datetime
from typing import Any, Dict, Optional
import threading

class SessionLogger:
    """
    Logger that captures all interactions in a session with both JSON and human-readable formats.
    Thread-safe for concurrent operations.
    """
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the session logger.
        
        Args:
            log_dir: Directory to store log files (default: "logs")
        """
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create timestamp-based filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = timestamp
        
        # Paths for both formats
        self.json_path = os.path.join(self.log_dir, f"session_{timestamp}.json")
        self.readable_path = os.path.join(self.log_dir, f"session_{timestamp}.log")
        
        # Thread lock for safe concurrent writes
        self.lock = threading.Lock()
        
        # Initialize both log files
        self._init_logs()
    
    def _init_logs(self):
        """Initialize log files with headers."""
        with self.lock:
            # JSON file - start with empty array
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            
            # Human-readable file - add header
            with open(self.readable_path, 'w', encoding='utf-8') as f:
                f.write(f"{'='*80}\n")
                f.write(f"SESSION LOG - {self.session_id}\n")
                f.write(f"{'='*80}\n\n")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    def _append_json(self, entry: Dict[str, Any]):
        """Append an entry to the JSON log."""
        with self.lock:
            # Read existing entries
            with open(self.json_path, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            
            # Add new entry
            entries.append(entry)
            
            # Write back
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def _append_readable(self, text: str):
        """Append text to the human-readable log."""
        with self.lock:
            with open(self.readable_path, 'a', encoding='utf-8') as f:
                f.write(text)
                f.write("\n")
    
    def log_user_input(self, input_text: str, uploaded_files: Optional[list] = None):
        """
        Log user input from the UI.
        
        Args:
            input_text: The user's instruction/query
            uploaded_files: List of uploaded file paths
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "user_input",
            "input_text": input_text,
            "uploaded_files": uploaded_files or []
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n{'-'*80}",
            f"[{timestamp}] USER INPUT",
            f"{'-'*80}",
            f"Input: {input_text}"
        ]
        if uploaded_files:
            readable.append(f"Files: {', '.join(uploaded_files)}")
        self._append_readable("\n".join(readable))
    
    def log_classification(self, category: str, request: str):
        """
        Log the classification result from orchestration agent.
        
        Args:
            category: Classified category (gmail/drive/expense/general)
            request: The request that was classified
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "classification",
            "category": category,
            "request": request
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n[{timestamp}] CLASSIFICATION",
            f"Category: {category}",
            f"Request: {request}"
        ]
        self._append_readable("\n".join(readable))
    
    def log_routing(self, destination: str, method: str):
        """
        Log routing decision.
        
        Args:
            destination: Where the request is being routed (MCP, local, etc.)
            method: The method being called
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "routing",
            "destination": destination,
            "method": method
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n[{timestamp}] ROUTING",
            f"Destination: {destination}",
            f"Method: {method}"
        ]
        self._append_readable("\n".join(readable))
    
    def log_tool_call(self, tool_name: str, parameters: Dict[str, Any], result: Any = None):
        """
        Log a tool call (function call by the model).
        
        Args:
            tool_name: Name of the tool being called
            parameters: Parameters passed to the tool
            result: Result from the tool (optional, can be logged separately)
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "tool_call",
            "tool_name": tool_name,
            "parameters": parameters,
            "result": str(result) if result is not None else None
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n[{timestamp}] TOOL CALL",
            f"Tool: {tool_name}",
            f"Parameters: {json.dumps(parameters, indent=2)}"
        ]
        if result is not None:
            result_str = str(result)
            if len(result_str) > 500:
                result_str = result_str[:500] + "... (truncated)"
            readable.append(f"Result: {result_str}")
        self._append_readable("\n".join(readable))
    
    def log_model_response(self, model_name: str, prompt: str, response: str, 
                          thinking_trace: Optional[str] = None):
        """
        Log a model response.
        
        Args:
            model_name: Name of the model used
            prompt: The prompt sent to the model
            response: The model's response
            thinking_trace: Any thinking/reasoning trace (optional)
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "model_response",
            "model_name": model_name,
            "prompt": prompt,
            "response": response,
            "thinking_trace": thinking_trace
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n[{timestamp}] MODEL RESPONSE",
            f"Model: {model_name}",
            f"Prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}",
            f"\nResponse:\n{response}"
        ]
        if thinking_trace:
            readable.append(f"\nThinking Trace:\n{thinking_trace}")
        self._append_readable("\n".join(readable))
    
    def log_output(self, output: str):
        """
        Log the final output shown to the user.
        
        Args:
            output: The output text/result
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "final_output",
            "output": output
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n{'-'*80}",
            f"[{timestamp}] FINAL OUTPUT",
            f"{'-'*80}",
            f"{output}"
        ]
        self._append_readable("\n".join(readable))
    
    def log_error(self, error_type: str, error_message: str, context: Optional[str] = None):
        """
        Log an error.
        
        Args:
            error_type: Type of error (classification_error, mcp_error, etc.)
            error_message: The error message
            context: Additional context about where the error occurred
        """
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n[{timestamp}] ERROR",
            f"Type: {error_type}",
            f"Message: {error_message}"
        ]
        if context:
            readable.append(f"Context: {context}")
        self._append_readable("\n".join(readable))
    
    def log_session_end(self):
        """Log the end of the session."""
        timestamp = self._get_timestamp()
        
        # JSON entry
        entry = {
            "timestamp": timestamp,
            "type": "session_end"
        }
        self._append_json(entry)
        
        # Human-readable entry
        readable = [
            f"\n{'='*80}",
            f"[{timestamp}] SESSION END",
            f"{'='*80}"
        ]
        self._append_readable("\n".join(readable))


# Global logger instance (will be initialized per session)
_current_logger: Optional[SessionLogger] = None
_logger_lock = threading.Lock()


def get_logger(log_dir: str = "logs") -> SessionLogger:
    """
    Get or create the current session logger.
    
    Args:
        log_dir: Directory for log files
        
    Returns:
        SessionLogger instance
    """
    global _current_logger
    with _logger_lock:
        if _current_logger is None:
            _current_logger = SessionLogger(log_dir)
        return _current_logger


def new_session(log_dir: str = "logs") -> SessionLogger:
    """
    Start a new logging session.
    
    Args:
        log_dir: Directory for log files
        
    Returns:
        New SessionLogger instance
    """
    global _current_logger
    with _logger_lock:
        if _current_logger is not None:
            _current_logger.log_session_end()
        _current_logger = SessionLogger(log_dir)
        return _current_logger
