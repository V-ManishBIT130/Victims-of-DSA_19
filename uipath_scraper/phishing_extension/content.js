// Gmail Phishing Detector Extension - INSPIRATION MODE
console.log("�️ Gmail Phishing Detector Extension Started!");

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
    // Skip if already has circle
    if (row.querySelector(".phishing-threat-circle")) {
      console.log(`⏭️ Skipping row ${index} - already has circle`);
      return;
    }

    // Make row position relative for absolute positioning
    row.style.position = "relative";

    // Try to get email ID from Gmail attributes (multiple attempts)
    let emailId = 
      row.getAttribute("data-legacy-message-id") ||
      row.getAttribute("data-message-id") ||
      row.getAttribute("data-legacy-last-message-id") ||
      row.getAttribute("data-thread-id") ||
      row.getAttribute("id");

    // Try to find in cache by email_id
    let emailData = null;
    if (emailId && flaggedEmailsCache.length > 0) {
      // Try exact match first
      emailData = flaggedEmailsCache.find((e) => e.email_id === emailId);
      
      // If not found, try partial match (last 16 chars)
      if (!emailData && emailId.length >= 16) {
        const shortId = emailId.slice(-16);
        emailData = flaggedEmailsCache.find((e) => e.email_id === shortId || e.email_id.includes(shortId));
      }
      
      // Debug log
      if (emailId && !emailData) {
        console.log(`⚠️ Row ${index}: emailId="${emailId}" not found in cache`);
      }
    }

    // Create the circle
    injectWarningBadge(row, emailData, index, emailId);

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
        
        console.log('\n� ========================================');
        console.log('📦 LOADED DATA FROM STORAGE');
        console.log('========================================');
        console.log(`📊 Total emails in cache: ${flaggedEmailsCache.length}`);
        console.log(`📧 Total emails monitored: ${result.totalEmails || 0}`);
        console.log(`🌐 Server online: ${result.serverOnline ? '✅ YES' : '❌ NO'}`);
        
        if (flaggedEmailsCache.length > 0) {
          console.log('\n📋 Sample email structure:');
          console.log(JSON.stringify(flaggedEmailsCache[0], null, 2));
          
          // Count phishing vs safe
          const phishingCount = flaggedEmailsCache.filter(e => e.is_phishing === true).length;
          const safeCount = flaggedEmailsCache.filter(e => e.is_phishing === false).length;
          
          console.log('\n📊 Email Classification Breakdown:');
          console.log(`  🔴 Phishing: ${phishingCount}`);
          console.log(`  � Safe: ${safeCount}`);
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
          
          console.log('\n� Classification Breakdown:');
          console.log(`  🔴 Phishing: ${phishingCount}`);
          console.log(`  🟢 Safe: ${safeCount}`);
          console.log(`  ⚪ Other: ${flaggedEmailsCache.length - phishingCount - safeCount}`);
          
          console.log('\n� Re-injecting circles with new data...');
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


// Inject visual warning badge - SIMPLIFIED LIKE INSPIRATION
function injectWarningBadge(emailRow, emailData, rowIndex, emailId) {
  // Skip if already has circle
  if (emailRow.querySelector(".phishing-threat-circle")) {
    return;
  }

  // Create circle container (EXACTLY LIKE INSPIRATION)
  const circle = document.createElement("div");
  circle.className = "phishing-threat-circle";

  // Determine threat level and color - NO TEXT, JUST COLOR
  let circleClass = "unknown"; // default white for unknown
  let tooltipText = "";

  if (emailData) {
    const confidencePercent =
      emailData.confidence_percentage ||
      (emailData.confidence ? emailData.confidence * 100 : 0);

    // Classify based on is_phishing flag
    if (
      emailData.is_phishing === false ||
      emailData.threat_level === "SAFE" ||
      emailData.threat_level === "LOW"
    ) {
      circleClass = "safe";
      tooltipText = `Safe (${confidencePercent.toFixed(1)}%)`;
      stats.safeEmails++;
      console.log(`✅ Row ${rowIndex} [${emailId}] - 🟢 GREEN (SAFE)`);
    } else if (
      emailData.is_phishing === true ||
      emailData.threat_level === "CRITICAL" ||
      emailData.threat_level === "HIGH"
    ) {
      circleClass = "danger";
      tooltipText = `Phishing (${confidencePercent.toFixed(1)}%)`;
      stats.phishingEmails++;
      console.log(`✅ Row ${rowIndex} [${emailId}] - 🔴 RED (PHISHING)`);
    } else if (emailData.threat_level === "MEDIUM") {
      circleClass = "warning";
      tooltipText = `Suspicious (${confidencePercent.toFixed(1)}%)`;
      stats.phishingEmails++;
      console.log(`✅ Row ${rowIndex} [${emailId}] - 🟡 YELLOW (SUSPICIOUS)`);
    }
  } else {
    // NO DATA - show white circle, no text
    console.log(`✅ Row ${rowIndex} [${emailId}] - ⚪ WHITE (NO DATA)`);
    tooltipText = "Not analyzed yet";
  }

  circle.classList.add(circleClass);

  // Add tooltip on hover (EXACTLY LIKE INSPIRATION) - only if there's data
  if (tooltipText) {
    const tooltip = document.createElement("div");
    tooltip.className = "hover-text";
    tooltip.textContent = tooltipText;
    circle.appendChild(tooltip);
  }

  // Add circle to the row (EXACTLY LIKE INSPIRATION)
  emailRow.appendChild(circle);
}

// Also run when scrolling (for lazy-loaded emails) - EXACTLY LIKE INSPIRATION
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

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Start the detector - NO NEED FOR waitForGmail, already running on line 33
console.log('🚀 Extension loaded and waiting...');

// MANUAL DEBUG COMMANDS (paste in console)
console.log('\n💡 === MANUAL DEBUG COMMANDS ===');
console.log('To manually inject circles, paste in console:');
console.log('  injectCirclesOnAllRows()');
console.log('\nTo check cache:');
console.log('  chrome.storage.local.get(["flaggedEmails"], r => console.log("Cache:", r))');
console.log('\nTo force refresh from background:');
console.log('  chrome.runtime.sendMessage({action: "forceRefresh"})');
console.log('================================\n');
  
  // Threat level styling
  const threatLevel = emailData.threat_level || 'HIGH';
  const threatColors = {
    'CRITICAL': '#dc3545',
    'HIGH': '#fd7e14',
    'MEDIUM': '#ffc107',
    'LOW': '#28a745'
  };
  
  // Format URLs
  const urlsList = (emailData.urls_found || []).map(url => `
    <li>
      <code>${escapeHtml(url)}</code>
      <span class="url-warning">⚠️ Do not click</span>
    </li>
  `).join('');
  
  // Format red flags
  const redFlagsList = (emailData.red_flags || []).map(flag => `
    <li class="red-flag-item ${flag.severity.toLowerCase()}">
      <strong>[${flag.severity}] ${flag.category}:</strong> ${flag.flag}
      <br><small>${flag.description}</small>
    </li>
  `).join('');
  
  // Format recommendations
  const recommendationsList = (emailData.recommendations || []).map(rec => `
    <li class="recommendation-item ${rec.priority.toLowerCase()}">
      <strong>[${rec.priority}] ${rec.action}</strong>
      <br><small>${rec.description}</small>
    </li>
  `).join('');
  
  const confidencePercent = emailData.confidence_percentage || (emailData.confidence * 100);
  
  modal.innerHTML = `
    <div class="phishing-modal-content">
      <div class="modal-header" style="border-left: 5px solid ${threatColors[threatLevel]}">
        <h2>🚨 PHISHING EMAIL DETECTED</h2>
        <button class="modal-close" id="closeModal">×</button>
      </div>
      <div class="modal-body">
        <div class="alert-danger">
          <strong>⛔ Threat Level: ${threatLevel} (${confidencePercent.toFixed(1)}% confidence)</strong>
          <br>
          <small>Risk Score: ${emailData.risk_score || 0}/100 | Red Flags: ${emailData.red_flag_count || 0}</small>
        </div>
        
        <div class="email-details">
          <h3>📧 Email Information:</h3>
          <p><strong>From:</strong> ${escapeHtml(emailData.sender || 'Unknown')}</p>
          <p><strong>Subject:</strong> ${escapeHtml(emailData.subject || '(No Subject)')}</p>
          <p><strong>Date:</strong> ${emailData.date_received || 'Unknown'}</p>
          ${emailData.analyzed_at ? `<p><strong>Analyzed:</strong> ${new Date(emailData.analyzed_at).toLocaleString()}</p>` : ''}
        </div>
        
        ${redFlagsList ? `
        <div class="red-flags-section">
          <h3>� Security Red Flags:</h3>
          <ul class="red-flags-list">
            ${redFlagsList}
          </ul>
        </div>
        ` : ''}
        
        ${urlsList ? `
        <div class="urls-section">
          <h3>� Suspicious URLs Found (${emailData.url_count || 0}):</h3>
          <ul class="urls-list">
            ${urlsList}
          </ul>
        </div>
        ` : ''}
        
        <div class="warning-message">
          <h3>⚡ IMMEDIATE ACTIONS REQUIRED:</h3>
          <ul class="recommendations-list">
            ${recommendationsList}
          </ul>
        </div>
        
        <div class="modal-actions">
          <button class="btn-danger" id="closeModalBtn">
            Close Warning
          </button>
          <button class="btn-secondary" id="learnMoreBtn">
            Learn About Phishing
          </button>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // Add event listeners
  document.getElementById('closeModal').addEventListener('click', () => modal.remove());
  document.getElementById('closeModalBtn').addEventListener('click', () => modal.remove());
  document.getElementById('learnMoreBtn').addEventListener('click', () => {
    window.open('https://support.google.com/mail/answer/8253', '_blank');
  });
  
  // Close on outside click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.remove();
    }
  });

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Start the detector - NO NEED FOR waitForGmail, already running on line 33
console.log('🚀 Extension loaded and waiting...');

// MANUAL DEBUG COMMANDS (paste in console)
console.log('\n💡 === MANUAL DEBUG COMMANDS ===');
console.log('To manually inject circles, paste in console:');
console.log('  injectCirclesOnAllRows()');
console.log('\nTo check cache:');
console.log('  chrome.storage.local.get(["flaggedEmails"], r => console.log("Cache:", r))');
console.log('\nTo force refresh from background:');
console.log('  chrome.runtime.sendMessage({action: "forceRefresh"})');
console.log('================================\n');

// Make function available globally for debugging
window.injectCirclesOnAllRows = injectCirclesOnAllRows;



