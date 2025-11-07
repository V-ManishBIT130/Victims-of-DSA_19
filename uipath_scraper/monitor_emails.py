"""
Automatic Email Monitoring and Phishing Detection
Watches emails_data.json for changes and automatically runs detection
"""

import time
import hashlib
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
EMAILS_FILE = SCRIPT_DIR / "emails_data.json"
PROCESSOR_SCRIPT = SCRIPT_DIR / "process_emails.py"
RESULTS_FILE = SCRIPT_DIR / "phishing_results.json"
HASH_FILE = SCRIPT_DIR / ".last_emails_hash.txt"

def calculate_file_hash(filepath):
    """Calculate MD5 hash to detect file changes"""
    if not filepath.exists():
        return None
    
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_saved_hash():
    """Get the last processed file hash"""
    if HASH_FILE.exists():
        return HASH_FILE.read_text().strip()
    return None

def save_hash(file_hash):
    """Save the current file hash"""
    HASH_FILE.write_text(file_hash)

def run_processor():
    """Run the email processor"""
    try:
        result = subprocess.run(
            [sys.executable, str(PROCESSOR_SCRIPT)],
            cwd=str(SCRIPT_DIR),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            return True
        else:
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running processor: {e}")
        return False

def monitor_emails(check_interval=5):
    """Monitor emails_data.json and process when it changes"""
    print("="*80)
    print("🛡️  PHISHING DETECTION - CONTINUOUS MONITOR")
    print("="*80)
    print(f"\n📁 Monitoring: {EMAILS_FILE.name}")
    print(f"💾 Output: {RESULTS_FILE.name}")
    print(f"🔄 Check interval: {check_interval} seconds")
    print(f"⏸️  Press Ctrl+C to stop\n")
    print("="*80)
    
    # Check if file exists
    if not EMAILS_FILE.exists():
        print(f"\n⚠️  Warning: {EMAILS_FILE} not found!")
        print(f"   Waiting for file to be created...\n")
    
    last_hash = get_saved_hash()
    first_run = True
    
    try:
        while True:
            if EMAILS_FILE.exists():
                current_hash = calculate_file_hash(EMAILS_FILE)
                
                # Check if file changed or first run
                if current_hash != last_hash:
                    if first_run:
                        print(f"\n🔔 Processing existing {EMAILS_FILE.name}...")
                        first_run = False
                    else:
                        print(f"\n\n🔔 CHANGE DETECTED in {EMAILS_FILE.name}!")
                        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    print("="*80)
                    
                    # Run detection
                    success = run_processor()
                    
                    if success:
                        # Save new hash
                        save_hash(current_hash)
                        last_hash = current_hash
                        print(f"\n✅ Processing complete. Resuming monitoring...")
                    else:
                        print(f"\n❌ Processing failed. Will retry on next change...")
                    
                    print("="*80)
                    print(f"⏳ Monitoring for changes...\n")
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped by user")
        print("="*80)
        print(f"Final results in: {RESULTS_FILE}")
        print("="*80)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Phishing Detection Monitor')
    parser.add_argument('--interval', type=int, default=5,
                        help='Check interval in seconds (default: 5)')
    
    args = parser.parse_args()
    
    monitor_emails(check_interval=args.interval)

if __name__ == "__main__":
    main()
