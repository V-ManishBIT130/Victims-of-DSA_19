// Background Service Worker - Fetches email data every 10 seconds
console.log('🚀 Phishing Detector Background Script Started');

const API_URL = 'http://localhost:3000/api/emails';
const REFRESH_INTERVAL = 10000; // 10 seconds
let fetchCount = 0;
let isServiceWorkerActive = true;

// Check if service worker is still active
function checkServiceWorkerHealth() {
  try {
    if (chrome.runtime && chrome.runtime.id) {
      return true;
    }
  } catch (e) {
    isServiceWorkerActive = false;
    console.log('⚠️ Service worker context lost');
  }
  return false;
}

// Fetch flagged emails from server
async function fetchFlaggedEmails() {
  if (!checkServiceWorkerHealth()) {
    console.log('⏹️ Service worker inactive, stopping fetch');
    return false;
  }

  try {
    fetchCount++;
    console.log(`📡 Fetching flagged emails from server... (attempt ${fetchCount})`);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
    
    const response = await fetch(API_URL, { 
      signal: controller.signal,
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (data.success && data.emails) {
      await chrome.storage.local.set({
        flaggedEmails: data.emails,
        lastUpdate: data.timestamp,
        totalCount: data.count,
        totalEmails: data.total_emails,
        serverOnline: true
      });
      
      // Count phishing vs safe
      const phishingCount = data.emails.filter(e => e.is_phishing === true).length;
      const safeCount = data.emails.filter(e => e.is_phishing === false).length;
      
      console.log(`✅ Updated ${data.count} flagged emails (${data.total_emails} total) at ${new Date(data.timestamp).toLocaleTimeString()}`);
      console.log(`   📊 Breakdown: 🔴 ${phishingCount} Phishing | 🟢 ${safeCount} Safe | ⚪ ${data.count - phishingCount - safeCount} Other`);

      
      // Send message to all Gmail tabs to refresh warnings
      try {
        const tabs = await chrome.tabs.query({url: 'https://mail.google.com/*'});
        
        for (const tab of tabs) {
          try {
            await chrome.tabs.sendMessage(tab.id, {
              action: 'updateWarnings',
              emails: data.emails,
              count: data.count,
              totalEmails: data.total_emails
            });
            console.log(`📧 Sent update to tab ${tab.id}`);
          } catch (error) {
            // Tab might not be ready or doesn't have content script, ignore
            if (error.message.includes('Receiving end does not exist')) {
              // Normal - content script not injected yet
            } else {
              console.log(`⏭️ Skipping tab ${tab.id}: ${error.message}`);
            }
          }
        }
      } catch (tabError) {
        console.log('⚠️ Could not query tabs:', tabError.message);
      }
      
      return true;
    } else {
      console.warn('⚠️ Server returned no data');
      await chrome.storage.local.set({ serverOnline: false });
      return false;
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('❌ Request timeout - server not responding');
    } else {
      console.error('❌ Failed to fetch emails:', error.message);
    }
    
    // Mark server as offline
    await chrome.storage.local.set({ serverOnline: false });
    
    // Try to use cached data if server is down
    try {
      const result = await chrome.storage.local.get(['flaggedEmails', 'lastUpdate']);
      if (result.flaggedEmails && result.flaggedEmails.length > 0) {
        console.log(`⚠️ Using cached data: ${result.flaggedEmails.length} emails (last updated: ${result.lastUpdate})`);
      } else {
        console.log('⚠️ No cached data available - waiting for server...');
      }
    } catch (storageError) {
      console.error('❌ Could not access storage:', storageError.message);
    }
    
    return false;
  }
}

// Initial fetch on extension load
console.log('🔄 Starting initial fetch...');
fetchFlaggedEmails();

// Set up periodic refresh every 10 seconds
const refreshInterval = setInterval(() => {
  if (!checkServiceWorkerHealth()) {
    clearInterval(refreshInterval);
    console.log('⏹️ Stopping refresh interval - service worker inactive');
    return;
  }
  fetchFlaggedEmails();
}, REFRESH_INTERVAL);

// Create alarm as backup (Chrome suspends service workers)
chrome.alarms.create('fetchEmails', { periodInMinutes: 0.17 }); // ~10 seconds

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'fetchEmails' && checkServiceWorkerHealth()) {
    fetchFlaggedEmails();
  }
});

// Listen for messages from content script and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!checkServiceWorkerHealth()) {
    sendResponse({ success: false, error: 'Service worker inactive' });
    return false;
  }

  if (message.action === 'getLatestData') {
    chrome.storage.local.get(['flaggedEmails', 'lastUpdate', 'totalEmails', 'serverOnline'], (result) => {
      sendResponse({
        emails: result.flaggedEmails || [],
        lastUpdate: result.lastUpdate,
        totalEmails: result.totalEmails || 0,
        serverOnline: result.serverOnline || false
      });
    });
    return true; // Keep message channel open for async response
  }
  
  if (message.action === 'forceRefresh') {
    console.log('🔄 Force refresh requested from popup');
    fetchFlaggedEmails().then(() => {
      sendResponse({ success: true, message: 'Refresh completed' });
    }).catch((error) => {
      sendResponse({ success: false, error: error.message });
    });
    return true; // Keep channel open for async response
  }
  
  return false;
});

console.log('✅ Background script initialized with 10-second polling');
