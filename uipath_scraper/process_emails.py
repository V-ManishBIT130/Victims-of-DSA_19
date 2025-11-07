"""
Automatic Phishing Detection Processor
Processes emails_data.json and saves results to phishing_results.json
Only processes emails with isPredicted=0 flag
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Paths
SCRIPT_DIR = Path(__file__).parent
EMAILS_FILE = SCRIPT_DIR / "emails_data.json"
TEMP_FILE = SCRIPT_DIR / "temp_emails.json"
RESULTS_FILE = SCRIPT_DIR / "phishing_results.json"
PHISHING_MODEL_DIR = SCRIPT_DIR / "Phishing_Model"
PHISHING_DETECTOR = PHISHING_MODEL_DIR / "phishing_detector.py"

def initialize_flags_in_emails():
    """Add isPredicted flag to all emails if not present"""
    try:
        with open(EMAILS_FILE, 'r', encoding='utf-8-sig') as f:
            emails = json.load(f)
        
        modified = False
        for email in emails:
            if 'isPredicted' not in email:
                email['isPredicted'] = 0
                modified = True
        
        if modified:
            # Save back with flags
            with open(EMAILS_FILE, 'w', encoding='utf-8') as f:
                json.dump(emails, f, indent=2, ensure_ascii=False)
            print(f"Initialized isPredicted flags for {len(emails)} emails")
        
        return True
    except Exception as e:
        print(f"Error initializing flags: {e}")
        return False

def load_and_filter_emails():
    """Load emails and filter only those with isPredicted=0"""
    print(f"Loading emails from: {EMAILS_FILE.name}")
    
    if not EMAILS_FILE.exists():
        print(f"Error: {EMAILS_FILE} not found!")
        return None, None
    
    try:
        # Load with BOM handling
        with open(EMAILS_FILE, 'r', encoding='utf-8-sig') as f:
            all_emails = json.load(f)
        
        print(f"Loaded {len(all_emails)} total emails")
        
        # Filter emails with isPredicted=0 (not yet processed)
        unprocessed_emails = [
            email for email in all_emails 
            if email.get('isPredicted', 0) == 0
        ]
        
        if not unprocessed_emails:
            print("No new emails to process (all emails already analyzed)")
            return all_emails, []
        
        print(f"Found {len(unprocessed_emails)} new emails to analyze")
        print(f"Skipping {len(all_emails) - len(unprocessed_emails)} already processed emails")
        
        # Save unprocessed emails to temp file for model
        with open(TEMP_FILE, 'w', encoding='utf-8') as f:
            json.dump(unprocessed_emails, f, indent=2, ensure_ascii=False)
        
        return all_emails, unprocessed_emails
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def update_flags_in_source(all_emails, processed_email_ids):
    """Update isPredicted flag to 1 for processed emails in emails_data.json"""
    try:
        for email in all_emails:
            if email['email_id'] in processed_email_ids:
                email['isPredicted'] = 1
        
        # Save updated emails back to source file
        with open(EMAILS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_emails, f, indent=2, ensure_ascii=False)
        
        print(f"Updated isPredicted flag for {len(processed_email_ids)} emails in source file")
        return True
    except Exception as e:
        print(f"Error updating flags: {e}")
        return False

def merge_results_with_existing():
    """Add isPredicted flag to results in phishing_results.json"""
    try:
        # Read the fresh results from the model
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Add isPredicted flag to each result
        if 'results' in results:
            for result in results['results']:
                result['isPredicted'] = 1
        
        # Save the updated results
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Added isPredicted flag to {len(results.get('results', []))} results")
        return results
    except Exception as e:
        print(f"Error updating results: {e}")
        return None

def run_detection():
    """Run phishing detection model"""
    print(f"\nRunning phishing detection model...")
    
    cmd = [
        sys.executable,
        str(PHISHING_DETECTOR),
        "--input", str(TEMP_FILE),
        "--output", str(RESULTS_FILE),
        "--pretty"
    ]
    
    try:
        # Set environment to handle Unicode
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            cmd,
            cwd=str(PHISHING_MODEL_DIR),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )
        
        # Print model output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"Model analysis complete")
            return True
        else:
            print(f"Error running model:")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        # Clean up temp file
        if TEMP_FILE.exists():
            TEMP_FILE.unlink()

def main():
    print("="*80)
    print("PHISHING DETECTION - AUTOMATIC PROCESSOR (Smart Mode)")
    print("="*80)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize flags in emails_data.json if needed
    initialize_flags_in_emails()
    
    # Load and filter emails
    all_emails, unprocessed_emails = load_and_filter_emails()
    if all_emails is None:
        return False
    
    if not unprocessed_emails:
        print("\n" + "="*80)
        print("NO NEW EMAILS TO PROCESS")
        print("="*80)
        print(f"\nAll {len(all_emails)} emails have already been analyzed")
        print(f"Results: {RESULTS_FILE}\n")
        return True
    
    # Run detection on unprocessed emails only
    success = run_detection()
    
    if success:
        # Update results with flags
        print(f"\nUpdating results with flags...")
        results = merge_results_with_existing()
        
        if results:
            # Update flags in source file
            processed_ids = [e['email_id'] for e in unprocessed_emails]
            update_flags_in_source(all_emails, processed_ids)
            
            print("\n" + "="*80)
            print("PROCESSING COMPLETE!")
            print("="*80)
            print(f"\nNew emails analyzed: {len(unprocessed_emails)}")
            total_results = len(results.get('results', []))
            print(f"Total results saved: {total_results}")
            print(f"Results: {RESULTS_FILE}\n")
        else:
            print("\nError updating results!")
            return False
    else:
        print("\nProcessing failed!")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
