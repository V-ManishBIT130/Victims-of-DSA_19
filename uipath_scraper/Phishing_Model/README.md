# 🛡️ Phishing Email Detection Model - Production Ready

**Version:** 1.0  
**Model:** Bidirectional LSTM (PyTorch)  
**Accuracy:** 98.63%  
**Device:** GPU/CPU Auto-detection

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Input Format](#input-format)
4. [Usage](#usage)
5. [Output Format](#output-format)
6. [Python API](#python-api)
7. [Features](#features)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
python phishing_detector.py --input examples/sample_emails.json --output results.json --pretty
```

### 3. View Results
Open `results.json` to see detailed analysis of each email.

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster processing

### Step-by-Step Installation

**1. Extract this folder to your desired location**

**2. Open terminal/command prompt in this folder**

**3. Install required packages:**
```bash
pip install -r requirements.txt
```

**Installation will include:**
- PyTorch (Deep Learning)
- scikit-learn (Machine Learning)
- pandas & numpy (Data Processing)
- tldextract (URL Analysis)

---

## 📥 Input Format

Your emails must be in **JSON format** with the following structure:

```json
[
  {
    "email_id": "unique_identifier",
    "sender": "email@example.com",
    "sender_full": "\"Display Name\" <email@example.com>",
    "sender_domain": "example.com",
    "subject": "Email subject line",
    "body_preview": "First 200 characters of body...",
    "body_full": "Complete email body text",
    "date_received": "2025-11-07 12:00:00",
    "urls_found": ["https://example.com", "https://another.com"],
    "url_count": 2,
    "extracted_at": "2025-11-07 12:00:05",
    "has_urls": true
  }
]
```

### Required Fields:
- ✅ `email_id` - Unique identifier for tracking
- ✅ `sender` - Email address of sender
- ✅ `subject` - Email subject line
- ✅ `body_full` - Complete email body text

### Optional Fields (recommended for better analysis):
- `sender_full` - Full sender name and email
- `sender_domain` - Domain of sender
- `body_preview` - Preview text (for display)
- `date_received` - When email was received
- `urls_found` - Array of URLs in email
- `url_count` - Number of URLs
- `has_urls` - Boolean flag

---

## 💻 Usage

### Command Line

**Basic Usage:**
```bash
python phishing_detector.py --input your_emails.json --output results.json
```

**Pretty Print (Human Readable):**
```bash
python phishing_detector.py --input your_emails.json --output results.json --pretty
```

**Arguments:**
- `--input` (required): Path to input JSON file with emails
- `--output` (optional): Path to output JSON file (default: analysis_results.json)
- `--pretty` (optional): Format output JSON for readability

### Example:
```bash
# Analyze sample emails
python phishing_detector.py --input examples/sample_emails.json --output my_results.json --pretty
```

---

## 📤 Output Format

The model returns a detailed JSON with:

### Batch Summary
```json
{
  "batch_summary": {
    "total_emails": 10,
    "analyzed_successfully": 10,
    "failed": 0,
    "phishing_detected": 3,
    "legitimate": 7,
    "phishing_percentage": 30.0,
    "threat_distribution": {
      "CRITICAL": 1,
      "HIGH": 2,
      "MEDIUM": 0,
      "LOW": 0,
      "SAFE": 7
    }
  }
}
```

### Individual Email Analysis
```json
{
  "email_id": "example_001",
  "sender": "security@suspicious.com",
  "subject": "URGENT: Verify Account",
  
  "prediction": {
    "is_phishing": true,
    "confidence": 0.9987,
    "confidence_percentage": 99.87,
    "threat_level": "CRITICAL",
    "verdict": "PHISHING",
    "risk_score": 95
  },
  
  "url_analysis": {
    "total_urls": 1,
    "urls_found": [
      {
        "url": "http://192.168.1.1/verify",
        "risk_level": "CRITICAL",
        "risk_score": 60,
        "risk_factors": [
          "Contains IP address",
          "Contains phishing keywords"
        ]
      }
    ],
    "has_suspicious_urls": true
  },
  
  "content_analysis": {
    "text_features": {
      "subject_length": 27,
      "body_length": 145,
      "uppercase_ratio": 0.08,
      "has_phishing_keywords": true
    },
    "sender_features": {
      "sender_has_numbers": false,
      "domain_mismatch": true
    }
  },
  
  "security_indicators": {
    "red_flags": [
      {
        "category": "URL",
        "severity": "CRITICAL",
        "flag": "IP address in URL",
        "description": "URLs with IP addresses are highly suspicious"
      },
      {
        "category": "CONTENT",
        "severity": "HIGH",
        "flag": "Phishing keywords detected",
        "description": "Contains common phishing terminology"
      }
    ],
    "red_flag_count": 2
  },
  
  "recommendations": [
    {
      "priority": "CRITICAL",
      "action": "DELETE IMMEDIATELY",
      "description": "This email contains dangerous elements"
    },
    {
      "priority": "HIGH",
      "action": "Report as phishing/spam",
      "description": "Help improve email security"
    }
  ]
}
```

---

## 🐍 Python API

### Import and Initialize
```python
from phishing_detector import PhishingDetector

# Initialize detector
detector = PhishingDetector(model_dir='models')
```

### Analyze Single Email
```python
email_data = {
    "email_id": "test_001",
    "sender": "user@example.com",
    "subject": "Test Email",
    "body_full": "This is a test email body"
}

# Get detailed analysis
result = detector.analyze_email(email_data)

# Check if phishing
if result['prediction']['is_phishing']:
    print(f"⚠️  PHISHING DETECTED!")
    print(f"Confidence: {result['prediction']['confidence_percentage']}%")
    print(f"Threat Level: {result['prediction']['threat_level']}")
else:
    print("✓ Email appears legitimate")
```

### Analyze Multiple Emails
```python
import json

# Load emails from file
with open('emails.json', 'r') as f:
    emails = json.load(f)

# Analyze batch
results = detector.analyze_batch(emails)

# Get statistics
print(f"Total: {results['batch_summary']['total_emails']}")
print(f"Phishing: {results['batch_summary']['phishing_detected']}")
print(f"Rate: {results['batch_summary']['phishing_percentage']}%")
```

### Quick Prediction (Simple)
```python
# Just get verdict and confidence
is_phishing, confidence = detector.predict(email_data)

if is_phishing:
    print(f"PHISHING (Confidence: {confidence*100:.2f}%)")
else:
    print(f"LEGITIMATE (Confidence: {(1-confidence)*100:.2f}%)")
```

---

## ⚡ Features

### 1. Comprehensive URL Analysis
- ✓ Individual risk assessment for each URL
- ✓ Detects IP addresses in URLs
- ✓ Identifies suspicious TLDs (.tk, .ml, .online, etc.)
- ✓ Flags dangerous file extensions (.sh, .exe, .bat)
- ✓ Checks for phishing keywords
- ✓ URL shortener detection

### 2. Content Analysis
- ✓ 50,022 machine learning features
- ✓ Text pattern analysis
- ✓ Phishing keyword detection
- ✓ Urgency indicator detection
- ✓ Money symbol detection
- ✓ Uppercase/lowercase ratio

### 3. Sender Verification
- ✓ Domain mismatch detection
- ✓ Sender authenticity check
- ✓ Numbers in email address flagging

### 4. Security Indicators
- ✓ Red flags with severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- ✓ Suspicious pattern detection
- ✓ Malware link detection
- ✓ Threat level assessment

### 5. Actionable Recommendations
- ✓ Priority-based actions
- ✓ Step-by-step security advice
- ✓ Context-specific recommendations

---

## 🎯 Threat Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| **CRITICAL** | Extreme danger (malware, IP URLs) | Delete immediately, do not click |
| **HIGH** | High confidence phishing | Delete, report as spam |
| **MEDIUM** | Possible phishing attempt | Exercise caution, verify sender |
| **LOW** | Low risk indicators | Be cautious with links |
| **SAFE** | Appears legitimate | Normal handling, stay vigilant |

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Issue: "CUDA out of memory"
**Solution:** Model will automatically fallback to CPU. If needed, reduce batch size.

### Issue: "FileNotFoundError: models/lstm_model.pth"
**Solution:** Ensure you're running from the Phishing_Model folder:
```bash
cd Phishing_Model
python phishing_detector.py --input your_file.json
```

### Issue: JSON parsing error
**Solution:** Validate your JSON format:
- Check all quotes are properly closed
- Ensure arrays are enclosed in [ ]
- Use online JSON validator

### Issue: Slow processing
**Solutions:**
- Install CUDA/GPU drivers for faster processing
- Process in smaller batches
- Use SSD for faster file I/O

---

## 📊 Model Performance

- **Accuracy:** 98.63%
- **Precision:** 98.81%
- **Recall:** 98.55%
- **F1 Score:** 98.68%
- **Processing Speed:** 0.07ms per email (GPU)
- **Training Data:** 81,868 emails (7 datasets combined)

### Tested Against:
✅ Obvious phishing (100% detection)  
✅ Advanced phishing (99.9% detection)  
✅ CEO fraud attempts  
✅ Prize scams  
✅ Credential phishing  
✅ Malware links  
✅ Legitimate emails (low false positives)

---

## 🗂️ Folder Structure

```
Phishing_Model/
├── phishing_detector.py       # Main detection pipeline
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── models/                     # Model files (DO NOT MODIFY)
│   ├── lstm_model.pth         # PyTorch LSTM model (26MB)
│   ├── tokenizer.pkl          # Text tokenizer (13.5MB)
│   ├── tfidf_vectorizer.pkl   # TF-IDF features (1.77MB)
│   └── feature_transformer.pkl # Feature scaler (2.7KB)
└── examples/
    └── sample_emails.json     # Example input format
```

---

## 📝 License & Usage

- ✅ Free to use for personal and commercial projects
- ✅ Modify and integrate into your applications
- ✅ Use as part of email security systems
- ⚠️ Do not redistribute model files without permission
- ⚠️ Model provided "as-is" without warranty

---

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your input JSON format matches the specification
3. Ensure all model files are present in the `models/` folder
4. Check that dependencies are correctly installed

---

## 🎉 Quick Test

Run this to test the model is working:

```bash
python phishing_detector.py --input examples/sample_emails.json --output test_results.json --pretty
```

If successful, you'll see:
```
✓ Loaded 2 email(s)
✓ Model loaded successfully
Analyzing 2 email(s)...
✓ Results saved to: test_results.json
```

---

**Ready to protect against phishing attacks! 🛡️**
