# Firebase Hosting Deployment Guide

## Quick Start - Deploy in 3 Steps

### Step 1: Install Firebase CLI

Open your terminal and run:

```bash
npm install -g firebase-tools
```

### Step 2: Login and Initialize

```bash
# Login to Firebase
firebase login

# Navigate to your project directory
cd /Users/suraj/Desktop/ai_goverance/coen296-main

# Initialize Firebase (if not already done)
firebase init hosting
```

When prompted:
- **Select existing project** or create a new one
- **Public directory**: Enter `UI`
- **Configure as single-page app**: **No**
- **Set up automatic builds**: **No**
- **Overwrite files**: **No** (we already have the files)

### Step 3: Deploy

```bash
firebase deploy --only hosting
```

After deployment, you'll receive a URL like:
```
https://your-project-id.web.app
```

Share this URL with your teammates!

---

## Complete Deployment Instructions

### Prerequisites

1. **Node.js & npm** must be installed
   - Check: `node --version` and `npm --version`
   - Install from: https://nodejs.org/

2. **Firebase Project** configured
   - Update `UI/login.html` with your Firebase config (lines 165-170)
   - Update `UI/index.html` with your Firebase config (lines 265-270)

### Detailed Steps

#### 1. Install Firebase CLI

```bash
npm install -g firebase-tools
```

#### 2. Login to Firebase

```bash
firebase login
```

This will open a browser window for authentication.

#### 3. Configure Firebase Project

If you haven't initialized Firebase in this directory:

```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main
firebase init hosting
```

Select or create your Firebase project when prompted.

#### 4. Deploy

```bash
firebase deploy --only hosting
```

Expected output:
```
✔  Deploy complete!

Project Console: https://console.firebase.google.com/project/your-project/overview
Hosting URL: https://your-project-id.web.app
```

#### 5. Share URL

Your teammates can now access:
- **Login**: `https://your-project-id.web.app/login.html`
- **Main App**: `https://your-project-id.web.app/index.html`

---

## Alternative: Quick Deploy with Single Command

If Firebase is already configured, just run:

```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main
firebase deploy --only hosting
```

---

## Custom Domain (Optional)

To use a custom domain like `reimbursement.yourcompany.com`:

1. Go to Firebase Console → Hosting
2. Click "Add custom domain"
3. Follow verification steps
4. Update DNS records as instructed
5. SSL certificate will be provisioned automatically

---

## Environment-Specific Configuration

### Development
```bash
firebase serve
```
Access locally at: `http://localhost:5000`

### Production
```bash
firebase deploy --only hosting
```
Access at: `https://your-project-id.web.app`

---

## Troubleshooting

### Issue: "Firebase not found"
**Solution**: Make sure Firebase CLI is installed globally
```bash
npm install -g firebase-tools
```

### Issue: "Not authorized"
**Solution**: Login again
```bash
firebase logout
firebase login
```

### Issue: "No Firebase project found"
**Solution**: Initialize Firebase
```bash
firebase init hosting
```

### Issue: Changes not reflecting
**Solution**: Clear cache and redeploy
```bash
firebase deploy --only hosting
```

---

## Security Checklist

Before deploying to production:

- [ ] Update Firebase config in `login.html`
- [ ] Update Firebase config in `index.html`
- [ ] Set up Firestore security rules
- [ ] Enable Firebase Authentication
- [ ] Test all user roles (Employee, Manager, Admin)
- [ ] Verify logout functionality
- [ ] Test on different devices/browsers

---

## Monitoring & Analytics

After deployment, monitor your app:

1. **Firebase Console**: https://console.firebase.google.com
2. **Hosting Dashboard**: View traffic, bandwidth usage
3. **Analytics**: Set up Google Analytics (optional)

---

## Update Deployment

To deploy updates after making changes:

```bash
cd /Users/suraj/Desktop/ai_goverance/coen296-main
firebase deploy --only hosting
```

Changes will be live within seconds!

---

## Rollback (if needed)

View previous deployments:
```bash
firebase hosting:channel:list
```

Rollback to previous version:
```bash
firebase hosting:channels:rollback
```

---

## Next Steps

1. **Deploy**: Run `firebase deploy --only hosting`
2. **Test**: Access the URL and test all features
3. **Share**: Send the HTTPS URL to your teammates
4. **Configure**: Update Firebase credentials before production use
5. **Secure**: Implement Firestore security rules
