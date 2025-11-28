#!/bin/bash

# Reimbursement Assistant Server Startup Script

echo "🚀 Starting Blure Team Reimbursement Assistant Server..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "✓ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "✓ Installing dependencies..."
    pip install -q -r requirements.txt
    pip install -q aiofiles python-multipart
fi

echo "✓ Starting FastAPI server on port 8000..."
echo ""
echo "📱 Access URLs:"
echo "   Local:  http://localhost:8000"
echo "   Network: http://$(ipconfig getifaddr en0 2>/dev/null || echo "YOUR_IP"):8000"
echo ""
echo "🔐 Demo Accounts:"
echo "   Employee: employee@blureteam.com / demo123"
echo "   Manager:  manager@blureteam.com / demo123"
echo "   Admin:    admin@blureteam.com / demo123"
echo ""
echo "💡 For HTTPS access (teammates outside network):"
echo "   1. Install ngrok: brew install ngrok"
echo "   2. In new terminal: ngrok http 8000"
echo "   3. Share the https:// URL with your team"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Open browser after a short delay (in background)
(sleep 3 && open http://localhost:8000) &

# Start uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

