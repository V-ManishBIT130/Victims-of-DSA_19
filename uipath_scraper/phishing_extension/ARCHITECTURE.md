# 🏗️ Phishing Detector - System Architecture

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHISHING DETECTION SYSTEM                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐      ┌──────────────────┐      ┌─────────────────────┐
│   Gmail IMAP    │      │  emails_data.json│      │   Node.js Server    │
│   📧 Server     │─────▶│  📄 File Storage │─────▶│   🌐 Express API    │
│                 │      │                  │      │   Port 3000         │
└─────────────────┘      └──────────────────┘      └─────────────────────┘
        ▲                        ▲                           │
        │                        │                           │
        │ IMAP                   │ Write                     │ HTTP GET
        │ Connection             │ Every 10s                 │ /api/emails
        │                        │                           │
┌───────┴────────┐      ┌────────┴──────────┐      ┌────────▼────────────┐
│   UiPath       │      │   UiPath Main     │      │  Chrome Extension   │
│   Workflow     │      │   Workflow        │      │  🛡️ Background.js   │
│                │      │   Main.xaml       │      │                     │
└────────────────┘      └───────────────────┘      └─────────────────────┘
                                                            │
                                                            │ Polls every
                                                            │ 10 seconds
                                                            │
                                                    ┌───────▼──────────┐
                                                    │ chrome.storage   │
                                                    │ .local           │
                                                    │ 💾 Cache        │
                                                    └───────┬──────────┘
                                                            │
                                                            │ Message
                                                            │ Passing
                                                            │
                                                    ┌───────▼──────────┐
                                                    │  Content.js      │
                                                    │  🎯 Gmail Tab    │
                                                    │                  │
                                                    └───────┬──────────┘
                                                            │
                                                            │ Inject
                                                            │ Warnings
                                                            │
                                                    ┌───────▼──────────┐
                                                    │  Gmail UI        │
                                                    │  ⚠️ Warnings    │
                                                    │  🔴 Badges      │
                                                    │  🚫 Modal       │
                                                    └──────────────────┘
```

---

## 🔄 Process Flow

### Phase 1: Email Extraction (UiPath)
```
1. Connect to Gmail via IMAP
   └─▶ Login: phishingdemo65@gmail.com
       └─▶ Port: 993 (SSL)

2. For each email:
   ├─▶ Extract metadata (sender, subject, date)
   ├─▶ Extract body content
   ├─▶ Find URLs using regex: https?://[^\s<>"']+
   └─▶ Build JSON object with 12 properties

3. Write to file:
   └─▶ C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json

4. Wait 10 seconds → Repeat
```

### Phase 2: API Server (Node.js)
```
1. Start Express server on port 3000

2. On GET /api/emails:
   ├─▶ Read emails_data.json
   ├─▶ Filter: has_urls === true
   ├─▶ Return JSON response:
   │   {
   │     success: true,
   │     count: 4,
   │     emails: [...],
   │     timestamp: "2025-01-29T10:30:00Z"
   │   }
   └─▶ Log request

3. Keep running (listen for requests)
```

### Phase 3: Background Polling (Extension)
```
1. Start interval timer (10 seconds)

2. Every 10 seconds:
   ├─▶ Fetch http://localhost:3000/api/emails
   ├─▶ Parse JSON response
   ├─▶ Save to chrome.storage.local:
   │   {
   │     flaggedEmails: [...],
   │     lastUpdate: timestamp,
   │     totalCount: 4
   │   }
   ├─▶ Query all Gmail tabs
   └─▶ Send message: { action: 'updateWarnings', emails, count }

3. Listen for messages:
   ├─▶ forceRefresh → Fetch immediately
   └─▶ getLatestData → Return from storage
```

### Phase 4: UI Injection (Content Script)
```
1. Wait for Gmail to load

2. Load flagged emails from chrome.storage.local

3. Start MutationObserver on Gmail DOM

4. When emails detected:
   ├─▶ Find all email rows (tr.zA, tr[role="row"])
   ├─▶ For each row:
   │   ├─▶ Extract email_id attribute
   │   ├─▶ Check if email_id in flaggedEmails
   │   ├─▶ If flagged:
   │   │   ├─▶ Inject warning badge
   │   │   ├─▶ Add red border
   │   │   ├─▶ Block click events
   │   │   └─▶ Attach modal trigger
   │   └─▶ Continue to next row
   └─▶ Log: "✅ Injected X warnings"

5. On flagged email click:
   ├─▶ Prevent default action
   ├─▶ Show modal overlay with:
   │   ├─▶ Email details
   │   ├─▶ List of URLs
   │   ├─▶ Security recommendations
   │   └─▶ Close button
   └─▶ Wait for user action

6. Re-inject every 5 seconds (Gmail may remove elements)
```

---

## 📦 Component Details

### UiPath Workflow (Main.xaml)
- **Input:** Gmail IMAP credentials
- **Processing:**
  - Deserialize config.json
  - Connect to Gmail
  - For Each Email:
    - Extract fields
    - Regex URL extraction
    - Build JSON object
  - Serialize to JSON array
  - Write to file
- **Output:** emails_data.json (updated every 10s)

### Node.js API Server (server.js)
- **Framework:** Express.js
- **Middleware:** CORS (allow Chrome extension)
- **Endpoints:**
  - `GET /health` → Health check
  - `GET /api/emails` → Flagged emails only
  - `GET /api/emails/all` → All emails
  - `GET /api/stats` → Statistics
- **Logic:** Read file → Filter → Return JSON

### Chrome Extension Background Script (background.js)
- **Type:** Service Worker (Manifest V3)
- **Polling:** setInterval(10000ms)
- **Storage:** chrome.storage.local
- **Messaging:** chrome.tabs.sendMessage
- **Backup:** chrome.alarms (in case interval fails)

### Chrome Extension Content Script (content.js)
- **Injection:** Automatic on mail.google.com
- **Timing:** document_idle
- **Selectors:**
  - Email rows: `tr.zA, tr[role="row"]`
  - Email ID: `data-legacy-message-id`
  - Subject: `.bog, .a4W, .y6`
- **Events:**
  - MutationObserver for DOM changes
  - Click capture on flagged rows
- **UI Elements:**
  - Warning badge (inline element)
  - Modal overlay (full-screen popup)

### Styling (styles.css)
- **Badge:** Red gradient, pulse animation
- **Modal:** Dark overlay, white card, slide-up animation
- **Row highlight:** Red border, yellow background
- **Responsive:** Works with Gmail's fluid layout

---

## 🔌 Integration Points

### 1. UiPath ↔ File System
```
Interface: File Write
Format: JSON (UTF-8)
Frequency: Every 10 seconds
Path: C:\Users\V Manish\Desktop\uipath_scraper\emails_data.json
```

### 2. File System ↔ API Server
```
Interface: File Read (fs.readFileSync)
Format: JSON parsing
Trigger: On HTTP request
Error Handling: 404 if file missing, 500 if parse error
```

### 3. API Server ↔ Extension
```
Interface: HTTP REST API
Protocol: HTTP/1.1
Port: 3000
CORS: Enabled for chrome-extension://
Authentication: None (localhost only)
Response: JSON with {success, count, emails, timestamp}
```

### 4. Background Script ↔ Storage
```
Interface: chrome.storage.local API
Data: {flaggedEmails: Array, lastUpdate: String, totalCount: Number}
Size Limit: 5MB (Chrome default)
Persistence: Across browser sessions
```

### 5. Background Script ↔ Content Script
```
Interface: chrome.runtime.sendMessage
Direction: Background → Content
Message: {action: 'updateWarnings', emails: Array, count: Number}
Trigger: After successful API fetch
```

### 6. Content Script ↔ Gmail DOM
```
Interface: DOM manipulation (vanilla JS)
Injection: Dynamic element creation
Selectors: Gmail-specific classes (tr.zA, .bog, etc.)
Observer: MutationObserver on [role="main"]
Events: Click capture with stopPropagation
```

---

## ⏱️ Timing Diagram

```
Time    UiPath          API Server      Background.js    Content.js       Gmail UI
────────────────────────────────────────────────────────────────────────────────
0:00    Extract emails  Idle            Idle             Idle             Normal
0:10    Write JSON      Idle            Poll API ────▶   Receive message  Inject
        ▼               ▼ Read file                      ▼                warnings
        ▼               ▼ Filter                         ▼                ⚠️
0:15    Extract emails  ▼ Return JSON   Store data       Update DOM       
0:20    Write JSON      Idle            Poll API ────▶   Receive message  Update
0:30    Write JSON      Idle            Poll API ────▶   Receive message  Update
...     (repeat)        (on-demand)     (every 10s)      (every 5s)       (live)
```

**Total Latency:** ~15-20 seconds from email extraction to warning display

---

## 🛡️ Security Considerations

### Current Implementation
- ✅ CORS enabled (necessary for extension communication)
- ✅ localhost-only API (no external exposure)
- ✅ No sensitive data in API responses (email content only)
- ✅ Click blocking on flagged emails
- ✅ XSS protection (escapeHtml function)

### Future Enhancements
- 🔜 Add API authentication (API key)
- 🔜 Encrypt sensitive email content
- 🔜 Rate limiting on API
- 🔜 HTTPS for API (if deployed remotely)

---

## 📈 Scalability

### Current Limits
- **Emails:** ~100-200 emails max (JSON file size)
- **Polling:** Every 10 seconds (6 requests/minute)
- **Storage:** 5MB Chrome storage limit
- **Performance:** Gmail DOM injection ~100-500ms

### Scaling Options
1. **Database:** Replace JSON file with MongoDB/PostgreSQL
2. **WebSocket:** Replace polling with real-time push
3. **Pagination:** API returns paginated results
4. **Caching:** Add Redis for faster reads
5. **Queue:** Use RabbitMQ for email processing

---

This architecture is designed for **real-time phishing detection** with minimal latency
and maximum user experience in Gmail! 🚀
