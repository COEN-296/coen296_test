# Mock Authentication Setup

## Overview
The login pages have been updated to use **mock authentication** for local testing, removing the Firebase dependency. This allows you to test the UI immediately without needing Firebase credentials.

## Default Login Credentials

### Demo Accounts
Three pre-configured demo accounts are available:

1. **Employee Account**
   - Email: `employee@blureteam.com`
   - Password: `demo123`
   - Role: Employee

2. **Manager Account**
   - Email: `manager@blureteam.com`
   - Password: `demo123`
   - Role: Manager

3. **Admin Account**
   - Email: `admin@blureteam.com`
   - Password: `demo123`
   - Role: Admin

## How to Login

### Quick Login (Recommended)
Simply click one of the demo account buttons on the login page:
- 👤 **Employee Demo**
- 👔 **Manager Demo**
- ⚙️ **Admin Demo**

### Manual Login
1. Enter one of the email addresses above
2. Enter the password: `demo123`
3. Click "Sign In"

## Technical Details

### How It Works
- User credentials are stored in browser `localStorage` (mock database)
- Authentication state is stored in `sessionStorage`
- No network requests are made
- Simulates a 500ms network delay for realistic UX

### Data Storage
- **Mock Database**: `localStorage` key `mock_users_db`
- **Session Data**: Stored in `sessionStorage`:
  - `userRole`: User's role (employee/manager/admin)
  - `userName`: User's display name
  - `userEmail`: User's email address
  - `userUid`: Mock user ID
  - `mockAuth`: Authentication flag (`'true'`)

### Security Note
⚠️ **This is for LOCAL TESTING ONLY**. Passwords are stored in plain text in localStorage. For production, you must:
1. Set up proper Firebase authentication (Option 1 from earlier)
2. Or implement a secure backend authentication system
3. Never deploy this mock authentication to production

## Files Modified
- `/UI/login.html` - Updated with mock authentication
- `/project/static/login.html` - Updated with mock authentication

## Migrating to Production

To migrate to production Firebase authentication:
1. Follow the instructions in `/DEPLOYMENT.md`
2. Update the Firebase configuration in both login pages
3. Re-add the Firebase SDK scripts
4. Replace the mock authentication code with the original Firebase authentication

## Troubleshooting

### Login Not Working
- Clear browser localStorage: Open DevTools → Application → Local Storage → Clear All
- Clear browser cache and reload the page

### Already Logged In
- The system automatically redirects to `index.html` if you're already authenticated
- To logout, clear sessionStorage or close/reopen the browser

### Console Output
When using mock authentication, you'll see these console messages:
- `🔧 Mock Authentication Mode - No Firebase Required`
- `🚀 Quick login as: [role]`
- `✅ Mock login successful: {email, role, name}`
- `🔐 Already authenticated, redirecting...`
