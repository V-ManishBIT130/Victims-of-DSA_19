# 🛡️ Phishing Detector Chrome Extension

Real-time phishing detection system that integrates with UiPath email extraction workflow to display warnings directly in Gmail.

## 📋 Architecture

```
UiPath Workflow → emails_data.json (10s updates) → Node.js API Server → Chrome Extension → Gmail UI Warnings
```

## 🚀 Setup Instructions

### Step 1: Install Node.js Dependencies

Open PowerShell in the `phishing_extension` folder and run:

```powershell
npm install
```

This installs:
- **express**: API server framework
- **cors**: Cross-origin resource sharing for Chrome extension

### Step 2: Start the API Server

Run the server to expose the JSON data:

```powershell
npm start
```

You should see:
```
🛡️  PHISHING DETECTOR API SERVER
✅ Server running on http://localhost:3000
📂 Monitoring file: C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json
```

**Keep this terminal running!**

### Step 3: Load Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Select the `C:\Users\V Manish\Desktop\phishing_extension` folder
5. The extension icon should appear in your toolbar

### Step 4: Make Sure UiPath is Running

Your UiPath workflow should be running and updating `emails_data.json` every 10 seconds.

**Location:** `C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json`

### Step 5: Open Gmail

1. Go to [https://mail.google.com](https://mail.google.com)
2. The extension will automatically:
   - Fetch flagged emails from API every 10 seconds
   - Inject warning badges for emails with suspicious URLs
   - Block clicks on flagged emails
   - Show detailed modal with URLs and security recommendations

## 🔧 Files Overview

### Extension Files

| File | Purpose |
|------|---------|
| `manifest.json` | Extension configuration (permissions, content scripts) |
| `background.js` | Background service worker (fetches data every 10s) |
| `content.js` | Gmail DOM injection (warnings, badges, modals) |
| `styles.css` | Warning badge and modal styling |
| `popup.html` | Extension popup UI |
| `popup.js` | Popup functionality (stats, test API, refresh) |

### API Server Files

| File | Purpose |
|------|---------|
| `server.js` | Express API server serving JSON data |
| `package.json` | Node.js dependencies |

## 📡 API Endpoints

The server exposes these endpoints:

### GET /health
Health check endpoint
```json
{
  "status": "ok",
  "message": "Phishing Detector API Server is running",
  "timestamp": "2025-01-29T10:30:00.000Z"
}
```

### GET /api/emails
Returns only flagged emails (has_urls: true)
```json
{
  "success": true,
  "count": 4,
  "total_emails": 8,
  "emails": [...],
  "timestamp": "2025-01-29T10:30:00.000Z",
  "file_last_modified": "2025-01-29T10:29:45.000Z"
}
```

### GET /api/emails/all
Returns all emails (including safe ones)

### GET /api/stats
Returns statistics about the data
```json
{
  "success": true,
  "statistics": {
    "total_emails": 8,
    "flagged_emails": 4,
    "safe_emails": 4,
    "total_urls_found": 19,
    "file_last_modified": "2025-01-29T10:29:45.000Z",
    "file_size_bytes": 15234
  }
}
```

## 🎯 How It Works

### 1. Data Collection (UiPath)
- UiPath workflow extracts emails from Gmail via IMAP
- Saves to `emails_data.json` every 10 seconds
- Includes: sender, subject, body, URLs, timestamps

### 2. API Layer (Node.js)
- `server.js` reads `emails_data.json`
- Filters emails with URLs (`has_urls: true`)
- Serves data via REST API on port 3000

### 3. Background Polling (background.js)
- Fetches from API every 10 seconds
- Stores in `chrome.storage.local`
- Sends messages to Gmail tabs when data updates

### 4. UI Injection (content.js)
- Monitors Gmail DOM for email rows
- Matches `email_id` from API with Gmail data
- Injects warning badges with ⚠️ icon and URL count
- Blocks clicks on flagged emails
- Shows modal with detailed warnings

### 5. Visual Warnings (styles.css)
- Red gradient warning badges with pulse animation
- Red border on flagged email rows
- Modal overlay with email details and URLs
- Security recommendations

## 🧪 Testing

### Test API Connection
1. Click the extension icon in Chrome toolbar
2. Click "🔍 Test API Connection"
3. Should show: "✅ API Connected! Found X flagged emails."

### Test in Gmail
1. Open Gmail
2. Look for emails with warning badges: **⚠️ SUSPICIOUS URLs**
3. Try clicking a flagged email → Modal should block and show warning
4. Check browser console (F12) for logs: `🛡️ Phishing Detector Content Script Loaded`

### Test with UiPath Data
Your current `emails_data.json` has 8 emails, 4 with URLs:
- 2 from `vm.manish502@gmail.com` (contains `malware.testing.google.test`)
- 2 Google security alerts with multiple URLs

These should appear with warning badges in Gmail.

## 🐛 Troubleshooting

### Extension not loading warnings
1. Check if API server is running: `http://localhost:3000/health`
2. Check extension popup: Click icon → Shows count and last update
3. Open browser console (F12) → Look for `🛡️` logs
4. Make sure you're on `mail.google.com`

### API errors in popup
1. Verify `emails_data.json` exists at: `C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json`
2. Make sure UiPath workflow is running
3. Test API manually: Open `http://localhost:3000/api/emails` in browser

### Warnings not showing in Gmail
1. Refresh Gmail page
2. Check content.js is injected: Console should show `✅ Gmail loaded, initializing detector...`
3. Verify email has `email_id` attribute in Gmail DOM
4. Check flagged emails in popup: Click extension icon

### Server won't start
1. Check if port 3000 is already in use
2. Make sure Node.js is installed: `node --version`
3. Install dependencies: `npm install`

## 📊 Current Data Status

Based on your `emails_data.json`:
- **Total Emails:** 8
- **Flagged (has URLs):** 4
- **Safe:** 4
- **Total URLs Found:** 19

### Flagged Emails:
1. ✉️ From: vm.manish502@gmail.com - "test malware" (2 URLs including `malware.testing.google.test`)
2. ✉️ From: vm.manish502@gmail.com - "sent it" (1 URL)
3. ✉️ From: no-reply@accounts.google.com - "Security alert" (3 URLs)
4. ✉️ From: no-reply@accounts.google.com - "Security alert" (3 URLs)

## 🔄 Update Frequency

- **UiPath:** Generates JSON every **10 seconds**
- **Background.js:** Polls API every **10 seconds**
- **Content.js:** Re-injects warnings every **5 seconds** + on DOM changes

Total latency: ~15-20 seconds from email extraction to Gmail warning

## 🎨 Customization

### Change polling interval
**background.js** line 4:
```javascript
const REFRESH_INTERVAL = 10000; // Change to 5000 for 5 seconds
```

### Change warning badge color
**styles.css** line 8:
```css
background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); /* Red */
```

### Change API port
**server.js** line 8:
```javascript
const PORT = 3000; // Change to another port
```

Also update in **background.js** line 3 and **popup.js** line 4.

## 📝 Next Steps

1. ✅ Start API server: `npm start`
2. ✅ Load extension in Chrome
3. ✅ Open Gmail and test
4. 🔜 Add icon images (currently using default)
5. 🔜 Enhance phishing detection logic (friend's implementation)
6. 🔜 Add ML-based URL analysis

## 🎯 Credits

- **UiPath Workflow:** Email extraction via IMAP
- **API Server:** Express.js + CORS
- **Chrome Extension:** Manifest V3
- **Detection Logic:** URL-based flagging (friend's implementation pending)

---

**Made with ❤️ for Gmail Security**

For issues or questions, check the browser console and API server logs.
