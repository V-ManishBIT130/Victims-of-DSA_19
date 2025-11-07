# 🚀 Quick Setup Guide - Phishing Detector Extension

## ⚡ 3-Step Quick Start

### Step 1: Install Dependencies (1 minute)
```powershell
cd "C:\Users\V Manish\Desktop\phishing_extension"
npm install
```

### Step 2: Start API Server (Keep Running!)
```powershell
npm start reset
```

**Expected Output:**
```
🛡️  PHISHING DETECTOR API SERVER
✅ Server running on http://localhost:3000
📂 Monitoring file: C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json
✅ emails_data.json found
```

### Step 3: Load Extension in Chrome
1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (top-right toggle)
3. Click "Load unpacked"
4. Select: `C:\Users\V Manish\Desktop\phishing_extension`
5. Done! ✅

---

## ✅ Verification Checklist

### 1. API Server Running?
Open in browser: http://localhost:3000/health

Should show:
```json
{
  "status": "ok",
  "message": "Phishing Detector API Server is running"
}
```

### 2. Extension Loaded?
- Look for extension icon in Chrome toolbar (shield icon)
- Click it → Should show "Active - Monitoring Gmail"
- Should show count of flagged emails

### 3. Gmail Integration Working?
1. Open Gmail: https://mail.google.com
2. Look for warning badges: **⚠️ SUSPICIOUS URLs**
3. Press F12 → Console → Should see: `🛡️ Phishing Detector Content Script Loaded`
4. Should see: `✅ Gmail loaded, initializing detector...`

### 4. UiPath Running?
Check if file exists and is updating:
```powershell
Get-Item "C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json" | Select-Object LastWriteTime
```

Should show recent timestamp (within last 10 seconds).

---

## 🎯 Testing the Full Flow

### Test 1: API Connection
1. Click extension icon
2. Click "🔍 Test API Connection"
3. Should show: "✅ API Connected! Found X flagged emails"

### Test 2: Gmail Warnings
1. Open Gmail
2. Look at inbox
3. Emails with URLs should have red badges
4. Click on a flagged email → Modal should block and show warning

### Test 3: Real-time Updates
1. Keep Gmail open
2. Add new email with URLs in your inbox
3. Wait ~15-20 seconds
4. Warning should appear automatically

---

## 🐛 Troubleshooting

### Problem: "API Error" in extension popup
**Solution:**
```powershell
# Check if server is running
curl http://localhost:3000/health

# If not running, start it:
npm start
```

### Problem: No warnings in Gmail
**Solution:**
1. Refresh Gmail page (Ctrl+R)
2. Check browser console (F12) for errors
3. Verify emails have URLs in `emails_data.json`
4. Make sure you're on `mail.google.com` (not another Gmail domain)

### Problem: Extension not loading
**Solution:**
1. Go to `chrome://extensions/`
2. Check for error messages under the extension
3. Click "Reload" button
4. Check "Developer mode" is enabled

### Problem: UiPath data not updating
**Solution:**
1. Check UiPath workflow is running
2. Verify file path: `C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json`
3. Check file permissions (should be writable)

---

## 📊 Current Status of Your Data

Based on `emails_data.json` you have:
- **8 total emails**
- **4 flagged emails** (with URLs)
- **19 total URLs** found

### These emails will show warnings:
1. ✉️ "test malware" from vm.manish502@gmail.com
   - ⚠️ Contains: `malware.testing.google.test`
   
2. ✉️ "sent it" from vm.manish502@gmail.com
   - ⚠️ Contains: 1 URL

3. ✉️ Google Security Alert #1
   - ⚠️ Contains: 3 URLs

4. ✉️ Google Security Alert #2
   - ⚠️ Contains: 3 URLs

---

## 🔧 Configuration

### Change Update Frequency

**Make it faster (5 seconds):**

Edit `background.js` line 4:
```javascript
const REFRESH_INTERVAL = 5000; // was 10000
```

Edit `server.js` - no changes needed (reads file on every request)

**Make it slower (30 seconds):**
```javascript
const REFRESH_INTERVAL = 30000;
```

### Change API Port

If port 3000 is busy, change to 3001:

1. **server.js** line 8: `const PORT = 3001;`
2. **background.js** line 3: `const API_URL = 'http://localhost:3001/api/emails';`
3. **popup.js** line 4: `const API_URL = 'http://localhost:3001/api/emails';`
4. **manifest.json** line 18: `"http://localhost:3001/*"`

Then restart server and reload extension.

---

## 📝 Files Structure

```
phishing_extension/
│
├── manifest.json          # Extension config
├── background.js          # Background worker (polling)
├── content.js             # Gmail injection script
├── styles.css             # Warning styles
├── popup.html             # Extension popup UI
├── popup.js               # Popup logic
├── server.js              # API server
├── package.json           # Node dependencies
├── README.md              # Full documentation
├── SETUP.md               # This file
│
└── icons/
    ├── icon16.svg         # 16x16 icon
    ├── icon48.svg         # 48x48 icon
    └── icon128.svg        # 128x128 icon
```

---

## 🎯 What Happens When You Start?

### 1. UiPath (Already Running)
```
Every 10 seconds:
  → Connect to Gmail IMAP
  → Extract new emails
  → Parse URLs from body
  → Save to emails_data.json
```

### 2. API Server (server.js)
```
On start:
  → Listen on port 3000
  → Monitor emails_data.json

On request to /api/emails:
  → Read emails_data.json
  → Filter emails with has_urls: true
  → Return flagged emails as JSON
```

### 3. Chrome Extension (background.js)
```
Every 10 seconds:
  → Fetch http://localhost:3000/api/emails
  → Store in chrome.storage.local
  → Send message to Gmail tabs
```

### 4. Gmail Page (content.js)
```
On Gmail load:
  → Wait for Gmail DOM ready
  → Load flagged emails from storage
  → Find email rows in DOM
  → Match email_id
  → Inject warning badges
  → Add click blockers
  → Show modal on click

On DOM changes:
  → Re-scan for new emails
  → Re-inject warnings
```

---

## 🚀 Ready to Go!

**Terminal 1:** (Keep running)
```powershell
cd "C:\Users\V Manish\Desktop\phishing_extension"
npm start
```

**Chrome:**
1. Load extension from `chrome://extensions/`
2. Open Gmail
3. Watch for warnings! ⚠️

---

## 📞 Need Help?

### Check Logs

**Browser Console (F12):**
- Should see: `🛡️ Phishing Detector Content Script Loaded`
- Should see: `✅ Gmail loaded, initializing detector...`
- Should see: `📧 Loaded X flagged emails from storage`

**Server Terminal:**
- Should see: `✅ Served X flagged emails`
- Should update every 10 seconds when extension polls

### Test Each Component

```powershell
# Test 1: File exists
Test-Path "C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json"
# Should return: True

# Test 2: API responds
curl http://localhost:3000/health
# Should return: {"status":"ok",...}

# Test 3: Get flagged emails
curl http://localhost:3000/api/emails
# Should return: {"success":true,"count":4,...}
```

---

**You're all set! Open Gmail and see the magic happen! ✨**
