"""
Email Monitoring and Processing Script
Automatically monitors emails_data.json for changes and processes them every 10 seconds
"""

import os
import time
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
EMAILS_FILE = "emails_data.json"
RESULTS_FILE = "phishing_results.json"
CHECK_INTERVAL = 10  # seconds
PROCESS_SCRIPT = "process_emails.py"

class EmailMonitor:
    def __init__(self):
        self.last_modified = None
        self.last_email_count = 0
        self.process_count = 0
        
    def get_file_modified_time(self, filepath):
        """Get last modified time of a file"""
        try:
            if os.path.exists(filepath):
                return os.path.getmtime(filepath)
        except Exception as e:
            print(f"⚠️  Error getting file time: {e}")
        return None
    
    def get_email_count(self, filepath):
        """Get number of emails in the JSON file"""
        try:
            if os.path.exists(filepath):
                # Try utf-8-sig to handle BOM
                with open(filepath, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return len(data)
        except Exception as e:
            print(f"Warning: Error reading email count: {e}")
        return 0
    
    def should_process(self):
        """Check if emails_data.json has been updated"""
        current_modified = self.get_file_modified_time(EMAILS_FILE)
        current_count = self.get_email_count(EMAILS_FILE)
        
        if current_modified is None:
            return False, "File not found"
        
        # First run
        if self.last_modified is None:
            self.last_modified = current_modified
            self.last_email_count = current_count
            return True, f"Initial processing ({current_count} emails)"
        
        # Check if file was modified
        if current_modified > self.last_modified:
            self.last_modified = current_modified
            old_count = self.last_email_count
            self.last_email_count = current_count
            
            if current_count != old_count:
                return True, f"Updated: {old_count} → {current_count} emails"
            else:
                return True, f"Modified ({current_count} emails)"
        
        return False, f"No changes ({current_count} emails)"
    
    def run_processing(self):
        """Run the process_emails.py script"""
        try:
            print(f"\n{'='*80}")
            print(f"Processing emails... (Run #{self.process_count + 1})")
            print(f"{'='*80}")
            
            # Run the processing script
            result = subprocess.run(
                [sys.executable, PROCESS_SCRIPT],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                print(result.stdout)
                self.process_count += 1
                print(f"Processing completed successfully!")
                return True
            else:
                print(f"Processing failed with exit code {result.returncode}")
                print(f"Error output: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Processing timed out after 2 minutes")
            return False
        except Exception as e:
            print(f"❌ Error running processing script: {e}")
            return False
    
    def run(self):
        """Main monitoring loop"""
        print("="*80)
        print("EMAIL PHISHING DETECTION - AUTOMATED MONITOR")
        print("="*80)
        print(f"\nMonitoring file: {EMAILS_FILE}")
        print(f"Results file: {RESULTS_FILE}")
        print(f"Check interval: {CHECK_INTERVAL} seconds")
        print(f"Press Ctrl+C to stop monitoring")
        print("="*80)
        
        try:
            while True:
                should_run, reason = self.should_process()
                
                current_time = datetime.now().strftime("%H:%M:%S")
                
                if should_run:
                    print(f"\n[{current_time}] {reason}")
                    success = self.run_processing()
                    
                    if success:
                        # Show result summary
                        if os.path.exists(RESULTS_FILE):
                            try:
                                with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                                    results = json.load(f)
                                    if 'predictions' in results:
                                        phishing_count = sum(1 for p in results['predictions'] if p.get('is_phishing'))
                                        total = len(results['predictions'])
                                        print(f"\nSummary: {phishing_count}/{total} emails flagged as phishing")
                            except:
                                pass
                else:
                    print(f"[{current_time}] {reason}", end='\r')
                
                # Wait for next check
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\n\n{'='*80}")
            print(f"Monitoring stopped by user")
            print(f"Total processing runs: {self.process_count}")
            print(f"{'='*80}")
            sys.exit(0)

if __name__ == "__main__":
    # Check if required files exist
    if not os.path.exists(PROCESS_SCRIPT):
        print(f"❌ Error: {PROCESS_SCRIPT} not found!")
        print(f"   Make sure process_emails.py is in the same directory.")
        sys.exit(1)
    
    if not os.path.exists(EMAILS_FILE):
        print(f"⚠️  Warning: {EMAILS_FILE} not found yet")
        print(f"   Waiting for file to be created...")
    
    # Start monitoring
    monitor = EmailMonitor()
    monitor.run()
