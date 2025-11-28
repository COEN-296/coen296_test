# Blure Team Enterprise Copilot - Reimbursement Assistant User Guide

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Firebase Configuration](#firebase-configuration)
4. [Using the Chat Interface](#using-the-chat-interface)
5. [Uploading Reimbursement Proof](#uploading-reimbursement-proof)
6. [Viewing Claim Metadata](#viewing-claim-metadata)
7. [Processing Reimbursement Decisions](#processing-reimbursement-decisions)
8. [Clearing Metadata](#clearing-metadata)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The **Blure Team Enterprise Copilot - Reimbursement Assistant** is a web-based application designed to streamline the reimbursement claim process. The application provides:

- **AI Chat Assistant** for answering policy and procedure questions
- **PDF Upload** functionality for submitting reimbursement proofs
- **Real-time Metadata Display** showing current claim information
- **Automated Metadata Clearing** upon claim approval or decline
- **Professional, Responsive Design** for desktop and mobile devices

---

## Getting Started

### Accessing the Application

1. Open `index.html` in a modern web browser (Chrome, Firefox, Safari, or Edge)
2. The application will initialize and authenticate automatically
3. Wait for the status indicator (top-right) to show "Connected" with a green dot

### System Requirements

- Modern web browser with JavaScript enabled
- Internet connection (for Firebase and Tailwind CSS CDN)
- Firebase project with Firestore enabled

---

## Firebase Configuration

**IMPORTANT:** Before using the application, you must configure Firebase with your project credentials.

### Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Follow the setup wizard to create your project

### Step 2: Enable Firestore

1. In the Firebase Console, navigate to **Firestore Database**
2. Click "Create database"
3. Choose "Start in production mode" or "test mode" (test mode for development)
4. Select a location for your database

### Step 3: Get Firebase Configuration

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Scroll to "Your apps" section
3. Click the web icon (`</>`) to add a web app
4. Register your app (nickname: "Reimbursement Assistant")
5. Copy the Firebase configuration object

### Step 4: Update index.html

1. Open `index.html` in a text editor
2. Find the `firebaseConfig` object (around line 223)
3. Replace the placeholder values with your actual Firebase credentials:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_ACTUAL_API_KEY",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef123456"
};
```

### Step 5: Configure Firestore Security Rules

For production, set appropriate security rules in Firestore:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /artifacts/{appId}/users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

## Using the Chat Interface

### Starting a Conversation

1. Type your question in the text input field at the bottom of the chat panel
2. Click the "Send" button or press Enter
3. The AI assistant will respond with relevant information

### Example Questions You Can Ask

- **Policy Questions:**
  - "What expenses are eligible for reimbursement?"
  - "What is the reimbursement policy?"
  - "Are there any spending limits?"

- **Process Questions:**
  - "How do I submit a claim?"
  - "How long does the process take?"
  - "What happens after I upload my receipt?"

- **Upload Help:**
  - "How do I upload my PDF?"
  - "What file types are accepted?"

- **Status Inquiries:**
  - "How can I check my claim status?"
  - "When will I get paid?"

### AI Response Features

The AI assistant provides contextual, intelligent responses based on:
- Reimbursement policies and procedures
- Eligible expenses and limits
- Claim submission process
- Timeline expectations
- Common troubleshooting

---

## Uploading Reimbursement Proof

### Upload Methods

**Method 1: Click to Select**
1. Click anywhere in the upload area (dashed border box)
2. Select your PDF file from the file browser
3. Click "Upload PDF" button

**Method 2: Drag and Drop**
1. Drag your PDF file from your file explorer
2. Drop it onto the upload area
3. Click "Upload PDF" button

### Important Notes

- **Only PDF files are accepted** (receipts, invoices, proof of purchase)
- File size and name will be displayed after selection
- Upload status will show progress and confirmation
- Metadata is automatically saved to Firebase Firestore

### After Upload

- The chat assistant will confirm receipt of your document
- Metadata will appear in the "Current Claim Metadata" panel
- Status will be set to "pending" initially

---

## Viewing Claim Metadata

The **Current Claim Metadata** panel displays information about your uploaded reimbursement proof:

### Displayed Information

1. **Filename:** Name of the uploaded PDF file
2. **File Size:** Size of the file (formatted in KB/MB)
3. **Upload Date:** Timestamp of when the file was uploaded
4. **Status:** Current claim status
   - 🟡 **Pending:** Awaiting review
   - 🟢 **Approved:** Claim accepted
   - 🔴 **Declined:** Claim rejected

### Real-Time Updates

- Metadata updates automatically when changes occur
- No page refresh required
- Firebase Firestore provides live synchronization

---

## Processing Reimbursement Decisions

### Accept Reimbursement

1. Review the uploaded claim metadata
2. Click the **"✓ Accept Reimbursement"** button (green)
3. Confirm the action in the popup dialog
4. The system will:
   - Update status to "approved"
   - Send confirmation via chat
   - **Automatically clear metadata after 2 seconds**

### Decline Reimbursement

1. Review the uploaded claim metadata
2. Click the **"✗ Decline Reimbursement"** button (orange)
3. Confirm the action in the popup dialog
4. The system will:
   - Update status to "declined"
   - Send notification via chat
   - **Automatically clear metadata after 2 seconds**

### Auto-Clear Feature

As per requirements, metadata is **automatically cleared** when:
- Reimbursement is accepted ✓
- Reimbursement is declined ✗

This ensures:
- Clean slate for next claim
- No orphaned data in Firestore
- Compliance with data retention policies

---

## Clearing Metadata

### Manual Clearing

If you need to manually clear metadata (without approval/decline):

1. Click the **"Clear Metadata & Reset"** button (red)
2. Confirm the action in the popup dialog
3. Metadata will be deleted from Firestore immediately
4. The metadata panel will show "No metadata available"

### When to Use Manual Clear

- Uploading wrong file and need to start over
- Testing the system
- Resetting after an error
- Clearing old data before new submission

---

## Troubleshooting

### Issue: Status Shows "Config Error"

**Cause:** Firebase configuration is invalid or missing

**Solution:**
1. Verify Firebase credentials in `index.html`
2. Ensure all configuration values are correct
3. Check Firebase Console for project settings
4. Refresh the page after updating configuration

---

### Issue: Status Shows "Auth Failed"

**Cause:** Firebase authentication error

**Solution:**
1. Check Firebase Console → Authentication is enabled
2. Enable "Anonymous" sign-in method if using anonymous auth
3. Check browser console for detailed error messages
4. Verify internet connection

---

### Issue: Upload Button is Disabled

**Cause:** No file selected or invalid file type

**Solution:**
1. Ensure you've selected a PDF file
2. Check that the file has `.pdf` extension
3. Try selecting the file again
4. Verify the file isn't corrupted

---

### Issue: Metadata Not Displaying

**Cause:** Firestore connection issue or no data uploaded

**Solution:**
1. Check that upload was successful (green success message)
2. Verify Firebase Firestore is enabled in Firebase Console
3. Check Firestore security rules allow read access
4. Check browser console for errors
5. Try uploading again

---

### Issue: Cannot Delete Metadata

**Cause:** Firestore permissions or connection issue

**Solution:**
1. Verify Firestore security rules allow delete operations
2. Check authentication status (should show "Connected")
3. Ensure internet connection is stable
4. Check browser console for error details

---

### Issue: Chat Not Responding

**Cause:** JavaScript error or browser compatibility

**Solution:**
1. Refresh the page
2. Use a modern browser (Chrome, Firefox, Safari, Edge)
3. Enable JavaScript in browser settings
4. Check browser console for errors
5. Clear browser cache and retry

---

### Issue: Drag and Drop Not Working

**Cause:** Browser doesn't support drag and drop or file type mismatch

**Solution:**
1. Use "Click to Select" method instead
2. Ensure you're dragging a PDF file
3. Try a different browser
4. Check that only ONE file is being dropped

---

## Data Storage Path

Metadata is stored in Firebase Firestore at:

```
/artifacts/{appId}/users/{userId}/reimbursement_proofs/current_claim
```

Where:
- `{appId}`: Application identifier (`reimbursement_app_v1`)
- `{userId}`: Authenticated user's unique ID (Firebase UID)

This ensures:
- User data privacy
- Data isolation per user
- Organized storage structure
- Easy data management

---

## Security Considerations

### Best Practices

1. **Production Security Rules:** Always use proper Firestore security rules in production
2. **HTTPS Only:** Host application over HTTPS in production
3. **API Key Protection:** Consider using Firebase App Check for additional security
4. **User Authentication:** Implement proper user authentication (not just anonymous)
5. **Data Retention:** Define policies for how long metadata is stored

### Private Data

The application stores metadata privately under each authenticated user's path. This ensures:
- Users can only access their own data
- No cross-user data leakage
- Compliance with privacy requirements

---

## Mobile Responsiveness

The application is fully responsive and works on:
- **Desktop:** Full feature set with side-by-side layout
- **Tablet:** Optimized layout with appropriate spacing
- **Mobile:** Stacked layout for small screens

All interactive elements are touch-friendly and accessible on mobile devices.

---

## Support

For additional help or issues not covered in this guide:

- **Email:** reimbursement-support@blureteam.com
- **Documentation:** Review Firebase and Tailwind CSS documentation
- **Browser Console:** Check for error messages that provide more details

---

## Version Information

- **Application Version:** 1.0.0
- **Last Updated:** November 2025
- **Tailwind CSS:** 3.x (via CDN)
- **Firebase SDK:** 10.7.1

---

**© 2025 Blure Team Enterprise. All rights reserved.**
