# 🎨 Visual Indicator System - Setup Guide

## Overview
The Chrome extension now displays **colored dots** (🔴 Red, 🟡 Yellow, 🟢 Green) next to emails in Gmail based on ML confidence scores.

## Color Coding System

### 🔴 RED DOT (Critical Threat)
- **Confidence:** 80-100%
- **Meaning:** High probability of phishing
- **Action:** DELETE IMMEDIATELY

### 🟡 YELLOW DOT (Warning)
- **Confidence:** 50-79%
- **Meaning:** Suspicious, needs caution
- **Action:** Review carefully before clicking

### 🟢 GREEN DOT (Safe)
- **Confidence:** 0-49% OR Legitimate
- **Meaning:** Low risk or verified safe
- **Action:** Proceed normally (but always stay vigilant)

## Hover Tooltip Features

When you hover over any colored dot, you'll see a detailed tooltip showing:

1. **Confidence Percentage** - How confident the AI is
2. **Risk Score** - Numerical risk rating (0-100)
3. **Threat Level** - CRITICAL, HIGH, MEDIUM, LOW, SAFE
4. **Verdict** - PHISHING or LEGITIMATE
5. **Red Flags** - Security issues detected (if any)
6. **Recommendations** - What actions to take

## Setup Instructions

### Step 1: Make Sure Server is Running
```powershell
cd "c:\Users\HR Lithesh\OneDrive\Desktop\Phising ml\uipath_scraper\phishing_extension"
node server.js
```

You should see:
```
✅ Server running on http://localhost:3000
✅ phishing_results.json found
```

### Step 2: Reload Chrome Extension
1. Open Chrome: `chrome://extensions/`
2. Find "Phishing Email Detector"
3. Click the **Reload** button (🔄)

### Step 3: Refresh Gmail
1. Open Gmail: https://mail.google.com
2. Press **Ctrl + F5** (hard refresh)
3. Wait 10 seconds for data to load

### Step 4: Check Console (Optional)
1. Right-click on Gmail page → **Inspect**
2. Go to **Console** tab
3. You should see:
   ```
   🛡️ Phishing Detector Content Script Loaded
   ✅ Gmail detected and ready
   📊 Processing 5 flagged emails
   ```

## Visual Examples

### In Gmail Inbox:
```
┌─────────────────────────────────────────┐
│ 🔴 vm.manish502@gmail.com               │ ← RED dot = Phishing (97% confident)
│    Fwd: hello                           │
├─────────────────────────────────────────┤
│ 🟡 hrlithesh05@gmail.com                │ ← YELLOW dot = Suspicious (57% confident)
│    testingg                             │
├─────────────────────────────────────────┤
│ 🟢 info@mail.uipath.com                 │ ← GREEN dot = Safe (37% confident)
│    You're in! What's next...            │
└─────────────────────────────────────────┘
```

### Hover Tooltip Example:
```
┌─────────────────────────────────────────┐
│  ⚠️  CRITICAL                           │ ← Red header
├─────────────────────────────────────────┤
│  Confidence:      97.7%                 │
│  Risk Score:      58/100                │
│  Threat Level:    HIGH                  │
│  Verdict:         PHISHING              │
│                                         │
│  🚩 Red Flags:                          │
│    • HIGH: Domain mismatch              │
│                                         │
│  🎯 Recommendations:                    │
│    • CRITICAL: DELETE IMMEDIATELY       │
│    • CRITICAL: DO NOT CLICK ANY LINKS   │
│    • HIGH: Report as phishing/spam      │
└─────────────────────────────────────────┘
```

## Troubleshooting

### ❌ No Dots Showing
**Problem:** Extension loaded but no colored dots appear

**Solutions:**
1. Check server is running: `http://localhost:3000/api/emails`
2. Verify phishing_results.json exists with data
3. Hard refresh Gmail: **Ctrl + Shift + R**
4. Check console for errors: **F12** → Console tab

### ❌ Server Not Running
**Problem:** "Failed to fetch emails" in console

**Solution:**
```powershell
cd "c:\Users\HR Lithesh\OneDrive\Desktop\Phising ml\uipath_scraper\phishing_extension"
node server.js
```

### ❌ Old Data Showing
**Problem:** Dots showing outdated predictions

**Solution:**
```powershell
# Re-run the ML model
cd "c:\Users\HR Lithesh\OneDrive\Desktop\Phising ml\uipath_scraper"
python process_emails.py
```

### ❌ Extension Context Invalidated
**Problem:** Extension stopped working after reload

**Solution:**
1. Reload extension in `chrome://extensions/`
2. Close and reopen Gmail tabs
3. Wait 10 seconds for reconnection

## Technical Details

### Files Modified:
- ✅ `server.js` - Updated to read new phishing_results.json format
- ✅ `content.js` - New dot indicator injection system
- ✅ `styles.css` - New dot styles with animations and tooltips
- ✅ `background.js` - No changes needed

### Data Flow:
```
phishing_results.json (ML output)
         ↓
   server.js (API)
         ↓
   background.js (Fetch every 10s)
         ↓
   content.js (Inject dots)
         ↓
   Gmail UI (Visual indicators)
```

### Color Determination Logic:
```javascript
if (!email.is_phishing) {
  color = GREEN (Safe)
} else if (confidence >= 80%) {
  color = RED (Critical)
} else if (confidence >= 50%) {
  color = YELLOW (Warning)
} else {
  color = GREEN (Low Risk)
}
```

## Testing

### Test with Current Data:
You have 11 emails analyzed:
- **5 Phishing** (will show RED 🔴 or YELLOW 🟡)
- **6 Legitimate** (will show GREEN 🟢)

### Expected Results:
| Email Subject | Sender | Expected Color | Confidence |
|--------------|--------|----------------|------------|
| Fwd: hello | vm.manish502 | 🔴 RED | 97.7% |
| hello | vm.manish502 | 🔴 RED | 99.98% |
| testingg | hrlithesh05 | 🔴 RED | 99.96% |
| hello lithesh | dhanushvmodiliay | 🔴 RED | 99.96% |
| As it was | vm.manish502 | 🟡 YELLOW | 57.04% |
| You're in! | uipath.com | 🟢 GREEN | 37.51% |

## Next Steps

1. ✅ **Server Running** - Keep it running in background
2. ✅ **Extension Loaded** - Reload if needed
3. ✅ **Monitor Working** - Process new emails automatically
4. 🎯 **Test in Gmail** - Check colored dots appear
5. 🎯 **Hover to Test** - Verify tooltips show details

## Support

If you encounter issues:
1. Check server logs in terminal
2. Check browser console (F12)
3. Verify phishing_results.json has data
4. Ensure all files are saved

---

**Created:** November 7, 2025  
**System Status:** ✅ Ready for testing
