"""
Simple test case for phishing detection model
Tests a single phishing email example from the README
"""

import json
import sys
from pathlib import Path

# Test email - Phishing example from README
test_email = {
    "email_id": "TEST001_PAYPAL_PHISHING",
    "sender": "support@paypal-verify.tk",
    "sender_full": "PayPal Support <support@paypal-verify.tk>",
    "subject": "URGENT: Your PayPal Account Has Been Suspended",
    "body_full": """Dear PayPal User,

Your account has been suspended due to unusual activity. You must verify your identity immediately to avoid permanent closure.

Click here to verify now: http://paypal-verify.tk/secure/login.php

This link will expire in 24 hours. If you do not verify, your account will be permanently closed and all funds will be forfeited.

Act now to restore your account!

PayPal Security Team
""",
    "urls_found": ["http://paypal-verify.tk/secure/login.php"],
    "url_count": 1,
    "has_urls": True,
    "date_received": "2025-11-07 10:30:00"
}

print("="*80)
print("🛡️  PHISHING DETECTION MODEL - SIMPLE TEST")
print("="*80)
print("\n📧 Test Email:")
print(f"   From: {test_email['sender']}")
print(f"   Subject: {test_email['subject']}")
print(f"   URLs Found: {test_email['url_count']}")
print(f"   URL: {test_email['urls_found'][0] if test_email['urls_found'] else 'None'}")

print("\n" + "="*80)
print("🔄 Loading Model...")
print("="*80)

# Add Model_submission to path
model_path = Path(__file__).parent / "Model_submission"
sys.path.insert(0, str(model_path))

try:
    from phishing_detector import PhishingDetector
    
    # Initialize detector
    detector = PhishingDetector()
    
    print("\n✅ Model loaded successfully!")
    
    print("\n" + "="*80)
    print("📊 Analyzing Email...")
    print("="*80)
    
    # Analyze the email
    result = detector.analyze_email(test_email)
    
    # Display results
    print("\n" + "="*80)
    print("📋 ANALYSIS RESULTS")
    print("="*80)
    
    verdict_emoji = "🚨" if result['is_phishing'] else "✅"
    print(f"\n{verdict_emoji} VERDICT: {result['verdict']}")
    print(f"📊 Confidence: {result['confidence_percent']}")
    print(f"🔗 URL Risk Score: {result['url_risk_score']}/100")
    print(f"⚠️  Risk Level: {result['risk_level'].upper()}")
    print(f"🤖 Model Consensus: {result['model_votes']['phishing']}/{result['model_votes']['total']} models ({result['model_votes']['agreement']})")
    
    if result['risk_factors']:
        print(f"\n⚠️  Detected Risk Factors:")
        for i, factor in enumerate(result['risk_factors'], 1):
            print(f"   {i}. {factor}")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    # Expected result check
    print("\n📝 Validation:")
    if result['is_phishing']:
        print("   ✅ PASS: Email correctly identified as PHISHING")
        print("   ✅ Model is working properly!")
    else:
        print("   ❌ FAIL: Email should be identified as phishing")
        print("   ⚠️  Model may need attention")
    
    # Save result to file
    output_file = "test_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Results saved to: {output_file}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"\nError Type: {type(e).__name__}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
