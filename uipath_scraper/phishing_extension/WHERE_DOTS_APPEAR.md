# 🎨 VISUAL GUIDE - Where Colored Dots Appear in Gmail

## Exact Placement in Gmail UI

The colored dots will appear **TO THE LEFT** of the sender's name in your Gmail inbox.

```
BEFORE (No Extension):
┌────────────────────────────────────────────────────────┐
│   vm.manish502@gmail.com                       7:40 AM │
│   Fwd: hello                                           │
└────────────────────────────────────────────────────────┘

AFTER (With Extension):
┌────────────────────────────────────────────────────────┐
│ 🔴  vm.manish502@gmail.com                     7:40 AM │  ← RED dot appears here
│     Fwd: hello                                         │
│ ▌   Light pink background                             │  ← Row gets colored
└────────────────────────────────────────────────────────┘
```

---

## Full Gmail Inbox View

```
┌──────────────────────────────────────────────────────────────────┐
│  Gmail                              [Search]         [Settings]  │
├──────────────────────────────────────────────────────────────────┤
│  [☰] [✎ Compose]                                                 │
├──────────────────────────────────────────────────────────────────┤
│  📥 Primary    Social (14 new)    Promotions (47 new)            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  [ ] ★  🔴 vm.manish502@gmail.com             •        7:40 AM   │  ← RED DOT (Phishing HIGH)
│         Fwd: hello                                                │
│  ▌      do you want money                                        │  ← Pink background
│                                                                   │
│  [ ] ★  🔴 vm.manish502@gmail.com             •        7:40 AM   │  ← RED DOT (Phishing HIGH)
│         hello                                                     │
│  ▌      do you want money                                        │  ← Pink background
│                                                                   │
│  [ ] ★  🔴 hrlithesh05@gmail.com              •        7:40 AM   │  ← RED DOT (Phishing HIGH)
│         testingg                                                  │
│  ▌      testing 1                                                │  ← Pink background
│                                                                   │
│  [ ] ★  🔴 dhanushvmodiliay@gmail.com         •        7:40 AM   │  ← RED DOT (Phishing HIGH)
│         hello lithesh                                             │
│  ▌      happy new

 year                                           │  ← Pink background
│                                                                   │
│  [ ] ★  🟡 vm.manish502@gmail.com             •        7:40 AM   │  ← YELLOW DOT (Suspicious LOW)
│         As it was - subject                                       │
│  ▌      https://open.spotify.com/track...                        │  ← Yellow background
│                                                                   │
│  [ ] ★  🟢 info@mail.uipath.com               •        7:40 AM   │  ← GREEN DOT (Safe)
│         You're in! What's next for your UiPath journey?           │
│         Welcome to UiPath! Here's how to get started...          │  ← Normal background
│                                                                   │
│  [ ] ★  🟢 dhanushvmodiliay@gmail.com         •        7:40 AM   │  ← GREEN DOT (Safe)
│         (No Subject)                                              │
│         hi lets meet                                              │  ← Normal background
│                                                                   │
│  [ ] ★  🟢 vm.manish502@gmail.com             •        7:40 AM   │  ← GREEN DOT (Safe)
│         subject with a url                                        │
│         https://github.com/Click2Hack/Phishing-Email...          │  ← Normal background
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

Legend:
[ ] = Checkbox
★ = Star/Important marker
🔴 = RED dot (DANGER - Phishing HIGH/CRITICAL)
🟡 = YELLOW dot (WARNING - Phishing LOW/MEDIUM)
🟢 = GREEN dot (SAFE - Legitimate)
▌ = Colored left border (3px)
• = Unread indicator
```

---

## Hover Tooltip Position

When you hover over a dot, tooltip appears to the RIGHT:

```
Your mouse here
      ↓
     🔴 vm.manish502@gmail.com          ┌─────────────────────────────┐
         Fwd: hello                     │  ⚠️  HIGH                   │
                                        ├─────────────────────────────┤
                                        │  Confidence:      97.7%     │
                                        │  Risk Score:      58/100    │
                                        │  Threat Level:    HIGH      │
                                        │  Verdict:         PHISHING  │
                                        │                             │
                                        │  🎯 Recommendations:        │
                                        │    CRITICAL: DELETE NOW     │
                                        │    DO NOT CLICK ANY LINKS   │
                                        └─────────────────────────────┘
                                              ↑
                                        Tooltip appears here
```

---

## Dot Size & Animation

### RED DOT (Phishing):
- Size: 14px × 14px
- Color: #dc3545 (red)
- Border: 2px white
- Animation: Pulsing glow effect (every 2 seconds)
- Shadow: Subtle drop shadow

### YELLOW DOT (Suspicious):
- Size: 14px × 14px
- Color: #ffc107 (yellow/orange)
- Border: 2px white
- Animation: Light pulse
- Shadow: Subtle drop shadow

### GREEN DOT (Safe):
- Size: 14px × 14px
- Color: #28a745 (green)
- Border: 2px white
- Animation: None (static)
- Shadow: Subtle drop shadow

---

## Row Highlighting

### HIGH Threat (RED dot):
- Background: #fff5f5 (very light pink)
- Left Border: 3px solid red (#dc3545)
- Effect: Draws attention without being overwhelming

### LOW Threat (YELLOW dot):
- Background: #fffef5 (very light yellow)
- Left Border: 3px solid yellow (#ffc107)
- Effect: Subtle warning

### SAFE (GREEN dot):
- Background: Normal (no change)
- Left Border: None
- Effect: No visual alarm needed

---

## Technical Details

### CSS Classes Applied:

1. **Dot Container:**
   ```css
   .phishing-dot-indicator {
     position: relative;
     display: inline-flex;
     margin-right: 12px;
     margin-left: 8px;
   }
   ```

2. **Dot Element:**
   ```css
   .phishing-dot {
     width: 14px;
     height: 14px;
     border-radius: 50%;
     border: 2px solid white;
     box-shadow: 0 2px 6px rgba(0,0,0,0.3);
   }
   ```

3. **Color Classes:**
   - `.dot.critical` → Red (#dc3545)
   - `.dot.warning` → Yellow (#ffc107)
   - `.dot.safe` → Green (#28a745)

---

## Injection Point in Gmail DOM

The dot is inserted into the Gmail email row at this location:

```html
<tr class="zA yO"> <!-- Gmail email row -->
  <td>
    <!-- Checkbox -->
  </td>
  <td>
    <!-- Star icon -->
  </td>
  <td class="yX xY"> <!-- Sender column -->
    
    <!-- OUR DOT GETS INJECTED HERE ↓ -->
    <div class="phishing-dot-indicator">
      <div class="phishing-dot critical">
        <div class="dot-pulse"></div>
      </div>
      <div class="phishing-tooltip" style="display:none;">
        <!-- Tooltip content -->
      </div>
    </div>
    <!-- OUR DOT INJECTION ENDS HERE ↑ -->
    
    <span class="yW">
      <span>vm.manish502@gmail.com</span>
    </span>
  </td>
  <!-- Subject column -->
  <!-- Date column -->
</tr>
```

---

## Expected Behavior

### On Page Load:
1. Extension waits for Gmail to fully load
2. Fetches data from server (localhost:3000)
3. Finds all email rows in DOM
4. Matches emails by email_id
5. Injects colored dots
6. Applies row highlighting

### Every 10 Seconds:
1. Background script fetches fresh data
2. Sends update message to content script
3. Content script re-processes email rows
4. Updates dots if data changed

### On Hover:
1. Mouse enters dot area
2. Tooltip display set to 'block'
3. Tooltip positioned to the right
4. Tooltip stays visible while hovering

### On Mouse Leave:
1. Mouse exits dot area
2. Tooltip display set to 'none'
3. Tooltip hidden

---

## Color Decision Logic

```javascript
if (threat_level === 'SAFE') {
  color = GREEN
} else if (threat_level === 'CRITICAL' || threat_level === 'HIGH') {
  color = RED
} else if (threat_level === 'MEDIUM' || threat_level === 'LOW') {
  color = YELLOW
} else {
  // Fallback based on is_phishing
  color = is_phishing ? RED : GREEN
}
```

---

## Verification Steps

After reloading extension and refreshing Gmail:

1. ✅ Look for colored dots to the LEFT of sender names
2. ✅ Count dots: Should see 12 dots total (5 red, 1 yellow, 6 green)
3. ✅ Check row highlighting: Red/yellow emails have colored backgrounds
4. ✅ Hover over a dot: Tooltip should appear to the right
5. ✅ Check console: Should show "Processing 12 flagged emails"

---

## Screenshot Comparison

Your Gmail should look similar to this:

```
INBOX VIEW:
┌─────────────────────────────────────┐
│  🔴 Sender 1     HIGH      7:40 AM  │  ← Phishing email (pink)
│  🔴 Sender 2     HIGH      7:40 AM  │  ← Phishing email (pink)
│  🔴 Sender 3     HIGH      7:40 AM  │  ← Phishing email (pink)
│  🔴 Sender 4     HIGH      7:40 AM  │  ← Phishing email (pink)
│  🟡 Sender 5     LOW       7:40 AM  │  ← Suspicious email (yellow)
│  🟢 Sender 6     SAFE      7:40 AM  │  ← Safe email (normal)
│  🟢 Sender 7     SAFE      7:40 AM  │  ← Safe email (normal)
│  🟢 Sender 8     SAFE      7:40 AM  │  ← Safe email (normal)
└─────────────────────────────────────┘
```

**NOT in terminal - these colors appear IN GMAIL WEBSITE!**

---

**Last Updated:** November 7, 2025 - 8:00 AM  
**Status:** Ready for testing  
**Action Required:** Reload Chrome extension and refresh Gmail!
