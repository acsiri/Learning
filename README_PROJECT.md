# Card Camera Capture - Complete Project

Automatic detection and capture of credit/debit cards from camera feed using OpenCV and computer vision.

## Features

✅ **Real-time Card Detection** - Uses edge detection and contour analysis  
✅ **Multiple Camera Support** - System camera, USB cameras, mobile devices  
✅ **Automatic + Manual Capture** - Auto-capture on detection or manual SPACE key  
✅ **Motion Detection** - Auto-capture based on motion  
✅ **Batch Processing** - Capture multiple cards in sequence  
✅ **High Performance** - Optimized for real-time processing  

## Project Structure

```
card-camera-capture/
├── src/
│   ├── __init__.py
│   ├── camera_capture.py      # Main CardCameraCapture class
│   ├── card_detector.py       # Card detection logic
│   ├── simple_capture.py      # Simple capture functions
│   └── utils.py               # Utility functions
├── tests/
│   └── __init__.py
├── examples/
│   └── __init__.py
├── output/
│   └── captured_cards/        # Output directory
├── main.py                    # Main entry point
├── setup.py                   # Package setup
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .github/
    └── copilot-instructions.md
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install opencv-python imutils pillow
```

### 2. Verify Installation

```bash
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
```

## Quick Start

### Run Main Application
```bash
python main.py
```

**Controls:**
- SPACE: Manual capture
- Q/ESC: Exit

### Using as a Package

```python
from src import CardCameraCapture, find_available_cameras

# Find available cameras
cameras = find_available_cameras()
print(f"Available cameras: {cameras}")

# Create capture instance
capture = CardCameraCapture(camera_index=0)

# Run camera feed
capture.run_camera_feed()
```

## API Reference

### CardCameraCapture

Main class for capturing card images.

```python
from src import CardCameraCapture

capture = CardCameraCapture(
    output_dir="output/captured_cards",
    camera_index=0
)

# Run with auto-capture
capture.run_camera_feed(
    confidence_threshold=3,  # Frames to confirm detection
    save_every_n_frames=1    # Save frequency
)
```

### CardDetector

Card detection using computer vision.

```python
from src import CardDetector
import cv2

detector = CardDetector(
    min_area=10000,
    max_area=500000
)

frame = cv2.imread("image.jpg")
detected, contours = detector.detect(frame)
```

### Utility Functions

```python
from src import find_available_cameras
from src.utils import create_output_directory, generate_timestamp_filename

# Find cameras
cameras = find_available_cameras()

# Create directories
create_output_directory("my_cards")

# Generate filenames
filename = generate_timestamp_filename(prefix="card")
```

## Examples

### Example 1: Basic Usage
```python
from src import CardCameraCapture

capture = CardCameraCapture()
capture.run_camera_feed()
```

### Example 2: Batch Capture
```python
from src import CardCameraCapture

capture = CardCameraCapture(output_dir="batch_cards")
if capture.initialize_camera():
    for i in range(5):
        ret, frame = capture.cap.read()
        detected, _, contours = capture.detect_card(frame)
        if detected:
            capture.capture_card_image(frame, contours)
    capture.cleanup()
```

### Example 3: Process Existing Images
```python
import cv2
from src import CardDetector
import os

detector = CardDetector()

for filename in os.listdir("captured_cards"):
    frame = cv2.imread(f"captured_cards/{filename}")
    detected, contours = detector.detect(frame)
    print(f"{filename}: {'✓' if detected else '✗'}")
```

### Example 4: Different Cameras

**Camera Index:**
- 0: Default/Built-in camera
- 1+: External USB cameras

```python
from src import CardCameraCapture

# Use external camera
capture = CardCameraCapture(camera_index=1)
capture.run_camera_feed()
```

**Mobile Phone Camera:**

1. Install IP Webcam on Android
2. Start app and note IP:PORT
3. Use in code:

```python
import cv2
cap = cv2.VideoCapture("http://192.168.1.100:8080/video")
```

## Configuration

### Adjust Detection Sensitivity

```python
from src import CardCameraCapture

capture = CardCameraCapture()

# Smaller cards
capture.detector.min_area = 5000

# Larger cards only
capture.detector.max_area = 300000

# Stricter aspect ratio (more like actual credit cards)
capture.detector.min_aspect_ratio = 1.55
capture.detector.max_aspect_ratio = 1.65

capture.run_camera_feed()
```

### Camera Properties

```python
import cv2

cap = cv2.VideoCapture(0)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Set FPS
cap.set(cv2.CAP_PROP_FPS, 30)

# Adjust brightness
cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)

# Adjust contrast
cap.set(cv2.CAP_PROP_CONTRAST, 50)
```

## Troubleshooting

### Camera Not Detected

```python
from src import find_available_cameras

cameras = find_available_cameras()
print(f"Available: {cameras}")
```

### Cards Not Detected

1. **Improve lighting** - Ensure good illumination
2. **Adjust detection area**:
   ```python
   capture.detector.min_area = 5000  # Reduce from 10000
   ```
3. **Adjust Canny thresholds** in `card_detector.py`:
   ```python
   edges = cv2.Canny(blurred, 30, 100)  # Lower from 50, 150
   ```

### Blurry Images

1. Ensure steady camera position
2. Improve lighting
3. Reduce FPS: `cap.set(cv2.CAP_PROP_FPS, 15)`

### False Positives

1. Increase `confidence_threshold`:
   ```python
   capture.run_camera_feed(confidence_threshold=10)
   ```
2. Tighten aspect ratio checks

### Performance Issues

1. Reduce resolution:
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   ```
2. Increase frame skip:
   ```python
   capture.run_camera_feed(save_every_n_frames=3)
   ```

## Integration with Vision AI

### With CardVisionExtractor

```python
import os
from src import CardCameraCapture
from CardVisionExtractor import CardVisionExtractor

# Capture cards
capture = CardCameraCapture()
capture.run_camera_feed()

# Extract data
extractor = CardVisionExtractor()
for img in os.listdir("output/captured_cards"):
    data = extractor.extract_from_image(f"output/captured_cards/{img}")
    print(data)
```

## Performance Optimization

### Faster Processing
```python
capture.run_camera_feed(
    confidence_threshold=2,      # Lower
    save_every_n_frames=3        # Skip frames
)
```

### Lower Memory Usage
```python
import cv2
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

### GPU Acceleration
```bash
pip install opencv-contrib-python
```

## Output

**Default location:** `output/captured_cards/`

**Filename format:** `card_YYYYMMDD_HHMMSS_mmm.jpg`

**Example:**
- `card_20250504_143025_123.jpg`
- `card_20250504_143026_456.jpg`

## Requirements

- Python 3.7+
- OpenCV 4.8.0+
- NumPy
- imutils
- Pillow

## License

Use for personal and educational purposes.

## Support

- Check available cameras: `find_available_cameras()`
- Verify OpenCV: `cv2.__version__`
- Check camera permissions on your OS
- Enable USB debugging for Android devices
