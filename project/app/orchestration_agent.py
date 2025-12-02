import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastmcp import Client  # Correct import per library docs
from logging_utils import get_logger  # Import logging utilities

# Import Gmail tools (local if needed, but route via MCP)
from gmail_agent import list_emails as gmail_list_emails
from gmail_agent import read_email as gmail_read_email
from gmail_agent import send_email as gmail_send_email
from gmail_agent import create_label as gmail_create_label
from gmail_agent import apply_label as gmail_apply_label

# Expense validation (local)
import fitz  # PyMuPDF
from datetime import datetime
AI_MODEL = "gemini-2.5-flash"


# Load environment variables
load_dotenv()

# Configure Gemini locally for classification/routing
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

async def route_to_mcp(request: str) -> str:
    logger = get_logger()
    logger.log_routing("MCP Server", "agent_action")
    
    try:
        async with Client("http://localhost:8000/sse") as client:
            result = await client.call_tool('agent_action', {'request': request})
            # Improved extraction to avoid repeats
            if hasattr(result, 'content') and isinstance(result.content, list) and len(result.content) > 0 and hasattr(result.content[0], 'text'):
                response = result.content[0].text.replace('\\n', '\n')
            elif hasattr(result, 'structured_content') and 'result' in result.structured_content:
                response = result.structured_content['result'].replace('\\n', '\n')
            elif hasattr(result, 'text'):
                response = result.text.replace('\\n', '\n')
            elif isinstance(result, str) and 'text=' in result:
                # Parse from string like "type='text' text='content'"
                start = result.find("text='") + 6
                end = result.find("'", start)
                text = result[start:end]
                response = text.replace('\\n', '\n')
            else:
                response = str(result).replace('\\n', '\n')
            
            logger.log_model_response(
                model_name="MCP agent_action",
                prompt=request,
                response=response
            )
            return response
    except Exception as e:
        error_msg = f"MCP Error: {str(e)}"
        logger.log_error(
            error_type="mcp_error",
            error_message=str(e),
            context="route_to_mcp"
        )
        return error_msg

async def route_to_mcp_general(prompt: str) -> str:
    logger = get_logger()
    logger.log_routing("MCP Server", "ask_gemini")
    
    try:
        async with Client("http://localhost:8000/sse") as client:
            result = await client.call_tool('ask_gemini', {'prompt': prompt})
            # Improved extraction to avoid repeats
            if hasattr(result, 'content') and isinstance(result.content, list) and len(result.content) > 0 and hasattr(result.content[0], 'text'):
                response = result.content[0].text.replace('\\n', '\n')
            elif hasattr(result, 'structured_content') and 'result' in result.structured_content:
                response = result.structured_content['result'].replace('\\n', '\n')
            elif hasattr(result, 'text'):
                response = result.text.replace('\\n', '\n')
            elif isinstance(result, str) and 'text=' in result:
                start = result.find("text='") + 6
                end = result.find("'", start)
                text = result[start:end]
                response = text.replace('\\n', '\n')
            else:
                response = str(result).replace('\\n', '\n')
            
            logger.log_model_response(
                model_name="MCP ask_gemini",
                prompt=prompt,
                response=response
            )
            return response
    except Exception as e:
        error_msg = f"MCP General Error: {str(e)}"
        logger.log_error(
            error_type="mcp_general_error",
            error_message=str(e),
            context="route_to_mcp_general"
        )
        return error_msg

# Make handle_request async
async def handle_request(user_input: str, file_paths: list[str] = None) -> str:
    """
    Handle a user request by routing to the appropriate agent (Gmail/Drive via MCP, or Expense locally).
    Use natural language to describe the request. If files are involved, upload them to Gemini.
    
    Args:
        user_input: The user's instructions (e.g., "Email john@gmail.com that I hate him").
        file_paths: Optional list of uploaded file paths (e.g., for expense validation).
    """
    if not API_KEY:
        return "Error: GEMINI_API_KEY not set."

    # Get logger for this session
    logger = get_logger()

    # Combine input if files provided
    full_request = user_input
    if file_paths:
        full_request += "\n\nAttached files: " + ', '.join(file_paths)

    # Use local Gemini to classify the request type (sync)
    model = genai.GenerativeModel(model_name=AI_MODEL)
    classification_prompt = f"""
    Classify this request into one category: 'gmail', 'drive', 'expense', or 'general'.
    Request: {full_request}
    Output only the category.
    """
    chat = model.start_chat()
    category_response = chat.send_message(classification_prompt)
    # Safe extract category if response is list or multi-part
    if isinstance(category_response, list):
        category_text = category_response[0].text if hasattr(category_response[0], 'text') else str(category_response[0])
    elif hasattr(category_response, 'candidates') and category_response.candidates:
        category_text = category_response.candidates[0].content.parts[0].text
    else:
        category_text = category_response.text
    category = category_text.strip().lower()
    
    # Log classification result
    logger.log_classification(category, full_request)

    if category == 'expense':
        return await route_to_mcp(full_request)
    elif category in ['gmail', 'drive']:
        # Route to MCP server async
        return await route_to_mcp(full_request)
    else:
        # General: Use MCP's ask_gemini async
        return await route_to_mcp_general(full_request)