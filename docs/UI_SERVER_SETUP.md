# Reimbursement Assistant - Server Setup & Access Guide

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the UI

- **Local access**: http://localhost:8000
- **Team access** (same network): http://YOUR_IP_ADDRESS:8000
- **Auto-redirects to login page**

---

## HTTPS Access for Teammates

### Option 1: Using ngrok (Easiest - Instant HTTPS)

**Install ngrok:**
```bash
brew install ngrok
# or download from https://ngrok.com/download
```

**Run the server:**
```bash
# Terminal 1: Start FastAPI server
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Create HTTPS tunnel:**
```bash
# Terminal 2: Start ngrok
ngrok http 8000
```

**Share the URL:**
ngrok will give you a public HTTPS URL like:
```
https://abcd-1234-5678.ngrok-free.app
```

Share this URL with your teammates - they can access it from anywhere!

**Demo Accounts for Testing:**
- Employee: employee@blureteam.com / demo123
- Manager: manager@blureteam.com / demo123
- Admin: admin@blureteam.com / demo123

---

### Option 2: Using Cloudflare Tunnel (Free, Persistent)

**Install:**
```bash
brew install cloudflare/homebrew/cloudflared
```

**Run server:**
```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Create tunnel:**
```bash
cloudflared tunnel --url http://localhost:8000
```

You'll get a URL like: `https://random-words.trycloudflare.com`

---

### Option 3: Deploy to Production (Render.com - Free Tier)

**1. Create `Procfile` in project folder:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**2. Push to GitHub**

**3. Deploy on Render:**
- Go to https://render.com
- Connect GitHub repo
- Select "Web Service"
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

You'll get: `https://your-app-name.onrender.com`

---

## File Structure

```
project/
├── static/                  # UI files (served at /static/)
│   ├── login.html          # Login page
│   ├── index.html          # Main application
│   └── USER_GUIDE.md       # Documentation
├── app/
│   ├── main.py             # FastAPI server (updated)
│   ├── agent.py
│   └── ...
├── requirements.txt
└── run_instructions.md
```

---

## Available Endpoints

### UI Endpoints
- `GET /` → Redirects to login
- `GET /static/login.html` → Login page
- `GET /static/index.html` → Main application
- `GET /static/*` → All UI assets

### API Endpoints (from original project)
- `POST /tasks` → Submit task to agent
- `GET /logs` → View logs
- `POST /tests/rt-01` → Red team simulation

---

## Finding Your IP Address

**For team access on local network:**

**On Mac:**
```bash
ipconfig getifaddr en0
```

**On Linux:**
```bash
hostname -I | awk '{print $1}'
```

**On Windows:**
```bash
ipconfig
```

Share: `http://YOUR_IP:8000`

---
# UI Development & Server Setup Guide

## Directory Structure

### UI Source Files
**Location**: `/project/ui/`

Contains the source files for the web interface:
- `index.html` - Main application interface
- `login.html` - Login page  
- `USER_GUIDE.md` - Application user guide

### Deployed UI Files
**Location**: `/project/static/`

The FastAPI server serves files from this directory. Files are synced here from `/project/ui/` using the sync script.

## Development Workflow

### 1. Edit UI Files

Edit the source files in `/project/ui/`:
```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project/ui
# Edit index.html, login.html, etc.
```

### 2. Sync to Static Directory

Run the sync script to copy files to the static directory:
```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
scripts/sync_ui.sh
```

Or from the project root:
```bash
./scripts/sync_ui.sh  # Via direct path
```

### 3. View Changes

The sync script (`scripts/sync_ui.sh`) automatically copies files from `/project/ui/` to `/project/static/`:. Simply refresh your browser:
- Normal refresh: `Cmd + R`
- Hard refresh (clear cache): `Cmd + Shift + R`

---

## Production Checklist

Before sharing with team:

- [ ] Update Firebase config in `static/login.html` (lines 165-170)
- [ ] Update Firebase config in `static/index.html` (lines 265-270)
- [ ] Set up Firestore security rules
- [ ] Enable Firebase Authentication
- [ ] Test all three roles (Employee, Manager, Admin)
- [ ] Verify logout functionality
- [ ] Test on different devices/browsers

---

## Recommended: Use ngrok for Team Access

**Why ngrok:**
✅ Instant HTTPS
✅ Works from anywhere (not just local network)
✅ Free tier available
✅ No deployment needed
✅ Perfect for team testing

**Steps:**
1. `brew install ngrok`
2. `uvicorn app.main:app --reload --port 8000`
3. `ngrok http 8000` (in new terminal)
4. Share the `https://` URL with team

That's it! Your teammates can access the UI from anywhere with a secure HTTPS link.

---

## Security Note

- ngrok/Cloudflare tunnels are great for development and testing
- For production, use proper deployment (Render, Heroku, AWS, etc.)
- Always use HTTPS in production
- Implement proper authentication before going live
