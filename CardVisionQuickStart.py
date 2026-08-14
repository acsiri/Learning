"""
Simple Vision AI Card Reader - Quick Start Example
"""

import os
import base64
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def read_card_simple(image_path):
    """
    Simple one-function approach to read card details
    
    Args:
        image_path: Path to the card image
    
    Returns:
        String with extracted details
    """
    # Configure API
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Read image file
    with open(image_path, 'rb') as f:
        image_data = base64.standard_b64encode(f.read()).decode('utf-8')
    
    # Determine media type
    ext = os.path.splitext(image_path)[1].lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    media_type = media_types.get(ext, 'image/jpeg')
    
    # Create image object
    image = {
        'inline_data': {
            'mime_type': media_type,
            'data': image_data
        }
    }
    
    # Send to Vision AI
    response = model.generate_content([
        image,
        "Extract all visible text and details from this card image. List each detail clearly."
    ])
    
    return response.text


def read_card_with_structure(image_path):
    """
    Extract card details in a structured format (JSON)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.standard_b64encode(f.read()).decode('utf-8')
    
    ext = os.path.splitext(image_path)[1].lower()
    media_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', 
                   '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'}
    media_type = media_types.get(ext, 'image/jpeg')
    
    image = {
        'inline_data': {
            'mime_type': media_type,
            'data': image_data
        }
    }
    
    # Request structured output
    prompt = """
    Extract card details and return ONLY a JSON object with:
    {
        "cardholder_name": "...",
        "card_number_last_4": "...",
        "card_type": "...",
        "expiry_date": "...",
        "issuer": "...",
        "visible_text": ["...", "..."],
        "image_quality": "high|medium|low",
        "confidence": "high|medium|low"
    }
    
    SECURITY: Only show last 4 digits of card number. Do not include CVV.
    """
    
    response = model.generate_content([image, prompt])
    return response.text


def read_id_card(image_path):
    """
    Extract details from ID card (driver's license, passport, national ID, etc.)
    """
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    with open(image_path, 'rb') as f:
        image_data = base64.standard_b64encode(f.read()).decode('utf-8')
    
    ext = os.path.splitext(image_path)[1].lower()
    media_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', 
                   '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'}
    media_type = media_types.get(ext, 'image/jpeg')
    
    image = {
        'inline_data': {
            'mime_type': media_type,
            'data': image_data
        }
    }
    
    prompt = """
    Extract ID card information and return as JSON:
    {
        "document_type": "driver_license|passport|national_id|...",
        "full_name": "...",
        "date_of_birth": "...",
        "id_number": "...",
        "expiration_date": "...",
        "address": "...",
        "gender": "...",
        "height": "...",
        "hair_color": "...",
        "issuing_state": "...",
        "issue_date": "..."
    }
    """
    
    response = model.generate_content([image, prompt])
    return response.text


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("QUICK START: VISION AI CARD READER")
    print("="*70)
    
    # Example 1: Simple text extraction
    print("\n[EXAMPLE 1] Simple Card Text Extraction")
    print("-" * 70)
    image_file = "sample_card.jpg"
    
    if os.path.exists(image_file):
        result = read_card_simple(image_file)
        print("Extracted Text:")
        print(result)
    else:
        print(f"⚠ Image not found: {image_file}")
        print("  Create or provide a card image file to test")
    
    # Example 2: Structured extraction
    print("\n[EXAMPLE 2] Structured Card Details (JSON)")
    print("-" * 70)
    if os.path.exists(image_file):
        result = read_card_with_structure(image_file)
        print("Structured Details:")
        print(result)
    
    # Example 3: ID Card extraction
    print("\n[EXAMPLE 3] ID Card Extraction")
    print("-" * 70)
    id_image = "sample_id.jpg"
    if os.path.exists(id_image):
        result = read_id_card(id_image)
        print("ID Details:")
        print(result)
    else:
        print(f"⚠ ID image not found: {id_image}")
    
    print("\n" + "="*70)
    print("SETUP REQUIRED:")
    print("="*70)
    print("1. Set GEMINI_API_KEY in your .env file")
    print("2. Provide a card image file (sample_card.jpg)")
    print("3. Run this script again")
    print("="*70)
