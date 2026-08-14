"""
Credit Card Capture Backend - Flask Application
Handles secure submission of credit card data with validation
DO NOT store raw card data - this is for demonstration only
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re
import json
import os
from typing import Dict, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB max request size


class CardValidator:
    """Validates credit card information"""
    
    @staticmethod
    def validate_luhn(card_number: str) -> bool:
        """
        Validate credit card number using Luhn algorithm
        
        Args:
            card_number: Card number without spaces/dashes
            
        Returns:
            True if valid, False otherwise
        """
        if not card_number.isdigit():
            return False
        
        total = 0
        reverse_digits = card_number[::-1]
        
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        return total % 10 == 0
    
    @staticmethod
    def validate_card_number(card_number: str) -> bool:
        """
        Validate card number format and Luhn check
        
        Args:
            card_number: Card number (may contain spaces)
            
        Returns:
            True if valid, False otherwise
        """
        cleaned = card_number.replace(' ', '').replace('-', '')
        
        if not cleaned.isdigit():
            return False
        
        # Check length (13-16 digits for most cards)
        if len(cleaned) < 13 or len(cleaned) > 16:
            return False
        
        # Verify Luhn algorithm
        return CardValidator.validate_luhn(cleaned)
    
    @staticmethod
    def validate_expiry(month: str, year: str) -> bool:
        """
        Validate expiry date
        
        Args:
            month: Month (MM format)
            year: Year (YY format)
            
        Returns:
            True if valid and not expired, False otherwise
        """
        try:
            month_int = int(month)
            year_int = int(year)
            
            if month_int < 1 or month_int > 12:
                return False
            
            if year_int < 24:  # Current year is 24+
                return False
            
            # Check if expiry date is in the future
            now = datetime.now()
            current_year = now.year % 100
            current_month = now.month
            
            if year_int < current_year:
                return False
            
            if year_int == current_year and month_int < current_month:
                return False
            
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_cvv(cvv: str) -> bool:
        """
        Validate CVV format (3 or 4 digits)
        
        Args:
            cvv: CVV code
            
        Returns:
            True if valid, False otherwise
        """
        if not cvv.isdigit():
            return False
        
        return len(cvv) in [3, 4]
    
    @staticmethod
    def validate_cardholder_name(name: str) -> bool:
        """
        Validate cardholder name
        
        Args:
            name: Cardholder name
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(name, str):
            return False
        
        name = name.strip()
        
        # Must have at least first and last name (3+ chars total)
        if len(name) < 3:
            return False
        
        # Only letters and spaces
        if not re.match(r'^[A-Za-z\s]+$', name):
            return False
        
        return True
    
    @staticmethod
    def validate_email(email: str) -> Optional[bool]:
        """
        Validate email format (optional field)
        
        Args:
            email: Email address
            
        Returns:
            True if valid, False if invalid, None if empty (valid)
        """
        if not email or email.strip() == '':
            return None  # Optional field
        
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(email_pattern, email.strip()))


class CardCaptureHandler:
    """Handles card capture requests"""
    
    def __init__(self):
        self.cards_log = 'card_transactions.log'
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup secure logging for transactions"""
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.cards_log = os.path.join(log_dir, 'card_transactions.log')
    
    def _mask_card_number(self, card_number: str) -> str:
        """
        Mask card number for logging (show last 4 digits only)
        
        Args:
            card_number: Full card number
            
        Returns:
            Masked card number (****-****-****-1234)
        """
        cleaned = card_number.replace(' ', '').replace('-', '')
        return f"****-****-****-{cleaned[-4:]}"
    
    def _log_transaction(self, card_data: Dict) -> None:
        """
        Log transaction for audit trail (without sensitive data)
        
        Args:
            card_data: Card data from request
        """
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'cardholder': card_data.get('cardholder'),
                'card_last_four': card_data.get('cardNumber')[-4:] if card_data.get('cardNumber') else 'N/A',
                'card_type': card_data.get('cardType'),
                'expiry': card_data.get('expiry'),
                'email': card_data.get('email'),
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', 'N/A')
            }
            
            with open(self.cards_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            logger.info(f"Transaction logged for {self._mask_card_number(card_data.get('cardNumber', ''))}")
        except Exception as e:
            logger.error(f"Error logging transaction: {e}")
    
    def validate_request(self, data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate card capture request
        
        Args:
            data: Request data
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ['cardholder', 'cardNumber', 'expiry', 'cvv']
        
        # Check for required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        
        # Validate cardholder name
        if not CardValidator.validate_cardholder_name(data['cardholder']):
            return False, "Invalid cardholder name"
        
        # Validate card number
        if not CardValidator.validate_card_number(data['cardNumber']):
            return False, "Invalid card number (failed Luhn check)"
        
        # Validate expiry
        expiry_parts = data['expiry'].split('/')
        if len(expiry_parts) != 2:
            return False, "Invalid expiry format (use MM/YY)"
        
        if not CardValidator.validate_expiry(expiry_parts[0], expiry_parts[1]):
            return False, "Invalid or expired card"
        
        # Validate CVV
        if not CardValidator.validate_cvv(data['cvv']):
            return False, "Invalid CVV"
        
        # Validate email if provided
        if 'email' in data and data['email']:
            email_valid = CardValidator.validate_email(data['email'])
            if email_valid is False:
                return False, "Invalid email address"
        
        return True, None
    
    def process_card(self, data: Dict) -> Tuple[Dict, int]:
        """
        Process credit card capture request
        
        Args:
            data: Card data from request
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        # Validate request
        is_valid, error_msg = self.validate_request(data)
        
        if not is_valid:
            logger.warning(f"Invalid card submission: {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'code': 'VALIDATION_ERROR'
            }, 400
        
        try:
            # Log transaction (without storing sensitive data)
            self._log_transaction(data)
            
            # TODO: Send to actual payment processor here
            # Examples:
            # - stripe.Charge.create(...)
            # - paypal_client.execute(payment)
            # - authorize_net_transaction(...)
            
            logger.info(f"Card processed successfully for {data['cardholder']}")
            
            response = {
                'success': True,
                'message': 'Card details captured and validated successfully',
                'code': 'CARD_CAPTURED',
                'card_last_four': data['cardNumber'].replace(' ', '')[-4:],
                'card_type': data.get('cardType'),
                'timestamp': datetime.now().isoformat()
            }
            
            return response, 200
            
        except Exception as e:
            logger.error(f"Error processing card: {e}")
            return {
                'success': False,
                'error': 'Internal server error',
                'code': 'SERVER_ERROR'
            }, 500


# Initialize handler
card_handler = CardCaptureHandler()


# ==================== Routes ====================

@app.route('/', methods=['GET'])
def index():
    """Health check and welcome endpoint"""
    return jsonify({
        'service': 'Card Capture Backend',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/capture-card', methods=['POST', 'OPTIONS'])
def capture_card():
    """
    Capture and process credit card details
    
    Expected JSON payload:
    {
        "cardholder": "John Doe",
        "cardNumber": "1234 5678 9012 3456",
        "expiry": "12/25",
        "cvv": "123",
        "email": "john@example.com",
        "cardType": "visa",
        "timestamp": "2025-05-07T10:30:00"
    }
    
    Returns:
    {
        "success": true/false,
        "message": "...",
        "code": "CARD_CAPTURED|VALIDATION_ERROR|SERVER_ERROR",
        "card_last_four": "3456",
        "card_type": "visa",
        "timestamp": "2025-05-07T10:30:00"
    }
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    # Validate content type
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json',
            'code': 'INVALID_CONTENT_TYPE'
        }), 400
    
    try:
        data = request.get_json()
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return jsonify({
            'success': False,
            'error': 'Invalid JSON format',
            'code': 'INVALID_JSON'
        }), 400
    
    # Process card
    response, status_code = card_handler.process_card(data)
    
    return jsonify(response), status_code


@app.route('/api/validate-card', methods=['POST'])
def validate_card():
    """
    Validate card details without capturing
    Useful for real-time validation on the frontend
    """
    if not request.is_json:
        return jsonify({'error': 'Invalid content type'}), 400
    
    data = request.get_json()
    
    validation_result = {
        'cardholder': CardValidator.validate_cardholder_name(data.get('cardholder', '')),
        'cardNumber': CardValidator.validate_card_number(data.get('cardNumber', '')),
        'cvv': CardValidator.validate_cvv(data.get('cvv', '')),
    }
    
    # Validate expiry
    if data.get('expiry'):
        parts = data['expiry'].split('/')
        if len(parts) == 2:
            validation_result['expiry'] = CardValidator.validate_expiry(parts[0], parts[1])
        else:
            validation_result['expiry'] = False
    
    # Validate email if provided
    if data.get('email'):
        email_valid = CardValidator.validate_email(data.get('email'))
        validation_result['email'] = email_valid if email_valid is not None else True
    
    is_all_valid = all(validation_result.values())
    
    return jsonify({
        'valid': is_all_valid,
        'validations': validation_result
    }), 200


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """
    Get recent transactions (masked for security)
    In production, add authentication and proper access control
    """
    try:
        transactions = []
        if os.path.exists(card_handler.cards_log):
            with open(card_handler.cards_log, 'r') as f:
                for line in f.readlines()[-20:]:  # Last 20 transactions
                    transactions.append(json.loads(line))
        
        return jsonify({
            'success': True,
            'count': len(transactions),
            'transactions': transactions
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving transactions: {e}")
        return jsonify({'error': 'Failed to retrieve transactions'}), 500


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'code': 'NOT_FOUND'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'code': 'METHOD_NOT_ALLOWED'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'code': 'SERVER_ERROR'
    }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🛡️  Card Capture Backend Server")
    print("="*60)
    print("⚠️  WARNING: This is for development/testing only!")
    print("   Never store raw credit card data in production.")
    print("   Use PCI-compliant payment processors like Stripe or PayPal.")
    print("="*60 + "\n")
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
