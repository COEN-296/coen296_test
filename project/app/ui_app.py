from nicegui import ui
from orchestration_agent import handle_request  # Import from your orchestrator file
import os
import fitz  # PyMuPDF for PDF text extraction (kept but not used in UI; can be removed if not needed here)
import io  # For handling file streams (kept for potential future use, but not needed here)
from logging_utils import new_session, get_logger  # Import logging utilities

# Ensure uploads directory exists
os.makedirs('uploads', exist_ok=True)

# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Global list to store uploaded file paths (strings)
uploaded_files = []

@ui.page('/')
async def main_page():
    ui.label('Orchestrator Agent UI').classes('text-h4')
    ui.label('Type instructions and optionally upload PDFs. The agent will process them.')

    # Text input
    instructions = ui.textarea(label='Instructions', placeholder='e.g., Validate these expenses...').props('outlined').classes('w-full')

    # PDF upload (multiple)
    async def handle_upload(event):
        # Read as bytes and save to disk
        content = await event.file.read()
        file_path = os.path.join('uploads', event.file.name)
        with open(file_path, 'wb') as f:
            f.write(content)
        uploaded_files.append(file_path)
        ui.notify(f'File uploaded and saved: {event.file.name}')

    ui.upload(on_upload=handle_upload, multiple=True, label='Upload PDFs').props('accept=.pdf').classes('w-full')

    # Submit button
    async def submit():
        if not instructions.value.strip():
            ui.notify('Please enter instructions.', color='negative')
            return

        # Start new logging session for this request
        logger = new_session(LOG_DIR)
        
        # Log user input
        logger.log_user_input(
            input_text=instructions.value,
            uploaded_files=uploaded_files.copy()
        )

        with ui.dialog().props('persistent') as dialog:
            with ui.card():
                ui.spinner(size='lg')
                ui.label('Processing...')
        try:
            # Pass the list of file paths directly (no text extraction here)
            result = await handle_request(instructions.value, uploaded_files)
            # Handle lists: Convert to string
            if isinstance(result, list):
                result = '\n'.join(str(item) for item in result)  # Join list items with newlines

            # Log the output
            logger.log_output(result)
            logger.log_session_end()

            # Clear for next use
            uploaded_files.clear()

            # Display output
            ui.label('Output:').classes('text-h6')
            ui.markdown(result)
        except Exception as e:
            error_msg = f'Error: {str(e)}'
            logger.log_error(
                error_type="ui_error",
                error_message=str(e),
                context="UI submit function"
            )
            logger.log_session_end()
            ui.notify(error_msg, color='negative')
        finally:
            dialog.close()

    ui.button('Submit', on_click=submit).props('color=primary')

import os
port = int(os.environ.get('PORT', 8080))
ui.run(title='Orchestrator UI', dark=True, port=port, host='0.0.0.0')