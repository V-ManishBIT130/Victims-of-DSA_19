// Gmail Phishing Detector Extension - CLEAN VERSION
console.log("🛡️ Gmail Phishing Detector Extension Started!");

let flaggedEmailsCache = [];
let extensionActive = true;

// Statistics tracking
let stats = {
  totalEmails: 0,
  phishingEmails: 0,
  safeEmails: 0,
  circlesAdded: 0
};

// Check if extension context is valid
function isExtensionValid() {
  try {
    if (!chrome.runtime || !chrome.runtime.id) {
      extensionActive = false;
      return false;
    }
    return extensionActive;
  } catch (e) {
    extensionActive = false;
    return false;
  }
}

// Load flagged emails from storage FIRST
loadFlaggedEmailsFromStorage();

// Wait for Gmail to fully load - EXACTLY LIKE INSPIRATION
setTimeout(() => {
  console.log("🔍 Looking for email rows...");
  injectCirclesOnAllRows();
}, 3000); // Wait 3 seconds for Gmail to load

// MAIN FUNCTION: Inject circles on ALL rows - EXACTLY LIKE INSPIRATION
function injectCirclesOnAllRows() {
  // Find all email rows (EXACTLY LIKE INSPIRATION)
  const allRows = document.querySelectorAll("tr");
  console.log(`📧 Found ${allRows.length} total rows in Gmail`);

  // Filter for actual email rows (EXACTLY LIKE INSPIRATION)
  const emailRows = Array.from(allRows).filter((row) => {
    return row.querySelector("td") && row.querySelector("span");
  });

  console.log(`✉️ Found ${emailRows.length} email rows`);

  if (emailRows.length === 0) {
    console.log("❌ No email rows found!");
    return;
  }

  // Reset stats
  stats = {
    totalEmails: emailRows.length,
    phishingEmails: 0,
    safeEmails: 0,
    circlesAdded: 0
  };

  // Add circle to each row (EXACTLY LIKE INSPIRATION)
  emailRows.forEach((row, index) => {
    // REMOVE old circles first!
    const oldCircle = row.querySelector(".phishing-threat-circle");
    if (oldCircle) {
      oldCircle.remove();
    }

    // Make row position relative for absolute positioning
    row.style.position = "relative";

    // Try to extract email info from the row
    let sender = "";
    let subject = "";
    
    // Extract sender email
    const senderSpan = row.querySelector('span[email]');
    if (senderSpan) {
      sender = senderSpan.getAttribute('email') || senderSpan.textContent.trim();
    }
    
    // Extract subject
    const subjectSpan = row.querySelector('span.bog, span[data-thread-id]');
    if (subjectSpan) {
      subject = subjectSpan.textContent.trim();
    }

    // Try to find in cache by sender OR subject
    let emailData = null;
    if (flaggedEmailsCache.length > 0 && (sender || subject)) {
      emailData = flaggedEmailsCache.find((e) => {
        // Match by sender email
        if (sender && e.sender && e.sender.toLowerCase().includes(sender.toLowerCase())) {
          return true;
        }
        // Match by subject
        if (subject && e.subject && e.subject.toLowerCase() === subject.toLowerCase()) {
          return true;
        }
        return false;
      });
      
      // Debug log
      if (emailData) {
        console.log(`✅ Row ${index}: MATCHED - sender="${sender}" subject="${subject}"`);
      } else {
        console.log(`⚠️ Row ${index}: NOT MATCHED - sender="${sender}" subject="${subject}"`);
      }
    }

    // Create the circle
    injectWarningBadge(row, emailData, index);

    stats.circlesAdded++;
  });

  // Log final statistics - CLEAR AND DETAILED
  console.log("\n🎉 ========================================");
  console.log("✅ CIRCLE INJECTION COMPLETE!");
  console.log("========================================");
  console.log(`📊 Total Email Rows Found: ${stats.totalEmails}`);
  console.log(`✅ Total Circles Added: ${stats.circlesAdded}`);
  console.log("\n📈 PHISHING DETECTION STATISTICS:");
  console.log(`  🔴 PHISHING DETECTED: ${stats.phishingEmails} emails`);
  console.log(`  🟢 SAFE EMAILS: ${stats.safeEmails} emails`);
  console.log(`  ⚪ UNKNOWN/PENDING: ${stats.totalEmails - stats.phishingEmails - stats.safeEmails} emails`);
  console.log("\n💡 Summary:");
  if (stats.phishingEmails > 0) {
    console.log(`  ⚠️ WARNING: ${stats.phishingEmails} phishing email(s) found in your inbox!`);
  } else {
    console.log(`  ✅ No phishing emails detected. Your inbox looks safe!`);
  }
  console.log("========================================\n");
}


// Load flagged emails from Chrome storage
function loadFlaggedEmailsFromStorage() {
  if (!isExtensionValid()) {
    console.log('⚠️ Extension context invalid, cannot load storage');
    return;
  }
  
  try {
    chrome.storage.local.get(['flaggedEmails', 'totalEmails', 'serverOnline'], (result) => {
      if (!isExtensionValid()) return;
      
      if (chrome.runtime.lastError) {
        console.error('❌ Storage error:', chrome.runtime.lastError.message);
        return;
      }
      
      if (result.flaggedEmails) {
        flaggedEmailsCache = result.flaggedEmails;
        
        console.log('\n📦 ========================================');
        console.log('📦 LOADED DATA FROM STORAGE');
        console.log('========================================');
        console.log(`📊 Total emails in cache: ${flaggedEmailsCache.length}`);
        console.log(`📧 Total emails monitored: ${result.totalEmails || 0}`);
        console.log(`🌐 Server online: ${result.serverOnline ? '✅ YES' : '❌ NO'}`);
        
        if (flaggedEmailsCache.length > 0) {
          console.log('\n📋 Sample email structure:');
          console.log(JSON.stringify(flaggedEmailsCache[0], null, 2));
          
          console.log('\n📋 ALL EMAIL SENDERS AND SUBJECTS:');
          flaggedEmailsCache.slice(0, 5).forEach((e, i) => {
            console.log(`  [${i}] sender: "${e.sender}" | subject: "${e.subject}" | is_phishing: ${e.is_phishing}`);
          });
          
          // Count phishing vs safe
          const phishingCount = flaggedEmailsCache.filter(e => e.is_phishing === true).length;
          const safeCount = flaggedEmailsCache.filter(e => e.is_phishing === false).length;
          
          console.log('\n📊 Email Classification Breakdown:');
          console.log(`  🔴 Phishing: ${phishingCount}`);
          console.log(`  🟢 Safe: ${safeCount}`);
          console.log(`  ⚪ Other: ${flaggedEmailsCache.length - phishingCount - safeCount}`);
        }
        console.log('========================================\n');
      } else {
        console.log('⏳ No data in storage yet, waiting for server...');
      }
    });
  } catch (error) {
    console.error('❌ Error loading from storage:', error.message);
  }
}

// Listen for messages from background script
if (isExtensionValid()) {
  try {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (!isExtensionValid()) {
        return false;
      }
      
      if (message.action === 'updateWarnings') {
        flaggedEmailsCache = message.emails || [];
        
        console.log('\n🔄 ========================================');
        console.log('🔄 RECEIVED UPDATE FROM BACKGROUND');
        console.log('========================================');
        console.log(`📧 Total emails monitored: ${message.totalEmails || 0}`);
        console.log(`🚨 Flagged emails: ${message.count}`);
        
        if (flaggedEmailsCache.length > 0) {
          const phishingCount = flaggedEmailsCache.filter(e => e.is_phishing === true).length;
          const safeCount = flaggedEmailsCache.filter(e => e.is_phishing === false).length;
          
          console.log('\n📊 Classification Breakdown:');
          console.log(`  🔴 Phishing: ${phishingCount}`);
          console.log(`  🟢 Safe: ${safeCount}`);
          console.log(`  ⚪ Other: ${flaggedEmailsCache.length - phishingCount - safeCount}`);
          
          console.log('\n🔄 Re-injecting circles with new data...');
          console.log('========================================\n');
          
          // Re-inject circles with updated data
          injectCirclesOnAllRows();
        } else {
          console.log('ℹ️ No emails flagged - all clear');
          console.log('========================================\n');
        }
        
        sendResponse({ success: true });
      }
      
      return false;
    });
  } catch (e) {
    console.error('❌ Failed to setup message listener:', e.message);
  }
}


// Inject visual warning badge - NO TEXT, JUST COLOR!
function injectWarningBadge(emailRow, emailData, rowIndex) {
  // Create circle container
  const circle = document.createElement("div");
  circle.className = "phishing-threat-circle";

  // Determine threat level and color - NO TEXT!
  let circleClass = "unknown"; // default white for unknown

  if (emailData) {
    // Classify based on is_phishing flag
    if (
      emailData.is_phishing === false ||
      emailData.threat_level === "SAFE" ||
      emailData.threat_level === "LOW"
    ) {
      circleClass = "safe";
      stats.safeEmails++;
      console.log(`  🟢 Row ${rowIndex} - GREEN (SAFE)`);
    } else if (
      emailData.is_phishing === true ||
      emailData.threat_level === "CRITICAL" ||
      emailData.threat_level === "HIGH"
    ) {
      circleClass = "danger";
      stats.phishingEmails++;
      console.log(`  🔴 Row ${rowIndex} - RED (PHISHING)`);
    } else if (emailData.threat_level === "MEDIUM") {
      circleClass = "warning";
      stats.phishingEmails++;
      console.log(`  🟡 Row ${rowIndex} - YELLOW (SUSPICIOUS)`);
    }
  } else {
    // NO DATA - show white circle
    console.log(`  ⚪ Row ${rowIndex} - WHITE (NO DATA)`);
  }

  circle.classList.add(circleClass);

  // NO TOOLTIP - JUST COLOR!
  // Add circle to the row
  emailRow.appendChild(circle);
}

// Also run when scrolling (for lazy-loaded emails)
let scrollTimeout;
window.addEventListener("scroll", () => {
  clearTimeout(scrollTimeout);
  scrollTimeout = setTimeout(() => {
    console.log("📜 Scroll detected, re-scanning...");
    injectCirclesOnAllRows();
  }, 1000);
});

console.log("🚀 Extension loaded and waiting...");

// Make function available globally for debugging
window.injectCirclesOnAllRows = injectCirclesOnAllRows;
