# 💳 Secure Credit Card Capture System

Complete solution for capturing credit card information with security best practices, validation, and iframe integration.

## 📋 Overview

This system provides:
- **Secure card capture form** with real-time validation
- **Embeddable iframe** for web applications
- **Python Flask backend** for secure data handling
- **Client-side validation** using Luhn algorithm
- **PCI compliance** guidance and best practices

## 🎯 Key Features

### Frontend (HTML/JavaScript)
- ✅ Real-time card type detection (Visa, Mastercard, Amex, Discover)
- ✅ Automatic card number formatting
- ✅ Luhn algorithm validation
- ✅ Expiry date validation with future date checking
- ✅ CVV validation (3-4 digits)
- ✅ Email validation (optional)
- ✅ Cardholder name validation
- ✅ Paste prevention on sensitive fields
- ✅ Error handling and user feedback
- ✅ Responsive design (mobile-friendly)
- ✅ Loading states and success messages
- ✅ Accessibility features

### Backend (Python Flask)
- ✅ Comprehensive card validation
- ✅ Secure transaction logging (masked data)
- ✅ CORS support
- ✅ Input sanitization
- ✅ Error handling with specific error codes
- ✅ Health check endpoints
- ✅ Transaction history (masked)
- ✅ Rate limiting ready

## 📁 Files

```
card_capture_form.html              # Main card capture form
card_capture_iframe_example.html    # Integration guide with live demo
card_capture_backend.py             # Flask backend server
CARD_CAPTURE_README.md              # This file
```

## 🚀 Quick Start

### 1. Run the Backend Server

```bash
# Install dependencies
pip install flask flask-cors

# Run the server
python card_capture_backend.py
```

Server will be available at `http://localhost:5000`

### 2. Open the Integration Guide

Open `card_capture_iframe_example.html` in your browser to see:
- Live form demonstration
- Integration methods
- Code examples for different backends
- Security best practices

### 3. Test the Form

Fill out the form with test card details:

**Test Cards:**
- Visa: `4532 1234 5678 9010`
- Mastercard: `5425 2334 3010 9903`
- Amex: `374245455400126`
- Discover: `6011 1111 1111 1117`

Expiry: Any future date (e.g., 12/25)
CVV: 3 digits (e.g., 123)

## 🔌 Integration Methods

### Method 1: Standalone Page

Direct users to the form:
```html
<a href="card_capture_form.html" target="_blank">Enter Card Details</a>
```

### Method 2: Iframe Embed

Embed in your application:
```html
<iframe 
    src="card_capture_form.html" 
    width="500" 
    height="700"
    sandbox="allow-same-origin allow-scripts allow-forms"
    style="border: none; border-radius: 8px;">
</iframe>
```

### Method 3: Modal Popup

```html
<!-- Button to open modal -->
<button onclick="openCardModal()">Add Card</button>

<!-- Modal -->
<div id="cardModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
    <div style="background: white; margin: 50px auto; width: 500px; border-radius: 8px; overflow: hidden;">
        <iframe 
            src="card_capture_form.html" 
            width="100%" 
            height="700"
            style="border: none;">
        </iframe>
    </div>
</div>

<script>
function openCardModal() {
    document.getElementById('cardModal').style.display = 'block';
}

function closeCardModal() {
    document.getElementById('cardModal').style.display = 'none';
}
</script>
```

### Method 4: React Component

```jsx
import React, { useRef } from 'react';

export function CardCapture() {
    const iframeRef = useRef(null);

    const handleCapture = () => {
        // Listen for messages from iframe
        window.addEventListener('message', (e) => {
            if (e.data.type === 'cardData') {
                console.log('Card data received:', e.data.payload);
                // Send to backend
                fetch('/api/capture-card', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(e.data.payload)
                });
            }
        });
    };

    return (
        <iframe
            ref={iframeRef}
            src="card_capture_form.html"
            width="500"
            height="700"
            style={{ border: 'none', borderRadius: '8px' }}
            sandbox="allow-same-origin allow-scripts allow-forms"
            onLoad={handleCapture}
        />
    );
}
```

### Method 5: Vue.js Component

```vue
<template>
    <div class="card-capture">
        <iframe
            ref="cardFrame"
            src="card_capture_form.html"
            width="500"
            height="700"
            style="border: none; border-radius: 8px"
            sandbox="allow-same-origin allow-scripts allow-forms"
            @load="initMessageListener"
        />
    </div>
</template>

<script>
export default {
    methods: {
        initMessageListener() {
            window.addEventListener('message', (event) => {
                if (event.data.type === 'cardData') {
                    this.$emit('card-captured', event.data.payload);
                }
            });
        }
    }
}
</script>
```

## 🐍 Backend Integration

### Flask Endpoint

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/capture-card', methods=['POST'])
def capture_card():
    data = request.json
    
    # Validate data (done on backend too)
    required_fields = ['cardholder', 'cardNumber', 'expiry', 'cvv']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # TODO: Send to payment processor
    # IMPORTANT: Never store raw card data
    
    # Example: Stripe integration
    # import stripe
    # stripe.Charge.create(
    #     amount=1000,
    #     currency='usd',
    #     source=data['cardNumber'],
    # )
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
```

### Node.js/Express Endpoint

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.post('/api/capture-card', (req, res) => {
    const { cardholder, cardNumber, expiry, cvv } = req.body;
    
    // Validate
    if (!cardholder || !cardNumber || !expiry || !cvv) {
        return res.status(400).json({ error: 'Missing fields' });
    }
    
    // TODO: Send to payment processor (Stripe, etc.)
    
    res.json({ success: true });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

### .NET/C# Endpoint

```csharp
[ApiController]
[Route("api")]
public class PaymentController : ControllerBase
{
    [HttpPost("capture-card")]
    public IActionResult CaptureCard([FromBody] CardData data)
    {
        // Validate
        if (string.IsNullOrEmpty(data.Cardholder) || string.IsNullOrEmpty(data.CardNumber))
        {
            return BadRequest(new { error = "Missing required fields" });
        }
        
        // TODO: Send to payment processor
        
        return Ok(new { success = true });
    }
}

public class CardData
{
    public string Cardholder { get; set; }
    public string CardNumber { get; set; }
    public string Expiry { get; set; }
    public string CVV { get; set; }
    public string Email { get; set; }
}
```

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Always use HTTPS in production
- ✅ Use PCI-compliant payment processors (Stripe, PayPal, etc.)
- ✅ Validate input on both client AND server
- ✅ Never log or store full card numbers
- ✅ Use secure headers (CSP, X-Frame-Options)
- ✅ Implement rate limiting
- ✅ Use strong SSL/TLS certificates
- ✅ Encrypt sensitive data in transit
- ✅ Regular security audits
- ✅ Keep dependencies updated

### ❌ DON'T:
- ❌ Store raw credit card data in your database
- ❌ Send card data over HTTP (unencrypted)
- ❌ Log full card numbers
- ❌ Handle card data directly without PCI compliance
- ❌ Disable CORS security unnecessarily
- ❌ Trust only client-side validation
- ❌ Use outdated encryption methods
- ❌ Store CVV (it's illegal)
- ❌ Bypass security checks for "convenience"

## 🛡️ PCI DSS Compliance

### Key Requirements:
1. **Requirement 1:** Firewall configuration
2. **Requirement 2:** Do not use vendor defaults
3. **Requirement 3:** Protect stored cardholder data
4. **Requirement 4:** Encrypt transmission of cardholder data
5. **Requirement 5:** Protect against malware
6. **Requirement 6:** Maintain secure systems
7. **Requirement 7:** Limit access to cardholder data
8. **Requirement 8:** Identify and authenticate access
9. **Requirement 9:** Restrict physical access
10. **Requirement 10:** Track and monitor network access
11. **Requirement 11:** Test security systems
12. **Requirement 12:** Maintain security policy

### Recommended Approach:
Use **tokenization** with payment processors:

```python
# Example with Stripe
import stripe

stripe.api_key = "sk_live_your_key"

# Get token from frontend
token = request.json['stripeToken']

# Create charge using token (not raw card data)
charge = stripe.Charge.create(
    amount=1000,
    currency="usd",
    source=token,
    description="Payment from web app"
)
```

## 📊 API Endpoints

### POST /api/capture-card
Capture and validate card details

**Request:**
```json
{
    "cardholder": "John Doe",
    "cardNumber": "4532123456789010",
    "expiry": "12/25",
    "cvv": "123",
    "email": "john@example.com",
    "cardType": "visa",
    "timestamp": "2025-05-07T10:30:00Z"
}
```

**Response (Success):**
```json
{
    "success": true,
    "message": "Card details captured and validated successfully",
    "code": "CARD_CAPTURED",
    "card_last_four": "9010",
    "card_type": "visa",
    "timestamp": "2025-05-07T10:30:00Z"
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "Invalid card number (failed Luhn check)",
    "code": "VALIDATION_ERROR"
}
```

### POST /api/validate-card
Validate card details without capturing

**Request:**
```json
{
    "cardholder": "John Doe",
    "cardNumber": "4532123456789010",
    "expiry": "12/25",
    "cvv": "123"
}
```

**Response:**
```json
{
    "valid": true,
    "validations": {
        "cardholder": true,
        "cardNumber": true,
        "expiry": true,
        "cvv": true
    }
}
```

### GET /api/health
Health check endpoint

**Response:**
```json
{
    "status": "healthy"
}
```

### GET /api/transactions
Get recent transactions (requires authentication)

**Response:**
```json
{
    "success": true,
    "count": 5,
    "transactions": [
        {
            "timestamp": "2025-05-07T10:30:00",
            "cardholder": "John Doe",
            "card_last_four": "9010",
            "card_type": "visa",
            "email": "john@example.com"
        }
    ]
}
```

## 🧪 Testing

### Test Card Numbers

| Card Type      | Number               | Expiry | CVV |
|----------------|----------------------|--------|-----|
| Visa           | 4532 1234 5678 9010 | 12/25  | 123 |
| Mastercard     | 5425 2334 3010 9903 | 12/25  | 123 |
| American Express| 3742 454554 00126   | 12/25  | 1234|
| Discover       | 6011 1111 1111 1117 | 12/25  | 123 |

### Unit Tests

```python
import unittest
from card_capture_backend import CardValidator

class TestCardValidation(unittest.TestCase):
    def test_luhn_validation(self):
        # Valid
        self.assertTrue(CardValidator.validate_card_number('4532 1234 5678 9010'))
        # Invalid
        self.assertFalse(CardValidator.validate_card_number('1234 5678 9012 3456'))
    
    def test_expiry_validation(self):
        self.assertTrue(CardValidator.validate_expiry('12', '25'))
        self.assertFalse(CardValidator.validate_expiry('13', '25'))
    
    def test_cvv_validation(self):
        self.assertTrue(CardValidator.validate_cvv('123'))
        self.assertFalse(CardValidator.validate_cvv('12'))

if __name__ == '__main__':
    unittest.main()
```

## 📱 Mobile Support

The form is fully responsive:
- Desktop: 500px width
- Tablet: Adapts to screen size
- Mobile: Full width with optimized touch controls

## 🌐 Internationalization

To add support for multiple languages:

```javascript
// translations.js
const translations = {
    en: {
        cardholderName: 'Cardholder Name',
        cardNumber: 'Card Number',
        expiryDate: 'Expiry Date',
        cvv: 'CVV'
    },
    es: {
        cardholderName: 'Nombre del Titular',
        cardNumber: 'Número de Tarjeta',
        expiryDate: 'Fecha de Vencimiento',
        cvv: 'CVV'
    }
};

// Usage
const lang = 'es';
const label = translations[lang].cardholderName;
```

## 🐛 Troubleshooting

### Form not loading in iframe
- Check CORS headers
- Verify sandbox attributes
- Check browser console for errors

### Card validation failing
- Use valid test card numbers
- Ensure Luhn algorithm check passes
- Check expiry date is in future

### Backend not receiving data
- Verify CORS is enabled
- Check Content-Type header
- Ensure /api/capture-card endpoint exists

### Password managers interfering
- Some password managers may auto-fill card fields
- Disable autocomplete for sensitive fields
- Add specific autocomplete="cc-number" etc.

## 📚 References

- [PCI DSS Standard](https://www.pcisecuritystandards.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Stripe Documentation](https://stripe.com/docs)
- [PayPal Integration](https://developer.paypal.com/)
- [Luhn Algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm)

## 📝 License

This code is provided as-is for educational and integration purposes. Always follow PCI compliance requirements and use certified payment processors.

## ⚠️ Disclaimer

This implementation is for demonstration purposes. For production use:
1. Use established payment processors (Stripe, Square, PayPal)
2. Implement full PCI DSS compliance
3. Conduct security audits
4. Use HTTPS everywhere
5. Never store raw card data

## 🤝 Support

For questions or issues:
1. Check the integration guide (card_capture_iframe_example.html)
2. Review backend documentation (card_capture_backend.py)
3. Test with provided test card numbers
4. Check browser console for errors
5. Verify backend server is running

---

**Last Updated:** May 7, 2025
**Version:** 1.0.0
