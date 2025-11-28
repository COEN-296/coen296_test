#!/bin/bash

# Enhanced Reimbursement Assistant Server Startup Script
# Supports automatic browser opening and optional HTTPS via ngrok

echo "🚀 Starting Blure Team Reimbursement Assistant Server..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Check if ngrok should be used
USE_NGROK=false
if [ "$1" == "--ngrok" ] || [ "$1" == "-n" ]; then
    USE_NGROK=true
    echo "🔐 HTTPS mode enabled via ngrok"
    echo ""
fi

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

if [ "$USE_NGROK" = true ]; then
    # Check if ngrok is installed
    if ! command -v ngrok &> /dev/null; then
        echo "❌ ngrok is not installed!"
        echo ""
        echo "To install ngrok:"
        echo "  brew install ngrok"
        echo ""
        echo "Or download from: https://ngrok.com/download"
        echo ""
        echo "Falling back to local HTTP mode..."
        USE_NGROK=false
    fi
fi

echo "✓ Starting FastAPI server on port 8000..."
echo ""

if [ "$USE_NGROK" = true ]; then
    echo "📱 Setting up HTTPS tunnel..."
    echo ""
    
    # Start FastAPI server in background
    uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 3
    
    # Start ngrok and capture the URL
    echo "🌐 Starting ngrok tunnel..."
    ngrok http 8000 --log=stdout > /tmp/ngrok.log &
    NGROK_PID=$!
    
    # Wait for ngrok to start and get the URL
    sleep 3
    
    # Extract ngrok URL
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*"' | grep -o 'https://[^"]*' | head -1)
    
    if [ -z "$NGROK_URL" ]; then
        echo "⚠️  Could not get ngrok URL. Please check manually at http://localhost:4040"
        NGROK_URL="http://localhost:8000"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ Server is running!"
    echo ""
    echo "📱 Access URLs:"
    echo "   HTTPS (Public): $NGROK_URL"
    echo "   HTTP (Local):   http://localhost:8000"
    echo "   Network:        http://$(ipconfig getifaddr en0 2>/dev/null || echo "YOUR_IP"):8000"
    echo ""
    echo "🔗 Share this HTTPS URL with your team:"
    echo "   $NGROK_URL"
    echo ""
    echo "🔐 Demo Accounts:"
    echo "   Employee: employee@blureteam.com / demo123"
    echo "   Manager:  manager@blureteam.com / demo123"
    echo "   Admin:    admin@blureteam.com / demo123"
    echo ""
    echo "📊 ngrok Dashboard: http://localhost:4040"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Opening browser..."
    
    # Open browser with HTTPS URL
    sleep 2
    open "$NGROK_URL"
    
    # Keep script running
    echo ""
    echo "Press Ctrl+C to stop the server and ngrok tunnel"
    
    # Wait for Ctrl+C
    trap "kill $SERVER_PID $NGROK_PID 2>/dev/null; exit" INT TERM
    wait
    
else
    # Standard HTTP mode
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
    echo "   Run: ./start_server_https.sh --ngrok"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Open browser after a short delay (in background)
    (sleep 3 && open http://localhost:8000) &
    
    # Start uvicorn
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi
