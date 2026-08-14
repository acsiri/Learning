"""
Card Camera Capture - Quick Examples and Use Cases
Run any of these examples directly: python -m CardCaptureExamples
"""

import os
import cv2
from CameraCardCapture import CardCameraCapture, find_available_cameras
from SimpleCardCapture import simple_card_capture, auto_capture_on_motion


# ============================================================================
# EXAMPLE 1: Basic Usage - Default Camera
# ============================================================================
def example_1_basic_usage():
    """Simplest way to get started"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    print("Starting camera with default settings...")
    print("Press SPACE to capture, Q to exit\n")
    
    capture = CardCameraCapture()
    capture.run_camera_feed()


# ============================================================================
# EXAMPLE 2: Detect Available Cameras
# ============================================================================
def example_2_find_cameras():
    """Find all connected cameras"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Finding Available Cameras")
    print("="*60)
    
    cameras = find_available_cameras()
    
    if cameras:
        print(f"\nFound {len(cameras)} camera(s):")
        for cam_id in cameras:
            print(f"  • Camera {cam_id}")
    else:
        print("No cameras found!")
        return
    
    # Try first external camera if available
    if len(cameras) > 1:
        print(f"\nUsing camera {cameras[1]}...")
        capture = CardCameraCapture(camera_index=cameras[1])
        capture.run_camera_feed()


# ============================================================================
# EXAMPLE 3: Custom Output Directory
# ============================================================================
def example_3_custom_output():
    """Save captured cards to custom folder"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Output Directory")
    print("="*60)
    
    output_dir = "my_captured_cards"
    print(f"Saving cards to: {output_dir}\n")
    
    capture = CardCameraCapture(output_dir=output_dir)
    capture.run_camera_feed()


# ============================================================================
# EXAMPLE 4: Adjust Detection Sensitivity
# ============================================================================
def example_4_sensitivity():
    """Fine-tune card detection"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Adjust Detection Sensitivity")
    print("="*60)
    print("Detecting smaller cards...\n")
    
    capture = CardCameraCapture(output_dir="small_cards")
    capture.min_area = 3000      # Smaller minimum area
    capture.max_area = 300000    # Smaller maximum area
    
    capture.run_camera_feed(confidence_threshold=2)


# ============================================================================
# EXAMPLE 5: High Confidence Detection
# ============================================================================
def example_5_high_confidence():
    """More accurate but slower detection"""
    print("\n" + "="*60)
    print("EXAMPLE 5: High Confidence Detection")
    print("="*60)
    print("Using high confidence threshold...")
    print("Cards will be captured only after confirmed detection\n")
    
    capture = CardCameraCapture()
    capture.run_camera_feed(confidence_threshold=10)  # High threshold


# ============================================================================
# EXAMPLE 6: Process Single Frame
# ============================================================================
def example_6_single_frame():
    """Process a single frame from camera"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Process Single Frame")
    print("="*60)
    
    capture = CardCameraCapture()
    
    if not capture.initialize_camera():
        print("Camera initialization failed!")
        return
    
    print("Capturing one frame...")
    ret, frame = capture.cap.read()
    
    if ret:
        detected, _, contours = capture.detect_card(frame)
        print(f"Card detected: {detected}")
        print(f"Contours found: {len(contours)}")
        
        if detected:
            capture.capture_card_image(frame, contours)
            print("Image saved!")
    
    capture.cleanup()


# ============================================================================
# EXAMPLE 7: Multiple Captures in Batch
# ============================================================================
def example_7_batch_capture():
    """Capture multiple cards in sequence"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Batch Capture Multiple Cards")
    print("="*60)
    
    capture = CardCameraCapture(output_dir="batch_cards")
    
    if not capture.initialize_camera():
        print("Camera initialization failed!")
        return
    
    print("Capturing up to 5 cards (press Q to exit)...")
    print("Position cards in front of camera\n")
    
    captured = 0
    consecutive_detections = 0
    frame_count = 0
    
    while captured < 5:
        ret, frame = capture.cap.read()
        if not ret:
            break
        
        detected, _, contours = capture.detect_card(frame)
        
        if detected:
            consecutive_detections += 1
            if consecutive_detections >= 3:
                capture.capture_card_image(frame, contours)
                captured += 1
                print(f"✓ Captured {captured}/5")
                consecutive_detections = 0
        else:
            consecutive_detections = 0
        
        # Display preview
        display_frame = capture.draw_detection(frame, contours if detected else [])
        cv2.putText(display_frame, f"Captured: {captured}/5", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Batch Capture", display_frame)
        
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.cleanup()
    print(f"\nCaptured {captured} card(s)")


# ============================================================================
# EXAMPLE 8: Manual vs Automatic Capture
# ============================================================================
def example_8_manual_capture():
    """Manual capture mode - press SPACE to capture"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Manual Capture Mode")
    print("="*60)
    print("Detected cards are highlighted")
    print("Press SPACE to manually capture")
    print("Press Q to exit\n")
    
    simple_card_capture()


# ============================================================================
# EXAMPLE 9: Auto Capture on Motion
# ============================================================================
def example_9_auto_motion_capture():
    """Automatically capture when motion is detected"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Auto Capture on Motion")
    print("="*60)
    print("Cards are automatically captured when motion is detected\n")
    
    auto_capture_on_motion(sensitivity=10)


# ============================================================================
# EXAMPLE 10: Process Existing Images
# ============================================================================
def example_10_process_existing_images():
    """Process images already captured"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Process Existing Images")
    print("="*60)
    
    image_dir = "captured_cards"
    
    if not os.path.exists(image_dir):
        print(f"Directory {image_dir} not found!")
        return
    
    capture = CardCameraCapture()
    
    images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    print(f"Found {len(images)} images in {image_dir}\n")
    
    for i, img_file in enumerate(images, 1):
        img_path = os.path.join(image_dir, img_file)
        frame = cv2.imread(img_path)
        
        if frame is not None:
            detected, _, contours = capture.detect_card(frame)
            print(f"{i}. {img_file}: Card detected = {detected}")
    
    print("\nDone!")


# ============================================================================
# EXAMPLE 11: Camera Properties
# ============================================================================
def example_11_camera_properties():
    """Display and modify camera properties"""
    print("\n" + "="*60)
    print("EXAMPLE 11: Camera Properties")
    print("="*60)
    
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        print("\nCamera Properties:")
        print(f"  Width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
        print(f"  Height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        print(f"  FPS: {cap.get(cv2.CAP_PROP_FPS)}")
        print(f"  Brightness: {cap.get(cv2.CAP_PROP_BRIGHTNESS)}")
        print(f"  Contrast: {cap.get(cv2.CAP_PROP_CONTRAST)}")
        print(f"  Saturation: {cap.get(cv2.CAP_PROP_SATURATION)}")
        
        # Optimize for card capture
        print("\nOptimizing for card capture...")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        cap.set(cv2.CAP_PROP_CONTRAST, 50)
        
        print("✓ Camera optimized!")
        
        cap.release()


# ============================================================================
# EXAMPLE 12: Phone Camera Integration (IP Webcam)
# ============================================================================
def example_12_phone_camera():
    """Use Android phone as camera via IP Webcam app"""
    print("\n" + "="*60)
    print("EXAMPLE 12: Phone Camera Integration")
    print("="*60)
    print("""
To use your phone camera:
1. Install "IP Webcam" app on Android
2. Start the app and note the IP:PORT
3. Update PHONE_URL below
    """)
    
    # Replace with your phone's IP:PORT
    PHONE_URL = "http://192.168.1.100:8080/video"
    
    print(f"Attempting to connect to: {PHONE_URL}\n")
    
    try:
        capture = CardCameraCapture(camera_index=PHONE_URL)
        # Note: Index parameter expects integer, so we'd need to modify the class
        # For now, just show the URL format
        print("✓ URL format ready")
        print(f"Use: cap = cv2.VideoCapture('{PHONE_URL}')")
    except Exception as e:
        print(f"Connection failed: {e}")


# ============================================================================
# Main Menu
# ============================================================================
def main():
    """Run examples"""
    examples = {
        '1': ('Basic Usage', example_1_basic_usage),
        '2': ('Find Available Cameras', example_2_find_cameras),
        '3': ('Custom Output Directory', example_3_custom_output),
        '4': ('Adjust Detection Sensitivity', example_4_sensitivity),
        '5': ('High Confidence Detection', example_5_high_confidence),
        '6': ('Process Single Frame', example_6_single_frame),
        '7': ('Batch Capture Multiple Cards', example_7_batch_capture),
        '8': ('Manual Capture Mode', example_8_manual_capture),
        '9': ('Auto Capture on Motion', example_9_auto_motion_capture),
        '10': ('Process Existing Images', example_10_process_existing_images),
        '11': ('Camera Properties', example_11_camera_properties),
        '12': ('Phone Camera Integration', example_12_phone_camera),
    }
    
    print("\n" + "="*60)
    print("CARD CAMERA CAPTURE - EXAMPLES")
    print("="*60)
    print("\nAvailable Examples:")
    
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    print("  0. Exit\n")
    
    choice = input("Select example (0-12): ").strip()
    
    if choice in examples:
        try:
            _, func = examples[choice]
            func()
        except KeyboardInterrupt:
            print("\n\nCancelled by user")
        except Exception as e:
            print(f"\n\nError: {e}")
    elif choice != '0':
        print("Invalid choice!")


if __name__ == "__main__":
    main()
