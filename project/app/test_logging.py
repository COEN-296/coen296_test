# Test Logging System

import asyncio
from logging_utils import new_session
import os

# Set log directory
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')

async def test_logging():
    """Test the logging system without running the full app."""
    
    # Create a new session
    logger = new_session(LOG_DIR)
    
    print("Testing logging system...")
    print(f"Logs will be saved to: {LOG_DIR}")
    
    # Test user input logging
    logger.log_user_input(
        input_text="Test query: What is the weather today?",
        uploaded_files=["test_file.pdf"]
    )
    
    # Test classification logging
    logger.log_classification(
        category="general",
        request="Test query: What is the weather today?"
    )
    
    # Test routing logging
    logger.log_routing(
        destination="MCP Server",
        method="ask_gemini"
    )
    
    # Test model response logging
    logger.log_model_response(
        model_name="gemini-2.5-flash",
        prompt="What is the weather today?",
        response="I don't have access to real-time weather information."
    )
    
    # Test tool call logging
    logger.log_tool_call(
        tool_name="list_emails",
        parameters={"max_results": 10},
        result="Found 5 emails"
    )
    
    # Test output logging
    logger.log_output(
        output="I don't have access to real-time weather information. You can check weather.com for current conditions."
    )
    
    # Test error logging
    logger.log_error(
        error_type="test_error",
        error_message="This is a test error",
        context="test_logging function"
    )
    
    # End session
    logger.log_session_end()
    
    print(f"\nTest complete! Check the logs directory:")
    print(f"JSON log: {logger.json_path}")
    print(f"Human-readable log: {logger.readable_path}")

if __name__ == "__main__":
    asyncio.run(test_logging())
