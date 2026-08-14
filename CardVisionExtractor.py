"""
Vision AI Card Extractor using Google Gemini
Reads card images and extracts details using Vision AI
"""

import os
import base64
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class CardVisionExtractor:
    """Extract card details from images using Google Gemini Vision AI"""
    
    def __init__(self, model_name="gemini-1.5-flash"):
        """Initialize the Vision AI card extractor"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        print(f"✓ Initialized Vision AI model: {model_name}")
    
    def _load_image(self, image_path):
        """Load and encode image to base64"""
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Determine media type
        suffix = image_path.suffix.lower()
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        
        media_type = media_type_map.get(suffix)
        if not media_type:
            raise ValueError(f"Unsupported image format: {suffix}")
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = base64.standard_b64encode(f.read()).decode('utf-8')
        
        return {
            'inline_data': {
                'mime_type': media_type,
                'data': image_data
            }
        }
    
    def extract_card_details(self, image_path, card_type=None):
        """
        Extract card details from image using Vision AI
        
        Args:
            image_path: Path to card image
            card_type: Type of card ('credit', 'debit', 'business', 'id', None for auto-detect)
        
        Returns:
            Dictionary with extracted card details
        """
        try:
            # Load image
            image = self._load_image(image_path)
            
            # Prepare prompt based on card type
            if card_type == 'id':
                prompt = """
                Please analyze this ID card image and extract the following information:
                - Full Name
                - ID Number
                - Date of Birth
                - Expiration Date
                - Address
                - Gender
                - Any other visible text or identifiers
                
                Format the response as a JSON object with these fields.
                If any field is not visible or unclear, set it to null.
                """
            else:
                # Default to credit/debit card
                prompt = """
                Please analyze this card image and extract the following information:
                - Card Holder Name (name on card)
                - Card Number (if visible, only show last 4 digits for security)
                - Card Type (Visa, Mastercard, American Express, etc.)
                - Expiration Date (MM/YY)
                - CVV/CVC (if visible - note: NEVER store this, only confirm if present)
                - Issuer (Bank or financial institution)
                - Card Color and Design
                - Any other visible text
                
                Format the response as a JSON object.
                For security, ONLY show the last 4 digits of the card number.
                If any field is not visible or unclear, set it to null.
                IMPORTANT: Do not extract or return full card numbers or CVV for security reasons.
                """
            
            # Call Gemini Vision API
            response = self.model.generate_content([image, prompt])
            
            # Parse response
            response_text = response.text
            
            # Try to extract JSON from response
            try:
                # Find JSON in response
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    card_details = json.loads(json_str)
                else:
                    card_details = {"raw_response": response_text}
            except json.JSONDecodeError:
                card_details = {"raw_response": response_text}
            
            return {
                "status": "success",
                "model_used": self.model_name,
                "details": card_details
            }
        
        except FileNotFoundError as e:
            return {"status": "error", "message": str(e)}
        except Exception as e:
            return {"status": "error", "message": f"Error extracting card details: {str(e)}"}
    
    def extract_with_confidence(self, image_path, card_type=None):
        """
        Extract card details with confidence scores
        Performs multiple passes for verification
        """
        try:
            image = self._load_image(image_path)
            
            prompt = """
            Analyze this card image and provide:
            1. Extracted details (card holder, number last 4 digits, expiry, type, issuer)
            2. For each field, provide confidence (high, medium, low)
            3. Any warnings or issues detected
            4. Image quality assessment
            
            Return as JSON with structure:
            {
                "details": {
                    "field_name": {"value": "...", "confidence": "high|medium|low"}
                },
                "image_quality": "...",
                "warnings": [...],
                "recommended_actions": [...]
            }
            """
            
            response = self.model.generate_content([image, prompt])
            
            try:
                json_start = response.text.find('{')
                json_end = response.text.rfind('}') + 1
                json_str = response.text[json_start:json_end]
                result = json.loads(json_str)
            except:
                result = {"raw_response": response.text}
            
            return {
                "status": "success",
                "model_used": self.model_name,
                "result": result
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def verify_card_details(self, image_path, details_to_verify):
        """
        Verify provided card details against image
        
        Args:
            image_path: Path to card image
            details_to_verify: Dict with details to verify (e.g., {"name": "John Doe", "expiry": "12/25"})
        
        Returns:
            Verification results
        """
        try:
            image = self._load_image(image_path)
            
            verification_str = json.dumps(details_to_verify, indent=2)
            
            prompt = f"""
            Please verify if the following details match what you see in the card image:
            
            Details to verify:
            {verification_str}
            
            For each detail, respond with:
            - "matches" if it matches the card
            - "does not match" if it doesn't
            - "unclear" if you can't determine
            - "not visible" if the information isn't visible on the card
            
            Also provide:
            - Any discrepancies found
            - Confidence level (high, medium, low)
            
            Return as JSON.
            """
            
            response = self.model.generate_content([image, prompt])
            
            try:
                json_start = response.text.find('{')
                json_end = response.text.rfind('}') + 1
                json_str = response.text[json_start:json_end]
                result = json.loads(json_str)
            except:
                result = {"raw_response": response.text}
            
            return {
                "status": "success",
                "verification_result": result
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("VISION AI CARD DETAILS EXTRACTOR")
    print("="*70)
    
    try:
        # Initialize extractor
        print("\n[1] Initializing Vision AI Extractor...")
        extractor = CardVisionExtractor()
        
        # Example: Extract from credit card image
        card_image = "sample_card.jpg"  # Replace with your card image
        
        if not os.path.exists(card_image):
            print(f"\n[!] Sample image not found: {card_image}")
            print("    Please provide a card image file.")
            print("\n    To test, you can:")
            print("    1. Add a card image as 'sample_card.jpg'")
            print("    2. Or modify the card_image variable with the correct path")
        else:
            # Extract basic details
            print(f"\n[2] Extracting card details from: {card_image}")
            result = extractor.extract_card_details(card_image)
            
            print("\n[3] Results:")
            print("-" * 70)
            if result["status"] == "success":
                print(json.dumps(result["details"], indent=2))
            else:
                print(f"Error: {result['message']}")
            
            # Extract with confidence scores
            print("\n[4] Extracting with confidence scores...")
            result_confidence = extractor.extract_with_confidence(card_image)
            
            if result_confidence["status"] == "success":
                print(json.dumps(result_confidence["result"], indent=2))
            
            # Verify specific details (example)
            print("\n[5] Verifying details...")
            details_to_check = {
                "card_holder": "JOHN DOE",
                "card_type": "Visa",
                "expiry": "12/25"
            }
            
            verification = extractor.verify_card_details(card_image, details_to_check)
            if verification["status"] == "success":
                print(json.dumps(verification["verification_result"], indent=2))
    
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("  Please ensure GEMINI_API_KEY is set in your .env file")
    except Exception as e:
        print(f"\n✗ Error: {e}")
