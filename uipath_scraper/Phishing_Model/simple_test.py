"""
Simple Test Script for Phishing Detection Model
Tests with a single phishing email example
"""

import json
from phishing_detector import PhishingDetector

# Simple phishing email test case
test_email = {
    "email_id": "TEST_001",
    "sender": "security@paypal-verify.tk",
    "sender_full": "PayPal Security <security@paypal-verify.tk>",
    "sender_domain": "paypal-verify.tk",
    "subject": "URGENT: Your Account Will Be Suspended",
    "body_preview": "Dear valued customer, immediate action required...",
    "body_full": """Dear valued customer,

Your PayPal account has been flagged for suspicious activity. 

To prevent permanent suspension, you must verify your identity immediately by clicking the link below:

http://paypal-verify.tk/secure/verify.php?id=12345

You have only 24 hours to complete this verification, or your account and all funds will be permanently lost.

Do not delay! Click now to verify.

PayPal Security Team
""",
    "date_received": "2025-11-07 10:30:00",
    "urls_found": ["http://paypal-verify.tk/secure/verify.php?id=12345"],
    "url_count": 1,
    "extracted_at": "2025-11-07 10:30:05",
    "has_urls": True
}

print("="*80)
print("🛡️  PHISHING DETECTION MODEL - SIMPLE TEST")
print("="*80)

print("\n📧 Test Email Details:")
print(f"   Email ID: {test_email['email_id']}")
print(f"   From: {test_email['sender']}")
print(f"   Subject: {test_email['subject']}")
print(f"   URL Count: {test_email['url_count']}")
if test_email['urls_found']:
    print(f"   URL: {test_email['urls_found'][0]}")

print("\n" + "="*80)
print("🔄 Initializing Detection Model...")
print("="*80)

try:
    # Initialize the detector
    detector = PhishingDetector()
    print("✅ Model loaded successfully!")
    
    print("\n" + "="*80)
    print("📊 Analyzing Email...")
    print("="*80)
    
    # Analyze single email
    result = detector.predict_single(test_email)
    
    print("\n" + "="*80)
    print("📋 ANALYSIS RESULTS")
    print("="*80)
    
    # Display results
    verdict_emoji = "🚨" if result['is_phishing'] else "✅"
    print(f"\n{verdict_emoji} VERDICT: {'PHISHING' if result['is_phishing'] else 'LEGITIMATE'}")
    print(f"📊 Confidence: {result['phishing_probability']:.1%}")
    print(f"🎯 Model Prediction Score: {result['phishing_score']:.4f}")
    
    if 'url_risk_score' in result:
        print(f"🔗 URL Risk Score: {result['url_risk_score']}/100")
    
    if 'risk_factors' in result and result['risk_factors']:
        print(f"\n⚠️  Risk Factors Detected:")
        for i, factor in enumerate(result['risk_factors'], 1):
            print(f"   {i}. {factor}")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETED!")
    print("="*80)
    
    # Validation
    print("\n📝 Test Validation:")
    if result['is_phishing']:
        print("   ✅ PASS - Email correctly identified as PHISHING")
        print("   ✅ Model is working properly!")
        print(f"   ✅ Confidence level: {result['phishing_probability']:.1%}")
    else:
        print("   ❌ FAIL - Email should be flagged as phishing")
        print("   ⚠️  Model may need review")
    
    # Save result
    output_file = "simple_test_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Full results saved to: {output_file}")
    
    print("\n" + "="*80)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
