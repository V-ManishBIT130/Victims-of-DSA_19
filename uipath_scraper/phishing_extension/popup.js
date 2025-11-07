// Popup script for Phishing Detector Extension
console.log('🛡️ Popup opened');

const API_URL = 'http://localhost:3000/api/emails';

// DOM elements
const loadingState = document.getElementById('loadingState');
const mainContent = document.getElementById('mainContent');
const statusBadge = document.getElementById('statusBadge');
const statusText = document.getElementById('statusText');
const messageArea = document.getElementById('messageArea');
const flaggedCount = document.getElementById('flaggedCount');
const totalUrls = document.getElementById('totalUrls');
const lastUpdate = document.getElementById('lastUpdate');

const testApiBtn = document.getElementById('testApiBtn');
const refreshBtn = document.getElementById('refreshBtn');
const clearCacheBtn = document.getElementById('clearCacheBtn');
const openGmailBtn = document.getElementById('openGmailBtn');

// Load data on popup open
window.addEventListener('DOMContentLoaded', () => {
  loadStatus();
});

// Load status from storage
function loadStatus() {
  chrome.storage.local.get(['flaggedEmails', 'lastUpdate', 'totalCount'], (result) => {
    loadingState.style.display = 'none';
    mainContent.style.display = 'block';

    if (result.flaggedEmails && result.flaggedEmails.length > 0) {
      updateUI(result.flaggedEmails, result.lastUpdate, result.totalCount);
    } else {
      showMessage('No flagged emails yet. Monitoring active...', 'info');
      flaggedCount.textContent = '0';
      totalUrls.textContent = '0';
      lastUpdate.innerHTML = '<strong>Last Update:</strong> Waiting for data...';
    }
  });
}

// Update UI with data
function updateUI(emails, lastUpdateTime, count) {
  flaggedCount.textContent = count || emails.length;
  
  // Calculate total URLs
  const totalUrlCount = emails.reduce((sum, email) => sum + (email.url_count || 0), 0);
  totalUrls.textContent = totalUrlCount;

  // Format last update time
  if (lastUpdateTime) {
    const date = new Date(lastUpdateTime);
    const timeString = date.toLocaleTimeString();
    const dateString = date.toLocaleDateString();
    lastUpdate.innerHTML = `<strong>Last Update:</strong> ${timeString} on ${dateString}`;
  }

  // Set status
  statusBadge.classList.add('active');
  statusBadge.classList.remove('inactive');
  statusText.textContent = 'Active - Monitoring Gmail';
}

// Show message
function showMessage(message, type = 'success') {
  const messageDiv = document.createElement('div');
  messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
  messageDiv.textContent = message;
  messageArea.innerHTML = '';
  messageArea.appendChild(messageDiv);

  setTimeout(() => {
    messageDiv.remove();
  }, 5000);
}

// Test API connection
testApiBtn.addEventListener('click', async () => {
  testApiBtn.disabled = true;
  testApiBtn.textContent = '⏳ Testing...';

  try {
    const response = await fetch(API_URL);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    
    if (data.success) {
      showMessage(`✅ API Connected! Found ${data.count} flagged emails.`, 'success');
      
      // Update storage with fresh data
      chrome.storage.local.set({
        flaggedEmails: data.emails,
        lastUpdate: data.timestamp,
        totalCount: data.count
      }, () => {
        loadStatus();
      });
    } else {
      showMessage('⚠️ API responded but no data available.', 'error');
    }
  } catch (error) {
    showMessage(`❌ API Error: ${error.message}. Make sure server.js is running.`, 'error');
    statusBadge.classList.add('inactive');
    statusBadge.classList.remove('active');
    statusText.textContent = 'Inactive - API Unreachable';
  } finally {
    testApiBtn.disabled = false;
    testApiBtn.innerHTML = '<span>🔍</span> Test API Connection';
  }
});

// Force refresh data
refreshBtn.addEventListener('click', async () => {
  refreshBtn.disabled = true;
  refreshBtn.textContent = '⏳ Refreshing...';

  try {
    // Trigger background script to fetch
    chrome.runtime.sendMessage({ action: 'forceRefresh' }, (response) => {
      if (response && response.success) {
        showMessage('✅ Data refreshed successfully!', 'success');
        setTimeout(loadStatus, 500);
      } else {
        showMessage('⚠️ Refresh failed. Check API connection.', 'error');
      }
    });
  } catch (error) {
    showMessage(`❌ Error: ${error.message}`, 'error');
  } finally {
    setTimeout(() => {
      refreshBtn.disabled = false;
      refreshBtn.innerHTML = '<span>🔄</span> Force Refresh Data';
    }, 2000);
  }
});

// Clear cache
clearCacheBtn.addEventListener('click', () => {
  if (confirm('Are you sure you want to clear all cached data?')) {
    chrome.storage.local.clear(() => {
      showMessage('🗑️ Cache cleared successfully!', 'success');
      flaggedCount.textContent = '0';
      totalUrls.textContent = '0';
      lastUpdate.innerHTML = '<strong>Last Update:</strong> Cache cleared';
    });
  }
});

// Open Gmail
openGmailBtn.addEventListener('click', () => {
  chrome.tabs.create({ url: 'https://mail.google.com' });
  window.close();
});

// Listen for background script messages
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'dataUpdated') {
    loadStatus();
  }
});

// Auto-refresh popup every 10 seconds
setInterval(loadStatus, 10000);
