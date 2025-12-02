# Render Deployment Guide

This application is configured to deploy on Render.com

## Quick Deploy

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Sign up at [Render.com](https://render.com)** with GitHub

3. **Create New Web Service** and configure:
   - **Build Command**: `pip install -r project/app/requirements.txt`
   - **Start Command**: `cd project/app && python ui_app.py`
   - **Environment Variables**:
     - `GEMINI_API_KEY` - Your Gemini API key
     - `GMAIL_USER` - Your Gmail address (optional)
     - `GMAIL_PASSWORD` - Your Gmail app password (optional)

4. **Deploy** and share your URL!

## Detailed Instructions

See the complete step-by-step guide in the artifacts folder.

## Your App URL

Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

Share this with your classmates!
