"""
Card Capture Integration Example
Shows how to integrate credit card capture with camera systems
"""

import json
import requests
from datetime import datetime
from typing import Dict, Optional


class CardCaptureClient:
    """
    Client for interacting with the card capture backend
    Can be used to process card data from forms or other sources
    """
    
    def __init__(self, backend_url: str = 'http://localhost:5000'):
        """
        Initialize the card capture client
        
        Args:
            backend_url: URL of the Flask backend
        """
        self.backend_url = backend_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def health_check(self) -> bool:
        """
        Check if backend is running
        
        Returns:
            True if backend is healthy
        """
        try:
            response = self.session.get(f'{self.backend_url}/api/health', timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def validate_card(self, card_data: Dict) -> Dict:
        """
        Validate card details without capturing
        
        Args:
            card_data: Dictionary with cardholder, cardNumber, expiry, cvv
            
        Returns:
            Validation result with detailed breakdown
        """
        try:
            response = self.session.post(
                f'{self.backend_url}/api/validate-card',
                json=card_data,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def capture_card(self, card_data: Dict) -> Dict:
        """
        Capture and process credit card data
        
        Args:
            card_data: Dictionary with card information
            
        Returns:
            Capture result with success/error status
        """
        try:
            response = self.session.post(
                f'{self.backend_url}/api/capture-card',
                json=card_data,
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'code': 'REQUEST_ERROR'
            }
    
    def get_transactions(self) -> Dict:
        """
        Get transaction history (masked)
        
        Returns:
            List of recent transactions
        """
        try:
            response = self.session.get(
                f'{self.backend_url}/api/transactions',
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# ==================== Examples ====================

def example_basic_capture():
    """Example 1: Basic card capture"""
    print("\n" + "="*60)
    print("Example 1: Basic Card Capture")
    print("="*60)
    
    client = CardCaptureClient()
    
    # Check if backend is running
    if not client.health_check():
        print("⚠️  Backend is not running!")
        print("   Start it with: python card_capture_backend.py")
        return
    
    print("✓ Backend is running")
    
    # Prepare card data
    card_data = {
        'cardholder': 'JOHN DOE',
        'cardNumber': '4532123456789010',
        'expiry': '12/25',
        'cvv': '123',
        'email': 'john@example.com',
        'cardType': 'visa'
    }
    
    # Capture card
    print("\n📤 Capturing card details...")
    result = client.capture_card(card_data)
    
    print(f"Result: {json.dumps(result, indent=2)}")


def example_validation():
    """Example 2: Validate without capturing"""
    print("\n" + "="*60)
    print("Example 2: Card Validation (No Capture)")
    print("="*60)
    
    client = CardCaptureClient()
    
    test_cases = [
        {
            'name': 'Valid Card',
            'data': {
                'cardholder': 'JANE SMITH',
                'cardNumber': '5425 2334 3010 9903',
                'expiry': '12/25',
                'cvv': '123'
            }
        },
        {
            'name': 'Invalid Card Number',
            'data': {
                'cardholder': 'INVALID USER',
                'cardNumber': '1234 5678 9012 3456',  # Fails Luhn check
                'expiry': '12/25',
                'cvv': '123'
            }
        },
        {
            'name': 'Expired Card',
            'data': {
                'cardholder': 'EXPIRED USER',
                'cardNumber': '4532 1234 5678 9010',
                'expiry': '01/20',  # Expired
                'cvv': '123'
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testing: {test['name']}")
        result = client.validate_card(test['data'])
        print(f"   Valid: {result.get('valid')}")
        print(f"   Details: {result.get('validations', {})}")


def example_transaction_history():
    """Example 3: Retrieve transaction history"""
    print("\n" + "="*60)
    print("Example 3: Transaction History")
    print("="*60)
    
    client = CardCaptureClient()
    
    print("\n📜 Retrieving transaction history...")
    result = client.get_transactions()
    
    if result.get('success'):
        print(f"Total transactions: {result.get('count')}")
        print("\nRecent transactions:")
        for tx in result.get('transactions', [])[:5]:
            print(f"  • {tx.get('timestamp')} - {tx.get('cardholder')} ({tx.get('card_type')})")
    else:
        print(f"Error: {result.get('error')}")


def example_batch_capture():
    """Example 4: Batch process multiple cards"""
    print("\n" + "="*60)
    print("Example 4: Batch Card Processing")
    print("="*60)
    
    client = CardCaptureClient()
    
    cards = [
        {
            'cardholder': 'JOHN DOE',
            'cardNumber': '4532123456789010',
            'expiry': '12/25',
            'cvv': '123',
            'email': 'john@example.com',
            'cardType': 'visa'
        },
        {
            'cardholder': 'JANE SMITH',
            'cardNumber': '5425233430109903',
            'expiry': '05/26',
            'cvv': '456',
            'email': 'jane@example.com',
            'cardType': 'mastercard'
        }
    ]
    
    results = []
    for i, card in enumerate(cards, 1):
        print(f"\n📊 Processing card {i}/{len(cards)}...")
        result = client.capture_card(card)
        results.append({
            'cardholder': card['cardholder'],
            'success': result.get('success'),
            'card_type': result.get('card_type'),
            'last_four': result.get('card_last_four')
        })
        print(f"   Status: {'✓ Success' if result.get('success') else '✗ Failed'}")
    
    print("\n📈 Batch Summary:")
    success_count = sum(1 for r in results if r['success'])
    print(f"  • Total: {len(results)}")
    print(f"  • Successful: {success_count}")
    print(f"  • Failed: {len(results) - success_count}")


def example_integration_with_camera():
    """
    Example 5: Integration with camera capture system
    Shows how to use card capture with existing camera capture
    """
    print("\n" + "="*60)
    print("Example 5: Camera + Card Capture Integration")
    print("="*60)
    
    # This would integrate with CameraCardCapture from existing project
    print("""
    Integration workflow:
    
    1. Capture card image using camera:
       card_capture = CardCameraCapture(output_dir='captured_cards')
       card_capture.initialize_camera()
       frame = card_capture.get_frame()
       image = card_capture.capture_card_image(frame)
    
    2. Extract card details using OCR (optional):
       card_details = extract_card_text(image)  # Using Tesseract/Keras-OCR
    
    3. Capture additional details via form:
       form_data = {
           'cardholder': 'JOHN DOE',
           'cardNumber': '4532123456789010',
           'expiry': '12/25',
           'cvv': '123'
       }
    
    4. Process using backend:
       client = CardCaptureClient()
       result = client.capture_card(form_data)
       
       if result['success']:
           # Store reference image + transaction ID
           store_transaction({
               'image': image,
               'transaction_id': result.get('id'),
               'card_last_four': result.get('card_last_four')
           })
    """)


def example_error_handling():
    """Example 6: Error handling and validation"""
    print("\n" + "="*60)
    print("Example 6: Error Handling")
    print("="*60)
    
    client = CardCaptureClient()
    
    invalid_cards = [
        {
            'name': 'Missing field',
            'data': {
                'cardholder': 'TEST',
                # Missing cardNumber
                'expiry': '12/25',
                'cvv': '123'
            }
        },
        {
            'name': 'Invalid CVV',
            'data': {
                'cardholder': 'TEST USER',
                'cardNumber': '4532123456789010',
                'expiry': '12/25',
                'cvv': '12'  # Too short
            }
        },
        {
            'name': 'Invalid name',
            'data': {
                'cardholder': 'X',  # Too short
                'cardNumber': '4532123456789010',
                'expiry': '12/25',
                'cvv': '123'
            }
        }
    ]
    
    for test in invalid_cards:
        print(f"\n❌ Test: {test['name']}")
        result = client.capture_card(test['data'])
        print(f"   Error: {result.get('error')}")
        print(f"   Code: {result.get('code')}")


def example_logging_to_file():
    """Example 7: Logging capture results"""
    print("\n" + "="*60)
    print("Example 7: Logging Results")
    print("="*60)
    
    client = CardCaptureClient()
    
    log_file = 'card_captures.log'
    
    card_data = {
        'cardholder': 'TEST USER',
        'cardNumber': '4532123456789010',
        'expiry': '12/25',
        'cvv': '123',
        'email': 'test@example.com',
        'cardType': 'visa'
    }
    
    result = client.capture_card(card_data)
    
    # Log the result
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'result': result,
        'cardholder': card_data.get('cardholder'),
        'card_type': result.get('card_type')
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"✓ Result logged to {log_file}")
    print(f"Entry: {json.dumps(log_entry, indent=2)}")


# ==================== Main ====================

if __name__ == '__main__':
    print("\n" + "█"*60)
    print("  Card Capture Integration Examples")
    print("█"*60)
    
    # Make sure backend is running
    client = CardCaptureClient()
    if not client.health_check():
        print("\n⚠️  Backend is not running!")
        print("\nStart the backend with:")
        print("  python card_capture_backend.py")
        print("\nThen run this script again.")
        exit(1)
    
    # Run examples
    try:
        example_basic_capture()
        example_validation()
        example_batch_capture()
        example_error_handling()
        example_integration_with_camera()
        example_logging_to_file()
        example_transaction_history()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "█"*60)
    print("  Examples completed!")
    print("█"*60 + "\n")
