# Logging Integration for gemini_mcp.py

To add logging to `gemini_mcp.py`, make the following minimal changes:

## 1. Add import at the top (after line 12):
```python
from logging_utils import get_logger  # Import logging utilities
```

## 2. In the `agent_action` function, after line 242 (after chat session starts), add:
```python
    # Get logger
    logger = get_logger()
```

## 3. Replace the try block (lines 244-258) with:
```python
    try:
        # 3. Send message to model (it will auto-call tools if needed)
        response = chat.send_message(request)
        
        # Log any tool calls that were made
        try:
            if hasattr(chat, 'history'):
                for turn in chat.history:
                    if hasattr(turn, 'parts'):
                        for part in turn.parts:
                            if hasattr(part, 'function_call'):
                                # Log the function call
                                func_call = part.function_call
                                logger.log_tool_call(
                                    tool_name=func_call.name,
                                    parameters=dict(func_call.args)
                                )
        except Exception as log_err:
            # Don't fail if logging fails
            pass
        
        # Safe extract text - fixes the error
        if response.candidates and response.candidates[0].content.parts:
            result_text = response.text
            logger.log_model_response(
                model_name="gemini-2.5-flash (agent_action)",
                prompt=request,
                response=result_text
            )
            return result_text
        else:
            finish_reason = response.candidates[0].finish_reason if response.candidates else "Unknown"
            if finish_reason == "MALFORMED_FUNCTION_CALL":
                # Retry with clarification prompt
                retry_response = chat.send_message("The previous tool call was malformed. Retry with correct arguments or ask for more info if needed.")
                result_text = retry_response.text
                logger.log_model_response(
                    model_name="gemini-2.5-flash (agent_action retry)",
                    prompt="Retry with clarification",
                    response=result_text
                )
                return result_text
            error_msg = "No results found or response blocked. Finish reason: " + str(finish_reason)
            logger.log_error(
                error_type="agent_action_finish_reason",
                error_message=error_msg,
                context="agent_action"
            )
            return error_msg
    except Exception as e:
        error_msg = f"Agent Error: {str(e)}"
        logger.log_error(
            error_type="agent_action_exception",
            error_message=str(e),
            context="agent_action"
        )
        return error_msg
```

These changes will enable logging of tool calls and model responses in the MCP server.
