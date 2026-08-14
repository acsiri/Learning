"""
Vision AI Card Extraction - Complete Reference Guide
=======================================================

OVERVIEW:
Vision AI uses advanced machine learning models to analyze images and extract
information intelligently, unlike simple OCR which only reads text.

PROVIDERS & MODELS:
1. Google Gemini Vision API (recommended for this setup)
   - gemini-1.5-flash: Faster, cost-effective
   - gemini-1.5-pro: More accurate, handles complex layouts
   - gemini-2.0-flash: Latest model

2. OpenAI GPT-4 Vision
3. Claude Vision (Anthropic)
4. Microsoft Azure Computer Vision
5. AWS Rekognition

SECURITY BEST PRACTICES:
=========================
1. NEVER store full card numbers - use last 4 digits only
2. NEVER store or log CVV/CVC
3. NEVER transmit card data unencrypted
4. Use API with HTTPS only
5. Rotate API keys regularly
6. Implement rate limiting
7. Log all card processing for audit trails
8. Use PCI DSS compliant infrastructure

CARD DETAILS EXTRACTION:
=========================
"""

# ============================================================================
# MINIMAL EXAMPLE - 5 Lines
# ============================================================================

"""
from dotenv import load_dotenv
import google.generativeai as genai
import base64

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Read and send image
with open('card.jpg', 'rb') as f:
    img_data = base64.standard_b64encode(f.read()).decode()

image = {'inline_data': {'mime_type': 'image/jpeg', 'data': img_data}}
response = genai.GenerativeModel("gemini-1.5-flash").generate_content([
    image, 
    "Extract card number (last 4 only), cardholder name, and expiry date. Return as JSON."
])

print(response.text)
"""

# ============================================================================
# COMMON PROMPTS FOR DIFFERENT CARD TYPES
# ============================================================================

PROMPTS = {
    "credit_debit": """
    Extract these fields from the credit/debit card:
    - Cardholder Name
    - Card Type (Visa/Mastercard/Amex/Discover)
    - Last 4 Digits (SECURITY: show only last 4)
    - Expiration Date (MM/YY)
    - Issuer/Bank Name
    - Card Color
    
    Return as JSON. Do NOT include full card number or CVV.
    """,
    
    "business_card": """
    Extract contact information from business card:
    - Full Name
    - Title/Position
    - Company Name
    - Email Address
    - Phone Number
    - Website
    - Address
    - Any other contact details
    
    Return as JSON.
    """,
    
    "id_card": """
    Extract ID information:
    - Document Type (Driver License/Passport/ID Card)
    - Full Name
    - Date of Birth
    - ID Number
    - Expiration Date
    - Address
    - Gender
    - Issuing Authority
    
    Return as JSON.
    """,
    
    "insurance_card": """
    Extract insurance information:
    - Insurance Provider
    - Member Name
    - Member ID
    - Group Number
    - Effective Date
    - Policy Holder Name
    - Coverage Type
    
    Return as JSON.
    """,
    
    "travel_card": """
    Extract travel/transportation card info:
    - Card Type (Train/Bus/Airline/etc)
    - Passenger Name
    - Card/Ticket Number (last 4 only)
    - Valid From/To Dates
    - Route/Destination
    - Card Status
    
    Return as JSON.
    """
}

# ============================================================================
# COMPARISON: DIFFERENT APPROACHES
# ============================================================================

COMPARISON = """
APPROACH 1: Simple OCR (EasyOCR)
  Pros: Fast, local processing, low cost
  Cons: No understanding, many false positives, layout issues
  Use Case: When speed > accuracy needed
  
APPROACH 2: Vision AI (Gemini/Claude)
  Pros: High accuracy, semantic understanding, handles complex layouts
  Cons: API cost, requires internet, rate limits
  Use Case: Production systems needing high accuracy
  
APPROACH 3: Specialized Services (AWS Rekognition, Azure Computer Vision)
  Pros: Purpose-built, good integration with cloud
  Cons: Expensive, vendor lock-in
  Use Case: Enterprise systems with existing cloud infrastructure

RECOMMENDED: Vision AI (Approach 2) for most use cases
"""

# ============================================================================
# ERROR HANDLING & EDGE CASES
# ============================================================================

"""
Common issues and solutions:

1. BLURRY/LOW QUALITY IMAGES
   Solution: Validate image quality before sending, provide user feedback
   
2. GLARE/REFLECTIONS
   Solution: Check for shiny surfaces, ask user to retake
   
3. PARTIALLY OBSCURED CARD
   Solution: Require full card visibility in image
   
4. MULTIPLE CARDS IN IMAGE
   Solution: Ask user to provide single card only
   
5. DAMAGED/EXPIRED CARDS
   Solution: Flag these cases, handle based on business logic
   
6. API RATE LIMITS
   Solution: Implement queue, retry with backoff
   
7. INVALID JSON RESPONSE
   Solution: Parse as text, regex extraction, human review
   
8. PII IN LOGS
   Solution: Sanitize logs, store only hashes, follow PCI DSS
"""

# ============================================================================
# ADVANCED FEATURES
# ============================================================================

"""
1. CONFIDENCE SCORING
   - Ask vision AI to provide confidence for each field
   - Flag low-confidence results for manual review
   
2. FIELD VALIDATION
   - Validate expiry date format and not expired
   - Validate card number checksum (Luhn algorithm)
   - Validate email format, phone format
   
3. DUPLICATE DETECTION
   - Hash processed cards to detect duplicates
   - Flag suspicious patterns
   
4. FRAUD DETECTION
   - Compare against known fraudulent cards
   - Check for altered/tampered cards
   - Verify issuer is legitimate
   
5. OCR FALLBACK
   - If vision AI fails, fall back to traditional OCR
   - Combine results from multiple approaches
   
6. MULTILINGUAL SUPPORT
   - Process cards in different languages
   - Map fields across language variations
"""

# ============================================================================
# CODE TEMPLATE - PRODUCTION READY
# ============================================================================

CODE_TEMPLATE = """
import os
import base64
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from dataclasses import dataclass
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CardDetails:
    cardholder_name: Optional[str] = None
    card_type: Optional[str] = None
    last_4_digits: Optional[str] = None
    expiry_date: Optional[str] = None
    issuer: Optional[str] = None
    confidence: Optional[float] = None
    raw_response: Optional[str] = None

class SecureCardReader:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("✓ Vision AI reader initialized")
    
    def extract_card_details(self, image_path: str) -> CardDetails:
        \"\"\"Extract card details securely\"\"\"
        try:
            # Validate image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            if os.path.getsize(image_path) > 5_000_000:  # 5MB limit
                raise ValueError("Image too large (max 5MB)")
            
            # Load image
            with open(image_path, 'rb') as f:
                img_data = base64.standard_b64encode(f.read()).decode()
            
            image = {
                'inline_data': {
                    'mime_type': 'image/jpeg',
                    'data': img_data
                }
            }
            
            # Extract details (SECURITY: specific about what to extract)
            response = self.model.generate_content([
                image,
                '''Extract ONLY these fields:
                - Cardholder Name
                - Card Type
                - Last 4 Digits (ONLY last 4, never full number)
                - Expiry Date
                - Issuer
                
                CRITICAL: Do not extract or include:
                - Full card number
                - CVV/CVC
                - Any sensitive data beyond what listed
                
                Return as JSON only.'''
            ])
            
            # Parse response (sanitize before logging)
            logger.info(f"✓ Extracted details from {image_path} (no PII logged)")
            
            # Return structured data
            import json
            try:
                data = json.loads(response.text)
                return CardDetails(
                    cardholder_name=data.get('Cardholder Name'),
                    card_type=data.get('Card Type'),
                    last_4_digits=data.get('Last 4 Digits'),
                    expiry_date=data.get('Expiry Date'),
                    issuer=data.get('Issuer'),
                    confidence=data.get('confidence')
                )
            except json.JSONDecodeError:
                return CardDetails(raw_response=response.text)
        
        except Exception as e:
            logger.error(f"Error extracting card: {str(e)}")
            raise

# Usage
if __name__ == "__main__":
    reader = SecureCardReader()
    details = reader.extract_card_details("card.jpg")
    print(details)
"""

# ============================================================================
# COST COMPARISON (As of May 2026)
# ============================================================================

"""
Provider              | Cost per Image | Accuracy | Speed  | Best For
---------------------|----------------|----------|--------|----------
Google Gemini Flash   | $0.075/image   | 90-95%   | 2-3s   | Most use cases
Google Gemini Pro     | $0.30/image    | 95-98%   | 3-5s   | High accuracy needed
OpenAI GPT-4 Vision   | $0.01-0.03/img | 92-96%   | 2-4s   | OpenAI ecosystem
Claude Vision         | $0.003-0.015   | 88-94%   | 3-5s   | Budget conscious
AWS Rekognition       | $0.10/image    | 85-92%   | 1-2s   | AWS users
Azure Computer Vision | $1-2/1000 calls| 90-95%   | 2-3s   | Microsoft users
Local OCR (EasyOCR)   | $0 (free)      | 70-85%   | 1-2s   | Simple text only

RECOMMENDATION: Use Gemini Flash for most applications
"""

# ============================================================================
# TESTING & VALIDATION
# ============================================================================

"""
Test with these card images:
1. Clear, well-lit photo: Expected 95%+ accuracy
2. Angled photo: Expected 85-90% accuracy
3. Partially obscured: Expected 70-80% accuracy
4. Very blurry: Expected <60% accuracy

Validate with:
- Test data set with known results
- Compare multiple AI providers
- Manual review of low-confidence results
- Monitor error rates over time
"""

print(__doc__)
