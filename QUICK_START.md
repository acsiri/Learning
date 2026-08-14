# Card Capture System - Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install flask flask-cors
```

### Step 2: Run the Backend Server
```bash
python card_capture_backend.py
```

You should see:
```
============================================================
🛡️  Card Capture Backend Server
============================================================
⚠️  WARNING: This is for development/testing only!
   Never store raw credit card data in production.
   Use PCI-compliant payment processors like Stripe or PayPal.
============================================================

 * Running on http://0.0.0.0:5000
```

### Step 3: Open the Form

#### Option A: Standalone Form
Open `card_capture_form.html` in your browser

#### Option B: Integration Guide with Live Demo
Open `card_capture_iframe_example.html` to see:
- Live embedded form
- Integration examples
- Code snippets
- Security best practices

### Step 4: Test with Sample Card

**Test Card:**
- Number: `4532 1234 5678 9010`
- Expiry: `12/25`
- CVV: `123`
- Name: `JOHN DOE`

## 📋 File Structure

```
📁 Card Capture System
├── card_capture_form.html              # Standalone form
├── card_capture_iframe_example.html    # Integration guide
├── card_capture_backend.py             # Flask backend
├── CARD_CAPTURE_README.md              # Full documentation
└── QUICK_START.md                      # This file
```

## 🔗 Integration Methods

### Quick Integration (Copy & Paste)

#### HTML/CSS/JavaScript
```html
<iframe 
    src="card_capture_form.html" 
    width="500" 
    height="700"
    sandbox="allow-same-origin allow-scripts allow-forms"
    style="border: none; border-radius: 8px;">
</iframe>
```

#### React
```jsx
<iframe
    src="card_capture_form.html"
    width="500"
    height="700"
    sandbox="allow-same-origin allow-scripts allow-forms"
/>
```

#### Vue.js
```vue
<iframe
    src="card_capture_form.html"
    width="500"
    height="700"
    sandbox="allow-same-origin allow-scripts allow-forms"
/>
```

## 📊 API Endpoints

### Capture Card
```
POST /api/capture-card
Content-Type: application/json

{
    "cardholder": "John Doe",
    "cardNumber": "4532123456789010",
    "expiry": "12/25",
    "cvv": "123",
    "email": "john@example.com"
}

Response:
{
    "success": true,
    "card_last_four": "9010",
    "card_type": "visa"
}
```

### Validate Card (without capturing)
```
POST /api/validate-card
Content-Type: application/json

{
    "cardholder": "John Doe",
    "cardNumber": "4532123456789010",
    "expiry": "12/25",
    "cvv": "123"
}

Response:
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

### Health Check
```
GET /api/health

Response:
{
    "status": "healthy"
}
```

## 🧪 Test Cards

| Type          | Number                | Expiry | CVV  |
|---------------|----------------------|--------|------|
| **Visa**      | 4532 1234 5678 9010 | 12/25  | 123  |
| **Mastercard**| 5425 2334 3010 9903 | 12/25  | 123  |
| **Amex**      | 3742 454554 00126   | 12/25  | 1234 |
| **Discover**  | 6011 1111 1111 1117 | 12/25  | 123  |

## 🔐 Security Checklist

- ✅ Form validates on client-side (Luhn algorithm)
- ✅ Backend validates all inputs
- ✅ HTTPS recommended for production
- ✅ CVV is NOT stored
- ✅ Card numbers are masked in logs
- ✅ CORS headers configured
- ✅ Input sanitization enabled
- ✅ Rate limiting ready to implement

## 🛠️ Customization

### Change Backend Port
```bash
# Edit card_capture_backend.py, line ~380:
app.run(host='0.0.0.0', port=3000)  # Change 5000 to desired port
```

### Change Form Colors
Edit `card_capture_form.html`, search for:
```css
/* Change these hex colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
background-color: #667eea;
```

### Add Custom Fields
Edit `card_capture_form.html`, add fields before the submit button:
```html
<div class="form-group">
    <label for="phone">Phone Number</label>
    <input type="tel" id="phone" name="phone" placeholder="(555) 123-4567">
</div>
```

## 📚 Full Documentation

For complete details, see `CARD_CAPTURE_README.md`

## ⚠️ Important Notes

### Production Deployment

⚠️ **CRITICAL:** Never store raw credit card data in your database!

**Recommended approach:**
1. Use **Stripe** (recommended)
   ```python
   import stripe
   stripe.Charge.create(amount=1000, source=token)
   ```

2. Use **PayPal**
   ```python
   # PayPal SDK integration
   ```

3. Use **Square**
   ```python
   # Square SDK integration
   ```

### HTTPS Configuration
```nginx
# nginx example
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

## 🐛 Troubleshooting

### Form not loading
- Check if `card_capture_form.html` exists in same directory
- Clear browser cache (Ctrl+Shift+Del)
- Open browser console (F12) for errors

### Backend not responding
- Verify Flask is running: `python card_capture_backend.py`
- Check port 5000 is not in use: `netstat -ano | grep 5000`
- Try different port if needed

### Card validation failing
- Use valid test card from table above
- Ensure no extra spaces in card number
- Check expiry date is in future (MM/YY format)

## 🌐 Localhost Testing

### Test URLs
- Form: `http://localhost:8000/card_capture_form.html`
- Integration Guide: `http://localhost:8000/card_capture_iframe_example.html`
- API: `http://localhost:5000/api/capture-card`

### Start Local Web Server (Python)
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

## 📞 Support Resources

- **PCI DSS**: https://www.pcisecuritystandards.org/
- **Stripe**: https://stripe.com/docs
- **PayPal**: https://developer.paypal.com/
- **OWASP**: https://owasp.org/

## ✨ Next Steps

1. **Test locally** - Use test cards above
2. **Review security** - Read CARD_CAPTURE_README.md
3. **Integrate payment processor** - Add Stripe, PayPal, etc.
4. **Deploy to production** - Use HTTPS and secure hosting
5. **Monitor transactions** - Set up logging and alerts

---

**Version:** 1.0.0  
**Last Updated:** May 7, 2025
