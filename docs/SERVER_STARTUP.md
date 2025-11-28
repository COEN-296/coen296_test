# Server Startup Guide

## Quick Start

### Option 1: Local HTTP (Auto-opens browser)
```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
./start_server.sh
```
- Starts server on http://localhost:8000
- **Automatically opens browser** after 3 seconds
- Access from same computer or local network

### Option 2: HTTPS with ngrok (Auto-opens browser with HTTPS)
```bash  
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
./start_server_https.sh --ngrok
```
- Starts server and creates HTTPS tunnel
- **Automatically opens browser** with HTTPS URL
- Share the HTTPS URL with teammates anywhere
- Requires ngrok: `brew install ngrok`

## What Happens When Server Starts

1. ✅ Virtual environment activates
2. ✅ Dependencies install (if needed)
3. ✅ FastAPI server starts on port 8000
4. ✅ **Browser automatically opens** (after 3 seconds)
5. ✅ Redirects to login page

## Demo Accounts

Once the browser opens, login with:

- **Employee**: employee@blureteam.com / demo123
- **Manager**: manager@blureteam.com / demo123  
- **Admin**: admin@blureteam.com / demo123

## Access Methods

### Local Access
- **URL**: http://localhost:8000
- **Who can access**: You only
- **Auto-open**: ✅ Yes

### Network Access  
- **URL**: http://YOUR_IP:8000
- **Who can access**: Anyone on same WiFi/network
- **Auto-open**: ❌ No (they need to type URL)

### HTTPS Access (ngrok)
- **URL**: https://random-string.ngrok-free.app
- **Who can access**: Anyone, anywhere with the link
- **Auto-open**: ✅ Yes (when using --ngrok flag)

## Stopping the Server

Press `Ctrl+C` in the terminal

## Troubleshooting

### Browser doesn't open
- Check if port 8000 is already in use
- Manually open: http://localhost:8000

### ngrok not found
```bash
brew install ngrok
```

### Port 8000 already in use
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

Then restart the server.

## File Sync

The UI files are automatically synced from `/UI/` to `/project/static/`:
- `/UI/index.html` → `/project/static/index.html`
- `/UI/login.html` → `/project/static/login.html`

Any updates to `/UI/` files should be copied to `/project/static/` before starting the server.

## Quick Copy Command

To manually sync UI files:
```bash
cp /Users/suraj/Desktop/ai_goverance/coen296-main/UI/*.html /Users/suraj/Desktop/ai_goverance/coen296-main/project/static/
```
