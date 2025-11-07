"""
Automated Phishing Detection Monitor
Watches emails_data.json for changes and runs phishing detection automatically
Saves results to phishing_results.json
"""

import os
import json
import time
import sys
from datetime import datetime
from pathlib import Path
import hashlib

# Change to Phishing_Model directory for model to find its files
SCRIPT_DIR = Path(__file__).parent
PHISHING_MODEL_DIR = SCRIPT_DIR / "Phishing_Model"
os.chdir(PHISHING_MODEL_DIR)

# Add Phishing_Model to path
sys.path.insert(0, str(PHISHING_MODEL_DIR))

from phishing_detector import PhishingDetector

# File paths (relative to parent directory)
EMAILS_DATA_FILE = SCRIPT_DIR / "emails_data.json"
RESULTS_FILE = SCRIPT_DIR / "phishing_results.json"
LAST_HASH_FILE = SCRIPT_DIR / ".last_emails_hash"

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file to detect changes"""
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if not filepath.exists():
        return None
    
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_last_processed_hash():
    """Get hash of last processed file"""
    if LAST_HASH_FILE.exists():
        with open(LAST_HASH_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_current_hash(file_hash):
    """Save current file hash"""
    with open(LAST_HASH_FILE, 'w') as f:
        f.write(file_hash)

def load_emails():
    """Load emails from emails_data.json"""
    if not EMAILS_DATA_FILE.exists():
        print(f"❌ Error: {EMAILS_DATA_FILE} not found!")
        return None
    
    try:
        # Try utf-8-sig first to handle BOM, then fall back to utf-8
        try:
            with open(EMAILS_DATA_FILE, 'r', encoding='utf-8-sig') as f:
                emails = json.load(f)
        except:
            with open(EMAILS_DATA_FILE, 'r', encoding='utf-8') as f:
                emails = json.load(f)
        
        print(f"✅ Loaded {len(emails)} emails from {EMAILS_DATA_FILE.name}")
        return emails
    except Exception as e:
        print(f"❌ Error loading emails: {e}")
        return None

def process_emails(detector, emails):
    """Process emails and return results"""
    print(f"\n🔄 Processing {len(emails)} emails...")
    
    results = []
    phishing_count = 0
    legitimate_count = 0
    
    for idx, email in enumerate(emails, 1):
        try:
            # Analyze email
            result = detector.predict_single(email)
            
            # Count verdicts
            if result['is_phishing']:
                phishing_count += 1
            else:
                legitimate_count += 1
            
            results.append(result)
            
            # Progress indicator
            if idx % 5 == 0 or idx == len(emails):
                print(f"   Processed: {idx}/{len(emails)} emails...")
                
        except Exception as e:
            print(f"   ⚠️  Error processing email {email.get('email_id', 'unknown')}: {e}")
            # Add error result
            results.append({
                'email_id': email.get('email_id', 'unknown'),
                'error': str(e),
                'is_phishing': False,
                'phishing_probability': 0.0
            })
    
    return results, phishing_count, legitimate_count

def save_results(results, phishing_count, legitimate_count):
    """Save results to phishing_results.json"""
    output = {
        'metadata': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_emails': len(results),
            'phishing_detected': phishing_count,
            'legitimate_detected': legitimate_count,
            'phishing_percentage': f"{(phishing_count / len(results) * 100):.1f}%" if results else "0.0%"
        },
        'emails': results
    }
    
    try:
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Results saved to {RESULTS_FILE}")
        return True
    except Exception as e:
        print(f"\n❌ Error saving results: {e}")
        return False

def run_detection():
    """Main detection function"""
    print("\n" + "="*80)
    print("🔍 RUNNING PHISHING DETECTION")
    print("="*80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load emails
    emails = load_emails()
    if not emails:
        return False
    
    # Initialize detector
    print("\n🤖 Initializing phishing detection model...")
    try:
        detector = PhishingDetector()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    # Process emails
    results, phishing_count, legitimate_count = process_emails(detector, emails)
    
    # Display summary
    print("\n" + "="*80)
    print("📊 ANALYSIS SUMMARY")
    print("="*80)
    print(f"   Total Emails: {len(results)}")
    print(f"   🚨 Phishing: {phishing_count}")
    print(f"   ✅ Legitimate: {legitimate_count}")
    print(f"   Phishing Rate: {(phishing_count / len(results) * 100):.1f}%")
    
    # Save results
    success = save_results(results, phishing_count, legitimate_count)
    
    if success:
        print("\n✅ Detection completed successfully!")
        print("="*80)
    
    return success

def monitor_file(check_interval=5):
    """Monitor emails_data.json for changes and run detection"""
    print("="*80)
    print("🛡️  PHISHING DETECTION MONITOR - STARTED")
    print("="*80)
    print(f"\n📁 Monitoring: {EMAILS_DATA_FILE.name}")
    print(f"💾 Output: {RESULTS_FILE.name}")
    print(f"🔄 Check interval: {check_interval} seconds")
    print("\n⏳ Waiting for changes... (Press Ctrl+C to stop)")
    print("="*80)
    
    # Initialize detector once
    print("\n🤖 Pre-loading model for faster processing...")
    try:
        detector = PhishingDetector()
        print("✅ Model loaded and ready!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    last_processed_hash = get_last_processed_hash()
    
    # Check if file exists and process immediately if it's new or changed
    if EMAILS_DATA_FILE.exists():
        current_hash = calculate_file_hash(EMAILS_DATA_FILE)
        if current_hash != last_processed_hash:
            print(f"\n🔔 Initial processing of {EMAILS_DATA_FILE.name}...")
            
            emails = load_emails()
            if emails:
                results, phishing_count, legitimate_count = process_emails(detector, emails)
                
                print("\n" + "="*80)
                print("📊 ANALYSIS SUMMARY")
                print("="*80)
                print(f"   Total Emails: {len(results)}")
                print(f"   🚨 Phishing: {phishing_count}")
                print(f"   ✅ Legitimate: {legitimate_count}")
                print(f"   Phishing Rate: {(phishing_count / len(results) * 100):.1f}%")
                
                save_results(results, phishing_count, legitimate_count)
                save_current_hash(current_hash)
                print("\n✅ Initial processing complete!")
                print("="*80)
    
    # Monitor for changes
    try:
        while True:
            if EMAILS_DATA_FILE.exists():
                current_hash = calculate_file_hash(EMAILS_DATA_FILE)
                
                if current_hash != last_processed_hash:
                    print(f"\n\n🔔 CHANGE DETECTED in {EMAILS_DATA_FILE.name}!")
                    print("="*80)
                    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Load and process emails
                    emails = load_emails()
                    if emails:
                        results, phishing_count, legitimate_count = process_emails(detector, emails)
                        
                        print("\n" + "="*80)
                        print("📊 ANALYSIS SUMMARY")
                        print("="*80)
                        print(f"   Total Emails: {len(results)}")
                        print(f"   🚨 Phishing: {phishing_count}")
                        print(f"   ✅ Legitimate: {legitimate_count}")
                        print(f"   Phishing Rate: {(phishing_count / len(results) * 100):.1f}%")
                        
                        save_results(results, phishing_count, legitimate_count)
                        save_current_hash(current_hash)
                        last_processed_hash = current_hash
                        
                        print("\n✅ Processing complete! Resuming monitoring...")
                        print("="*80)
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped by user")
        print("="*80)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Phishing Detection Monitor')
    parser.add_argument('--monitor', action='store_true', 
                        help='Run in continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=5,
                        help='Check interval in seconds (default: 5)')
    parser.add_argument('--once', action='store_true',
                        help='Run detection once and exit')
    
    args = parser.parse_args()
    
    if args.monitor:
        # Continuous monitoring mode
        monitor_file(check_interval=args.interval)
    elif args.once:
        # Run once and exit
        run_detection()
    else:
        # Default: run once
        run_detection()

if __name__ == "__main__":
    main()
