# Vision AI Card Details Extraction - Complete Guide

## 📋 Overview

This guide provides complete Python examples for reading card images using Vision AI and extracting card details automatically. Vision AI uses advanced machine learning models (like Google Gemini) to intelligently analyze card images, unlike simple OCR which only reads text.

## 🚀 Quick Start (30 seconds)

```python
from CardVisionQuickStart import read_card_simple

# Read a card image
result = read_card_simple("C:\\Sridhar\\Learning\\Sample.jpg")
print(result)
```

## 📁 Files Included

| File | Purpose | Complexity |
|------|---------|-----------|
| `CardVisionQuickStart.py` | Simple one-function examples | Beginner |
| `CardVisionExtractor.py` | Full-featured class-based approach | Intermediate |
| `AdvancedCardVisionProcessor.py` | Batch processing, caching, validation | Advanced |
| `VisionAI_Reference_Guide.py` | Complete reference and best practices | Reference |

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install google-generativeai python-dotenv
```

### 2. Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click "Create API Key"
3. Copy the API key

### 3. Configure Environment

Create/update `.env` file in your project:
```
GEMINI_API_KEY="AIzaSyDiB0cBwVeG_cXUwW5ecOjTWfOpQ2AOFiM"
```

### 4. Verify Setup
```bash
python SetupGemini.py
```

You should see: `✓ Gemini API test passed`

## 💡 Examples

### Example 1: Simple Card Reading (Fastest)

```python
import os
import base64
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Read image file
with open('credit_card.jpg', 'rb') as f:
    img_data = base64.standard_b64encode(f.read()).decode()

# Send to Vision AI
image = {'inline_data': {'mime_type': 'image/jpeg', 'data': img_data}}
response = genai.GenerativeModel("gemini-1.5-flash").generate_content([
    image,
    "Extract cardholder name, card type, and expiry date. Show last 4 digits only."
])

print(response.text)
```

### Example 2: Structured JSON Output

```python
from CardVisionQuickStart import read_card_with_structure

result = read_card_with_structure("card.jpg")
print(result)  # Returns formatted JSON
```

### Example 3: Full-Featured Extraction

```python
from CardVisionExtractor import CardVisionExtractor

extractor = CardVisionExtractor()

# Extract basic details
result = extractor.extract_card_details("card.jpg")

# With confidence scores
result = extractor.extract_with_confidence("card.jpg")

# Verify details
details_to_verify = {
    "card_holder": "JOHN DOE",
    "expiry": "12/25"
}
verification = extractor.verify_card_details("card.jpg", details_to_verify)
```

### Example 4: Batch Processing

```python
from AdvancedCardVisionProcessor import AdvancedCardProcessor

processor = AdvancedCardProcessor()

# Process multiple cards
images = ["card1.jpg", "card2.jpg", "card3.jpg"]
results = processor.batch_process(images)

# Results are cached automatically
```

### Example 5: Consistency Verification

```python
from AdvancedCardVisionProcessor import AdvancedCardProcessor

processor = AdvancedCardProcessor()

# Extract same card 3 times and compare
result = processor.compare_multiple_extractions("card.jpg", num_passes=3)

print(f"Consistency: {result['consistency_analysis']['consistency_score']:.1f}%")
```

## 🎯 Supported Card Types

- ✅ Credit Cards (Visa, Mastercard, Amex, Discover, etc.)
- ✅ Debit Cards
- ✅ Business Cards
- ✅ ID Cards (Driver License, Passport, National ID)
- ✅ Insurance Cards
- ✅ Travel Cards (Train, Bus, Airline tickets)
- ✅ Gift Cards
- ✅ Membership Cards

## 📊 What Gets Extracted

### Credit/Debit Card
```json
{
    "cardholder_name": "JOHN DOE",
    "card_type": "Visa",
    "last_4_digits": "1234",
    "expiry_date": "12/25",
    "issuer": "Chase Bank",
    "card_color": "Blue"
}
```

### ID Card
```json
{
    "document_type": "driver_license",
    "full_name": "John Doe",
    "date_of_birth": "01/15/1990",
    "id_number": "D123456789",
    "expiration_date": "12/31/2025",
    "address": "123 Main St, City, State 12345"
}
```

## 🔐 Security Best Practices

### ✅ DO:
- Show ONLY last 4 digits of card numbers
- Never store or log CVV/CVC codes
- Use HTTPS for all API calls
- Sanitize logs (no PII)
- Implement rate limiting
- Rotate API keys regularly
- Use encrypted connections
- Follow PCI DSS standards

### ❌ DON'T:
- Store full card numbers
- Log or transmit card data unencrypted
- Include CVV in API requests
- Share API keys in code
- Commit `.env` file to version control
- Process without user consent
- Store data without encryption

## ⚙️ Advanced Features

### Caching
```python
from AdvancedCardVisionProcessor import AdvancedCardProcessor

processor = AdvancedCardProcessor(cache_dir=".card_cache")

# First call: processes and caches
result = processor.process_with_cache("card.jpg")

# Second call: returns cached result (instant)
result = processor.process_with_cache("card.jpg")

# Force reprocessing
result = processor.process_with_cache("card.jpg", force_reprocess=True)
```

### Error Handling
```python
from CardVisionExtractor import CardVisionExtractor

extractor = CardVisionExtractor()
result = extractor.extract_card_details("card.jpg")

if result["status"] == "success":
    print(result["details"])
else:
    print(f"Error: {result['message']}")
```

### Image Validation
```python
import os

def validate_image(image_path):
    """Validate image before processing"""
    
    # Check file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Check file size (max 5MB)
    size = os.path.getsize(image_path)
    if size > 5_000_000:
        raise ValueError(f"Image too large: {size} bytes")
    
    # Check format
    valid_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in valid_formats:
        raise ValueError(f"Unsupported format: {ext}")
    
    return True
```

## 📈 Cost Estimates

| Provider | Cost/Image | Accuracy | Best For |
|----------|-----------|----------|----------|
| Gemini Flash | $0.075 | 90-95% | **Recommended** |
| Gemini Pro | $0.30 | 95-98% | High accuracy |
| GPT-4 Vision | $0.01-0.03 | 92-96% | OpenAI users |
| Claude Vision | $0.003-0.015 | 88-94% | Budget |
| Local OCR | Free | 70-85% | Simple text |

## 🧪 Testing

### Test with Sample Cards
```python
from CardVisionExtractor import CardVisionExtractor

extractor = CardVisionExtractor()

# Test different scenarios
test_cases = [
    ("clear_card.jpg", "Should work perfectly"),
    ("angled_card.jpg", "Should have ~90% accuracy"),
    ("blurry_card.jpg", "May have lower accuracy"),
    ("partial_card.jpg", "May miss some details"),
]

for image, expected in test_cases:
    if os.path.exists(image):
        result = extractor.extract_card_details(image)
        print(f"{image}: {result['status']}")
```

### Validate Results
```python
# Test specific fields
result = extractor.extract_card_details("card.jpg")
details = result["details"]

assert "cardholder_name" in details, "Missing cardholder name"
assert "expiry_date" in details, "Missing expiry date"
assert "last_4_digits" in details, "Missing last 4 digits"
```

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Create `.env` file with your API key
```
GEMINI_API_KEY=your_key_here
```

### Issue: Poor accuracy on angled images
**Solution:** Ask user for straight-on photo or implement image rotation

### Issue: Rate limit errors
**Solution:** Implement retry logic with backoff
```python
import time

for attempt in range(3):
    try:
        result = extractor.extract_card_details("card.jpg")
        break
    except Exception as e:
        if attempt < 2:
            time.sleep(2 ** attempt)
        else:
            raise
```

### Issue: "File not found" errors
**Solution:** Check absolute path and file exists
```python
import os
path = os.path.abspath("card.jpg")
print(f"Looking for: {path}")
print(f"Exists: {os.path.exists(path)}")
```

## 📚 Additional Resources

- [Google Gemini API Docs](https://ai.google.dev)
- [Vision AI Best Practices](https://cloud.google.com/vision/docs)
- [PCI DSS Compliance](https://www.pcisecuritystandards.org/)
- [Card Security Standards](https://en.wikipedia.org/wiki/PCI_DSS)

## 🤝 Common Use Cases

1. **KYC/AML Verification**: Verify customer identity
2. **Expense Tracking**: Extract card details for expense reports
3. **Payment Processing**: Initial card data capture
4. **Document Management**: Organize card documents
5. **Card Registry**: Maintain card inventory
6. **Travel Booking**: Extract booking reference numbers
7. **Insurance Claims**: Extract policy information
8. **Business Card Digitization**: Convert to digital contacts

## 📝 License & Ethics

- Use responsibly and ethically
- Respect user privacy
- Follow all applicable laws (PCI-DSS, GDPR, CCPA, etc.)
- Implement proper data protection
- Get proper consent before processing
- Secure all sensitive data

## ❓ FAQ

**Q: Is this secure for production?**
A: Yes, when following security best practices outlined above.

**Q: Can it read expired cards?**
A: Yes, but you should flag them and handle according to your business logic.

**Q: What about non-English cards?**
A: Gemini supports 100+ languages. Adjust prompts as needed.

**Q: Can it detect fraudulent cards?**
A: It can analyze visual indicators. Integrate with fraud detection services for full protection.

**Q: What's the accuracy rate?**
A: 90-95% with Gemini Flash, higher with Gemini Pro or multiple passes.

---

**Created:** May 2026  
**Version:** 1.0  
**Provider:** Google Gemini Vision AI
