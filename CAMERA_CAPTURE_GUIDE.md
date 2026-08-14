# Card Camera Capture - Complete Guide

## Overview
Automatically detect and capture images of credit/debit cards from your camera feed. Works with system cameras, laptop webcams, and mobile phones connected via USB.

## Features
✓ Real-time card detection using computer vision
✓ Automatic image capture when card is detected
✓ Manual capture option (press SPACE)
✓ Multiple camera support (USB, built-in, mobile)
✓ Timestamp-based file naming
✓ High-quality image extraction

---

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

If you only want the card capture without other dependencies:
```bash
pip install opencv-python imutils pillow
```

### 2. Verify OpenCV Installation
```bash
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
```

---

## Quick Start

### Option 1: Advanced Version (Recommended)
Full-featured with confidence threshold and manual controls:

```bash
python CameraCardCapture.py
```

**Controls:**
- SPACE: Manual capture
- ESC/Q: Exit
- Automatically saves detected cards to `captured_cards/` folder

**Features:**
- Smart card detection with aspect ratio matching
- Confidence threshold to reduce false positives
- Larger detected card is extracted and saved
- Real-time status display

### Option 2: Simple Version
Quick setup for basic usage:

```bash
python SimpleCardCapture.py
```

**Modes:**
1. Manual capture (press SPACE when card is detected)
2. Auto-capture (automatically captures on motion)

---

## Using Different Cameras

### 1. Built-in/System Camera (Default)
```python
from CameraCardCapture import CardCameraCapture

capture = CardCameraCapture(camera_index=0)  # 0 = default camera
capture.run_camera_feed()
```

### 2. External USB Camera
```python
from CameraCardCapture import CardCameraCapture

capture = CardCameraCapture(camera_index=1)  # 1 = first external camera
capture.run_camera_feed()
```

### 3. Mobile Phone Camera (Android)

#### Setup:
1. **Install IP Webcam on Android**: https://play.google.com/store/apps/details?id=com.pas.webcam
2. **Start the app** and note the IP address/port
3. **Run Python script**:

```python
import cv2
from CameraCardCapture import CardCameraCapture

# Replace with your phone's IP:PORT
PHONE_URL = "http://192.168.1.100:8080/video"
cap = cv2.VideoCapture(PHONE_URL)

# Then use CameraCardCapture class
capture = CardCameraCapture(camera_index=PHONE_URL, output_dir="mobile_cards")
```

#### Alternative - Using adb (USB Connection):
```bash
# Connect phone via USB with USB debugging enabled
adb forward tcp:5555 tcp:5555
# Then in Python:
cap = cv2.VideoCapture("http://127.0.0.1:5555/video")
```

### 4. Multiple Cameras Simultaneously
```python
import cv2
from CameraCardCapture import CardCameraCapture

# Find available cameras
from CameraCardCapture import find_available_cameras
cameras = find_available_cameras()
print(f"Available cameras: {cameras}")

# Run on each camera
for cam_idx in cameras:
    capture = CardCameraCapture(camera_index=cam_idx, 
                               output_dir=f"cards_camera_{cam_idx}")
    # capture.run_camera_feed()
```

---

## API Usage Examples

### Example 1: Basic Usage
```python
from CameraCardCapture import CardCameraCapture

capture = CardCameraCapture(output_dir="my_cards")
capture.run_camera_feed(confidence_threshold=3)
```

### Example 2: Custom Detection Parameters
```python
from CameraCardCapture import CardCameraCapture

capture = CardCameraCapture(output_dir="cards", camera_index=0)
capture.min_area = 5000      # Minimum card size
capture.max_area = 600000    # Maximum card size
capture.run_camera_feed(confidence_threshold=2, save_every_n_frames=1)
```

### Example 3: Manual Frame Processing
```python
import cv2
from CameraCardCapture import CardCameraCapture

capture = CardCameraCapture()
capture.initialize_camera()

# Read and process single frames
ret, frame = capture.cap.read()
if ret:
    detected, _, contours = capture.detect_card(frame)
    if detected:
        capture.capture_card_image(frame, contours)

capture.cleanup()
```

### Example 4: Batch Processing
```python
import cv2
import os
from CameraCardCapture import CardCameraCapture

capture = CardCameraCapture(output_dir="batch_cards")
capture.initialize_camera()

for i in range(10):  # Capture 10 frames
    ret, frame = capture.cap.read()
    detected, _, contours = capture.detect_card(frame)
    
    if detected:
        capture.capture_card_image(frame, contours)

capture.cleanup()
```

---

## Advanced Configuration

### Tuning Detection Sensitivity

**Adjust card detection area (in pixels):**
```python
capture.min_area = 5000      # Increase to ignore small objects
capture.max_area = 600000    # Decrease to ignore large objects
```

**Adjust confidence threshold:**
- Lower = faster capture, more false positives
- Higher = slower capture, more accurate
```python
capture.run_camera_feed(confidence_threshold=5)  # More confident
```

**Adjust edge detection:**
Edit the `detect_card()` method:
```python
edges = cv2.Canny(blurred, 30, 100)  # (lower, upper threshold)
```

### Custom Output Format
```python
import cv2
from datetime import datetime

capture = CardCameraCapture()
capture.initialize_camera()

ret, frame = capture.cap.read()
detected, _, contours = capture.detect_card(frame)

if detected:
    x, y, w, h = cv2.boundingRect(contours[0])
    card_image = frame[y:y+h, x:x+w]
    
    # Custom naming and processing
    custom_name = f"card_high_quality_{datetime.now().isoformat()}.jpg"
    cv2.imwrite(custom_name, card_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
```

---

## Troubleshooting

### Problem: Camera not detected
```python
from CameraCardCapture import find_available_cameras

cameras = find_available_cameras()
print(f"Available cameras: {cameras}")
# Use camera_index from the list
```

### Problem: Cards not detected
1. Ensure good lighting
2. Reduce `min_area` or increase `max_area`
3. Adjust `cv2.Canny()` thresholds in `detect_card()`
4. Make sure card fills 30-70% of frame

### Problem: Many false positives
1. Increase `confidence_threshold`
2. Increase `min_area` to ignore small objects
3. Tighten aspect ratio checks (1.3 to 1.8)

### Problem: Blurry images
1. Ensure good lighting
2. Hold card steady
3. Reduce camera speed: `cap.set(cv2.CAP_PROP_FPS, 15)`

### Problem: USB Camera not working on Windows
```bash
# Update camera drivers
# Or use DirectShow:
import cv2
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

---

## Performance Optimization

### Faster Processing
```python
capture.run_camera_feed(
    confidence_threshold=2,      # Lower threshold
    save_every_n_frames=3        # Skip some frames
)
```

### Reduce Memory Usage
```python
import cv2
capture.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

### GPU Acceleration (CUDA)
```bash
pip install opencv-contrib-python
```
Then in code:
```python
cv2.cuda.getCudaEnabledDeviceCount()
```

---

## Integration with Existing Vision AI

### With CardVisionExtractor
```python
from SimpleCardCapture import simple_card_capture
from CardVisionExtractor import CardVisionExtractor

# Capture card
simple_card_capture(output_dir="temp_cards")

# Then extract data
extractor = CardVisionExtractor()
extractor.extract_from_image("temp_cards/card_*.jpg")
```

### Complete Pipeline
```python
import os
from CameraCardCapture import CardCameraCapture
from CardVisionExtractor import CardVisionExtractor

# 1. Capture
capture = CardCameraCapture(output_dir="captured_cards")
capture.run_camera_feed()

# 2. Extract
extractor = CardVisionExtractor()
for img_file in os.listdir("captured_cards"):
    data = extractor.extract_from_image(os.path.join("captured_cards", img_file))
    print(data)
```

---

## File Outputs

**Default location:** `captured_cards/` folder

**Filename format:** `card_YYYYMMDD_HHMMSS_mmm.jpg`

**Example:**
- `card_20250504_143025_123.jpg`
- `card_20250504_143026_456.jpg`

---

## Requirements
- Python 3.7+
- OpenCV 4.8.0+
- NumPy
- imutils
- Pillow

---

## License
Use for personal and educational purposes.

## Support
For issues or questions, check:
1. Camera availability: `find_available_cameras()`
2. OpenCV version: `cv2.__version__`
3. Camera permissions on your OS
