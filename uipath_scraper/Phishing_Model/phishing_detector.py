"""
Phishing Email Detection - Production Pipeline
Accepts frontend JSON format and returns detailed analysis
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import re

# Try importing required packages
try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset
    import joblib
    import numpy as np
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    import tldextract
except ImportError as e:
    print(f"ERROR: Missing required package. Please run: pip install -r requirements.txt")
    sys.exit(1)


# ==================== MODEL DEFINITION ====================

class SimpleTokenizer:
    """Simple word tokenizer for LSTM"""
    def __init__(self, vocab_size=10000):
        self.vocab_size = vocab_size
        self.word2idx = {'<PAD>': 0, '<UNK>': 1}
        self.idx2word = {0: '<PAD>', 1: '<UNK>'}
        
    def fit_on_texts(self, texts):
        word_freq = {}
        for text in texts:
            for word in str(text).lower().split():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        for idx, (word, _) in enumerate(sorted_words[:self.vocab_size - 2], start=2):
            self.word2idx[word] = idx
            self.idx2word[idx] = word
    
    def texts_to_sequences(self, texts):
        sequences = []
        for text in texts:
            seq = [self.word2idx.get(word, 1) for word in str(text).lower().split()]
            sequences.append(seq)
        return sequences


class BiLSTMClassifier(nn.Module):
    """Bidirectional LSTM for phishing detection"""
    def __init__(self, vocab_size, embedding_dim, lstm_units, dropout_rate):
        super(BiLSTMClassifier, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm1 = nn.LSTM(embedding_dim, lstm_units, batch_first=True, bidirectional=True)
        self.dropout1 = nn.Dropout(dropout_rate)
        self.lstm2 = nn.LSTM(lstm_units * 2, lstm_units // 2, batch_first=True, bidirectional=True)
        self.dropout2 = nn.Dropout(dropout_rate)
        self.fc1 = nn.Linear(lstm_units, 32)
        self.relu = nn.ReLU()
        self.dropout3 = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        # Embedding
        embedded = self.embedding(x)
        
        # First LSTM layer
        lstm_out1, _ = self.lstm1(embedded)
        lstm_out1 = self.dropout1(lstm_out1)
        
        # Second LSTM layer
        lstm_out2, _ = self.lstm2(lstm_out1)
        lstm_out2 = self.dropout2(lstm_out2)
        
        # Take the last output
        last_output = lstm_out2[:, -1, :]
        
        # Fully connected layers
        fc_out = self.fc1(last_output)
        fc_out = self.relu(fc_out)
        fc_out = self.dropout3(fc_out)
        output = self.fc2(fc_out)
        output = self.sigmoid(output)
        
        return output


# ==================== FEATURE EXTRACTION ====================

class EmailFeatureExtractor:
    """Extract custom features from email data"""
    
    def __init__(self):
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        self.phishing_keywords = ['login', 'reset', 'verify', 'confirm', 'account', 'suspended', 
                                   'urgent', 'click', 'update', 'password', 'security', 'expire']
    
    def extract_url_features(self, text: str) -> dict:
        """Extract URL-based features"""
        urls = self.url_pattern.findall(str(text))
        
        features = {
            'num_urls': len(urls),
            'num_unique_domains': 0,
            'has_ip': 0,
            'avg_url_length': 0,
            'has_phishing_keywords_in_url': 0,
            'num_dots_in_url': 0,
            'num_digits_in_url': 0,
        }
        
        if urls:
            domains = set()
            total_length = 0
            total_dots = 0
            total_digits = 0
            
            for url in urls:
                extracted = tldextract.extract(url)
                domain = f"{extracted.domain}.{extracted.suffix}"
                domains.add(domain)
                total_length += len(url)
                
                if self.ip_pattern.search(url):
                    features['has_ip'] = 1
                
                total_dots += url.count('.')
                total_digits += sum(c.isdigit() for c in url)
                
                for keyword in self.phishing_keywords:
                    if keyword in url.lower():
                        features['has_phishing_keywords_in_url'] = 1
                        break
            
            features['num_unique_domains'] = len(domains)
            features['avg_url_length'] = total_length / len(urls)
            features['num_dots_in_url'] = total_dots / len(urls)
            features['num_digits_in_url'] = total_digits / len(urls)
        
        return features
    
    def extract_text_features(self, subject: str, body: str) -> dict:
        """Extract text-based features"""
        full_text = f"{subject} {body}"
        
        features = {
            'subject_len': len(str(subject)),
            'body_len': len(str(body)),
            'num_uppercase': sum(1 for c in full_text if c.isupper()),
            'num_digits': sum(1 for c in full_text if c.isdigit()),
            'num_special_chars': sum(1 for c in full_text if not c.isalnum() and not c.isspace()),
            'has_money_symbol': int(any(symbol in full_text for symbol in ['$', '€', '₹', '£', '¥'])),
            'num_exclamation': full_text.count('!'),
            'num_question': full_text.count('?'),
            'has_phishing_keywords': 0,
            'ratio_uppercase': 0,
            'ratio_digits': 0,
        }
        
        for keyword in self.phishing_keywords:
            if keyword in full_text.lower():
                features['has_phishing_keywords'] = 1
                break
        
        if len(full_text) > 0:
            features['ratio_uppercase'] = features['num_uppercase'] / len(full_text)
            features['ratio_digits'] = features['num_digits'] / len(full_text)
        
        return features
    
    def extract_sender_features(self, sender: str, body: str) -> dict:
        """Extract sender-based features"""
        features = {
            'sender_domain_mismatch': 0,
            'sender_has_numbers': 0,
            'sender_length': len(str(sender)),
        }
        
        if any(c.isdigit() for c in str(sender)):
            features['sender_has_numbers'] = 1
        
        sender_domain = ''
        if '@' in str(sender):
            sender_domain = str(sender).split('@')[-1].lower()
        
        if sender_domain:
            urls = self.url_pattern.findall(str(body))
            for url in urls:
                extracted = tldextract.extract(url)
                url_domain = f"{extracted.domain}.{extracted.suffix}".lower()
                if url_domain and url_domain != sender_domain:
                    features['sender_domain_mismatch'] = 1
                    break
        
        return features


# ==================== PHISHING DETECTOR ====================

class PhishingDetector:
    """Main phishing detection class"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = Path(model_dir)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.feature_extractor = EmailFeatureExtractor()
        
        print(f"Loading model on device: {self.device}")
        
        # Load tokenizer
        tokenizer_path = self.model_dir / 'tokenizer.pkl'
        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = joblib.load(f)
        
        # Load model
        model_path = self.model_dir / 'lstm_model.pth'
        checkpoint = torch.load(model_path, map_location=self.device)
        
        vocab_size = len(self.tokenizer.word2idx)
        embedding_dim = 128
        lstm_units = 64
        dropout_rate = 0.5
        
        self.model = BiLSTMClassifier(vocab_size, embedding_dim, lstm_units, dropout_rate)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.to(self.device)
        self.model.eval()
        
        print(f"✓ Model loaded successfully")
    
    def convert_frontend_to_model_format(self, email_data: Dict) -> Dict:
        """Convert frontend JSON to model format"""
        return {
            'subject': email_data.get('subject', ''),
            'body': email_data.get('body_full', ''),
            'sender': email_data.get('sender', '')
        }
    
    def predict(self, email_data: Dict) -> tuple:
        """Predict if email is phishing"""
        email = self.convert_frontend_to_model_format(email_data)
        
        # Prepare text for LSTM
        full_text = f"{email['subject']} {email['body']}"
        sequences = self.tokenizer.texts_to_sequences([full_text])
        
        # Pad sequence
        max_len = 200
        padded = np.zeros((1, max_len), dtype=np.int64)
        seq = sequences[0][:max_len]
        padded[0, :len(seq)] = seq
        
        # Predict
        with torch.no_grad():
            X_tensor = torch.LongTensor(padded).to(self.device)
            output = self.model(X_tensor)
            confidence = output.item()
        
        is_phishing = confidence >= 0.5
        return is_phishing, confidence
    
    def analyze_url_risk(self, url: str) -> Dict:
        """Analyze individual URL for risk factors"""
        risk_factors = []
        risk_score = 0
        url_lower = url.lower()
        
        # Dangerous file extensions
        dangerous_extensions = ['.sh', '.exe', '.bat', '.cmd', '.scr', '.vbs', '.ps1']
        if any(ext in url_lower for ext in dangerous_extensions):
            risk_factors.append('Dangerous file extension detected')
            risk_score += 40
        
        # IP addresses
        ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        if ip_pattern.search(url):
            risk_factors.append('Contains IP address')
            risk_score += 30
        
        # Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.online', '.top', '.club']
        if any(tld in url_lower for tld in suspicious_tlds):
            risk_factors.append('Suspicious top-level domain')
            risk_score += 20
        
        # Phishing keywords
        phishing_keywords = ['login', 'verify', 'account', 'secure', 'update', 'confirm', 'suspend']
        if any(keyword in url_lower for keyword in phishing_keywords):
            risk_factors.append('Contains phishing keywords')
            risk_score += 15
        
        # URL shorteners
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'is.gd']
        if any(shortener in url_lower for shortener in shorteners):
            risk_factors.append('URL shortener detected')
            risk_score += 10
        
        # Excessive length
        if len(url) > 100:
            risk_factors.append('Unusually long URL')
            risk_score += 10
        
        # Risk level
        if risk_score >= 50:
            risk_level = 'CRITICAL'
        elif risk_score >= 30:
            risk_level = 'HIGH'
        elif risk_score >= 15:
            risk_level = 'MEDIUM'
        elif risk_score > 0:
            risk_level = 'LOW'
        else:
            risk_level = 'SAFE'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors
        }
    
    def detect_red_flags(self, email_data: Dict, features: Dict, urls_analysis: List[Dict]) -> List[Dict]:
        """Detect all red flags in the email"""
        red_flags = []
        
        # Extract feature dictionaries
        url_features = features.get('url_features', {})
        text_features = features.get('text_features', {})
        sender_features = features.get('sender_features', {})
        
        # URL-based red flags
        if url_features.get('has_ip', 0):
            red_flags.append({
                'category': 'URL',
                'severity': 'CRITICAL',
                'flag': 'IP address in URL',
                'description': 'URLs with IP addresses are highly suspicious'
            })
        
        if url_features.get('has_phishing_keywords_in_url', 0):
            red_flags.append({
                'category': 'URL',
                'severity': 'HIGH',
                'flag': 'Phishing keywords in URL',
                'description': 'URL contains common phishing terms'
            })
        
        # Malicious files
        body = email_data.get('body_full', '')
        malicious_extensions = ['.sh', '.exe', '.bat', '.scr', '.vbs']
        for ext in malicious_extensions:
            if ext in body.lower():
                red_flags.append({
                    'category': 'MALWARE',
                    'severity': 'CRITICAL',
                    'flag': f'Malicious file extension: {ext}',
                    'description': f'{ext} files can execute malicious code'
                })
        
        # Sender-based
        if sender_features.get('sender_domain_mismatch', 0):
            red_flags.append({
                'category': 'SENDER',
                'severity': 'HIGH',
                'flag': 'Domain mismatch',
                'description': 'Sender domain does not match URLs in email'
            })
        
        # Content-based
        if text_features.get('num_exclamation', 0) > 3:
            red_flags.append({
                'category': 'CONTENT',
                'severity': 'MEDIUM',
                'flag': 'Excessive exclamation marks',
                'description': f'{text_features["num_exclamation"]} exclamation marks detected'
            })
        
        if text_features.get('ratio_uppercase', 0) > 0.3:
            red_flags.append({
                'category': 'CONTENT',
                'severity': 'MEDIUM',
                'flag': 'Excessive uppercase',
                'description': f'{text_features["ratio_uppercase"]*100:.1f}% uppercase text'
            })
        
        if text_features.get('has_phishing_keywords', 0):
            red_flags.append({
                'category': 'CONTENT',
                'severity': 'HIGH',
                'flag': 'Phishing keywords detected',
                'description': 'Contains common phishing terminology'
            })
        
        # URL risk-based
        for url_analysis in urls_analysis:
            if url_analysis['risk_level'] in ['CRITICAL', 'HIGH']:
                red_flags.append({
                    'category': 'URL',
                    'severity': url_analysis['risk_level'],
                    'flag': 'Dangerous URL detected',
                    'description': f"{url_analysis['url'][:50]}... - {', '.join(url_analysis['risk_factors'])}"
                })
        
        return red_flags
    
    def calculate_threat_level(self, is_phishing: bool, confidence: float, red_flags: List[Dict]) -> str:
        """Calculate overall threat level"""
        if not is_phishing:
            return 'SAFE'
        
        if confidence >= 0.95:
            critical_flags = sum(1 for flag in red_flags if flag['severity'] == 'CRITICAL')
            if critical_flags > 0:
                return 'CRITICAL'
            return 'HIGH'
        elif confidence >= 0.75:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_recommendations(self, threat_level: str, red_flags: List[Dict]) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if threat_level == 'SAFE':
            recommendations.append({
                'priority': 'INFO',
                'action': 'Email appears legitimate',
                'description': 'No immediate action required, but always verify sender before clicking links'
            })
            return recommendations
        
        if threat_level in ['CRITICAL', 'HIGH']:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'DELETE IMMEDIATELY',
                'description': 'This email contains dangerous elements. Do not interact with it.'
            })
            
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'DO NOT CLICK ANY LINKS',
                'description': 'Links in this email may lead to malware or credential theft'
            })
        
        has_malware = any('MALWARE' in flag['category'] for flag in red_flags)
        if has_malware:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'MALWARE DETECTED',
                'description': 'This email contains links to potentially malicious files'
            })
        
        recommendations.append({
            'priority': 'HIGH',
            'action': 'Report as phishing/spam',
            'description': 'Help improve email security by reporting this email'
        })
        
        recommendations.append({
            'priority': 'MEDIUM',
            'action': 'Block sender',
            'description': 'Prevent future emails from this sender'
        })
        
        return recommendations
    
    def analyze_email(self, email_data: Dict) -> Dict[str, Any]:
        """Complete analysis of a single email"""
        
        # Make prediction
        is_phishing, confidence = self.predict(email_data)
        
        # Extract features
        email = self.convert_frontend_to_model_format(email_data)
        url_features = self.feature_extractor.extract_url_features(email['body'])
        text_features = self.feature_extractor.extract_text_features(email['subject'], email['body'])
        sender_features = self.feature_extractor.extract_sender_features(email['sender'], email['body'])
        
        features = {
            'url_features': url_features,
            'text_features': text_features,
            'sender_features': sender_features
        }
        
        # Analyze URLs
        urls_analysis = []
        for url in email_data.get('urls_found', []):
            url_risk = self.analyze_url_risk(url)
            urls_analysis.append({
                'url': url,
                'risk_level': url_risk['risk_level'],
                'risk_score': url_risk['risk_score'],
                'risk_factors': url_risk['risk_factors']
            })
        
        # Detect red flags
        red_flags = self.detect_red_flags(email_data, features, urls_analysis)
        
        # Calculate threat level
        threat_level = self.calculate_threat_level(is_phishing, confidence, red_flags)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(threat_level, red_flags)
        
        # Calculate risk score
        base_score = confidence * 60
        flag_score = sum(15 if f['severity']=='CRITICAL' else 10 if f['severity']=='HIGH' else 5 for f in red_flags)
        risk_score = min(100, int(base_score + flag_score))
        
        # Build result
        result = {
            'email_id': email_data.get('email_id'),
            'sender': email_data.get('sender'),
            'sender_domain': email_data.get('sender_domain'),
            'subject': email_data.get('subject'),
            'date_received': email_data.get('date_received'),
            
            'prediction': {
                'is_phishing': is_phishing,
                'confidence': round(confidence, 4),
                'confidence_percentage': round(confidence * 100, 2),
                'threat_level': threat_level,
                'verdict': 'PHISHING' if is_phishing else 'LEGITIMATE',
                'risk_score': risk_score if is_phishing else 0
            },
            
            'url_analysis': {
                'total_urls': email_data.get('url_count', 0),
                'urls_found': urls_analysis,
                'has_suspicious_urls': any(u['risk_level'] in ['HIGH', 'CRITICAL'] for u in urls_analysis),
                'url_features': {
                    'num_urls': url_features['num_urls'],
                    'num_unique_domains': url_features['num_unique_domains'],
                    'has_ip_address': bool(url_features['has_ip']),
                    'has_phishing_keywords': bool(url_features.get('has_phishing_keywords_in_url', 0)),
                    'avg_url_length': round(url_features['avg_url_length'], 2)
                }
            },
            
            'content_analysis': {
                'text_features': {
                    'subject_length': text_features['subject_len'],
                    'body_length': text_features['body_len'],
                    'uppercase_ratio': round(text_features['ratio_uppercase'], 4),
                    'digit_count': text_features['num_digits'],
                    'exclamation_count': text_features['num_exclamation'],
                    'question_count': text_features['num_question'],
                    'has_money_symbols': bool(text_features['has_money_symbol']),
                    'has_phishing_keywords': bool(text_features['has_phishing_keywords'])
                },
                'sender_features': {
                    'sender_length': sender_features['sender_length'],
                    'sender_has_numbers': bool(sender_features['sender_has_numbers']),
                    'domain_mismatch': bool(sender_features['sender_domain_mismatch'])
                }
            },
            
            'security_indicators': {
                'red_flags': red_flags,
                'red_flag_count': len(red_flags)
            },
            
            'recommendations': recommendations,
            
            'analysis_metadata': {
                'analyzed_at': datetime.now().isoformat(),
                'model_type': 'LSTM (PyTorch)',
                'device': str(self.device)
            }
        }
        
        return result
    
    def analyze_batch(self, emails: List[Dict]) -> Dict[str, Any]:
        """Analyze multiple emails"""
        results = []
        
        for email in emails:
            try:
                result = self.analyze_email(email)
                results.append(result)
            except Exception as e:
                results.append({
                    'email_id': email.get('email_id'),
                    'error': str(e),
                    'status': 'FAILED'
                })
        
        # Calculate statistics
        successful = [r for r in results if 'error' not in r]
        phishing_count = sum(1 for r in successful if r['prediction']['is_phishing'])
        
        batch_summary = {
            'total_emails': len(emails),
            'analyzed_successfully': len(successful),
            'failed': len(results) - len(successful),
            'phishing_detected': phishing_count,
            'legitimate': len(successful) - phishing_count,
            'phishing_percentage': round((phishing_count / len(successful) * 100) if successful else 0, 2),
            'threat_distribution': {
                'CRITICAL': sum(1 for r in successful if r['prediction'].get('threat_level') == 'CRITICAL'),
                'HIGH': sum(1 for r in successful if r['prediction'].get('threat_level') == 'HIGH'),
                'MEDIUM': sum(1 for r in successful if r['prediction'].get('threat_level') == 'MEDIUM'),
                'LOW': sum(1 for r in successful if r['prediction'].get('threat_level') == 'LOW'),
                'SAFE': sum(1 for r in successful if r['prediction'].get('threat_level') == 'SAFE')
            }
        }
        
        return {
            'batch_summary': batch_summary,
            'results': results,
            'analyzed_at': datetime.now().isoformat()
        }


# ==================== MAIN FUNCTION ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Phishing Email Detection Pipeline')
    parser.add_argument('--input', required=True, help='Input JSON file with emails')
    parser.add_argument('--output', default='analysis_results.json', help='Output JSON file')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON')
    args = parser.parse_args()
    
    print("="*80)
    print("PHISHING EMAIL DETECTION PIPELINE")
    print("="*80)
    
    # Load emails
    print(f"\nLoading emails from: {args.input}")
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            emails = json.load(f)
        print(f"✓ Loaded {len(emails)} email(s)")
    except Exception as e:
        print(f"ERROR: Could not load input file: {e}")
        sys.exit(1)
    
    # Initialize detector
    print("\nInitializing detector...")
    try:
        detector = PhishingDetector()
    except Exception as e:
        print(f"ERROR: Could not load model: {e}")
        sys.exit(1)
    
    # Analyze emails
    print(f"\nAnalyzing {len(emails)} email(s)...\n")
    results = detector.analyze_batch(emails)
    
    # Save results
    with open(args.output, 'w', encoding='utf-8') as f:
        if args.pretty:
            json.dump(results, f, indent=2, ensure_ascii=False)
        else:
            json.dump(results, f, ensure_ascii=False)
    
    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\n✓ Results saved to: {args.output}")
    print(f"\nBatch Summary:")
    print(f"  Total emails:      {results['batch_summary']['total_emails']}")
    print(f"  Phishing detected: {results['batch_summary']['phishing_detected']}")
    print(f"  Legitimate:        {results['batch_summary']['legitimate']}")
    print(f"  Phishing rate:     {results['batch_summary']['phishing_percentage']}%")
    
    if results['batch_summary']['phishing_detected'] > 0:
        print(f"\n  Threat Distribution:")
        for level, count in results['batch_summary']['threat_distribution'].items():
            if count > 0:
                print(f"    {level}: {count}")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    main()
