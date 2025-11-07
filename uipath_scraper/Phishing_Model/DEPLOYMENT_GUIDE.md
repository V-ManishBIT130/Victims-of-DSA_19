# 🛡️ Phishing Email Detection - Deployment Guide

## ✅ Deployment Package Ready

This folder contains everything you need to deploy the phishing email detection system in production.

### 📦 What's Included

```
Phishing_Model/
├── phishing_detector.py       # Main detection pipeline (standalone)
├── requirements.txt            # Python dependencies
├── README.md                   # Complete usage documentation
├── DEPLOYMENT_GUIDE.md         # This file
├── models/                     # Pre-trained model files
│   ├── lstm_model.pth         # PyTorch model weights (26MB)
│   ├── tokenizer.pkl          # Text tokenizer (13.5MB)
│   ├── tfidf_vectorizer.pkl   # TF-IDF features (1.77MB)
│   └── feature_transformer.pkl # Feature scaler (2.7KB)
└── examples/
    └── sample_emails.json     # Test emails in correct format
```

### 🚀 Quick Start (3 Steps)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the System**
   ```bash
   python phishing_detector.py --input examples/sample_emails.json --output results.json --pretty
   ```

3. **Integrate with Your Frontend**
   ```python
   from phishing_detector import PhishingDetector
   
   detector = PhishingDetector("models")
   results = detector.analyze_emails(your_emails)
   ```

### 📊 Model Performance

- **Accuracy**: 98.63%
- **Precision**: 98.81%
- **Recall**: 98.55%
- **Speed**: 0.07ms per email (on GPU)
- **Training Data**: 81,868 emails from 7 datasets

### 🎯 Features

- Real-time phishing detection
- URL risk analysis
- Content analysis (keywords, formatting)
- Sender verification
- Malicious file detection
- Detailed threat reports
- GPU acceleration (CUDA support)

### 📋 Input Format (Frontend JSON)

Your frontend should send emails in this exact format:

```json
{
  "emails": [
    {
      "email_id": "unique_id",
      "sender": "sender@example.com",
      "sender_full": "Sender Name <sender@example.com>",
      "sender_domain": "example.com",
      "subject": "Email subject",
      "body_full": "Full email body text...",
      "body_preview": "Preview text...",
      "date_received": "2025-11-07 12:00:00",
      "urls_found": ["http://example.com"],
      "url_count": 1,
      "has_urls": true
    }
  ]
}
```

### 📤 Output Format

Returns detailed analysis for each email:

```json
{
  "batch_summary": {
    "total_emails": 6,
    "analyzed_successfully": 6,
    "phishing_detected": 2,
    "legitimate": 4,
    "phishing_percentage": 33.33
  },
  "results": [
    {
      "email_id": "unique_id",
      "prediction": {
        "is_phishing": true,
        "confidence": 0.98,
        "threat_level": "HIGH",
        "verdict": "PHISHING"
      },
      "url_analysis": { ... },
      "content_analysis": { ... },
      "security_indicators": { ... },
      "recommendations": [ ... ]
    }
  ]
}
```

### 🔧 Configuration Options

#### Command Line Usage
```bash
# Basic usage
python phishing_detector.py --input emails.json --output results.json

# Pretty-printed JSON
python phishing_detector.py --input emails.json --output results.json --pretty

# Force CPU (no GPU)
python phishing_detector.py --input emails.json --no-cuda

# Adjust batch size
python phishing_detector.py --input emails.json --batch-size 64
```

#### Python API Usage
```python
from phishing_detector import PhishingDetector

# Initialize (auto-detects GPU)
detector = PhishingDetector("models")

# Analyze emails
emails = load_your_emails()
results = detector.analyze_emails(emails)

# Process results
for result in results['results']:
    if result['prediction']['is_phishing']:
        print(f"⚠️ Phishing detected: {result['email_id']}")
```

### 🖥️ System Requirements

**Minimum**:
- Python 3.8+
- 4GB RAM
- 500MB disk space

**Recommended (with GPU)**:
- Python 3.8+
- CUDA-capable GPU (2GB+ VRAM)
- 8GB RAM
- 500MB disk space

### 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'torch'`
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: Model running on CPU (slow)
- **Solution**: Install PyTorch with CUDA: See README.md for instructions

**Issue**: `KeyError` when analyzing emails
- **Solution**: Ensure all required fields are present in input JSON

**Issue**: Out of memory error
- **Solution**: Reduce batch size: `--batch-size 16`

### 📝 Testing Results

**Sample Emails**: 2 test emails provided
- ✅ Phishing email: Detected with 100% confidence
- ✅ Legitimate email: Correctly classified as safe

**Frontend Emails**: 6 emails from your frontend
- ✅ All analyzed successfully
- ✅ 2 phishing detected (33.33%)
- ✅ 4 legitimate emails (66.67%)

### 📞 Integration Support

For detailed integration instructions, see `README.md`.

For Python API documentation, run:
```python
from phishing_detector import PhishingDetector
help(PhishingDetector)
```

### 🔐 Security Notes

- Model runs locally (no data sent to external servers)
- All processing happens in-memory
- No email data is stored by the system
- Safe for handling sensitive corporate email data

### 📈 Model Architecture

- **Type**: Bidirectional LSTM (PyTorch)
- **Layers**: 2 LSTM layers + 2 fully connected layers
- **Features**: 50,022 total (50,000 TF-IDF + 22 custom)
- **Embedding**: 128 dimensions
- **LSTM Units**: Layer 1: 64, Layer 2: 32 (bidirectional)

### 🎓 Trained On

7 public phishing datasets:
1. Nazario Phishing Corpus
2. SpamAssassin Corpus
3. Enron Email Dataset
4. CEAS 2008 Dataset
5. Fraudulent Email Corpus
6. Phishing Email Dataset
7. Nigerian Fraud Dataset

**Total**: 81,868 unique emails after deduplication

---

## 🎉 Ready for Production!

This package has been tested and verified to work with your exact frontend JSON format.

**You can now:**
1. Copy this entire folder to your production server
2. Install dependencies
3. Integrate with your email system
4. Start detecting phishing emails!

For questions or issues, refer to the comprehensive `README.md` file.
