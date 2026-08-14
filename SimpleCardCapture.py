"""
Simple Card Camera Capture - Basic version for quick setup
Uses OpenCV for camera access and card detection
"""

import cv2
import numpy as np
from datetime import datetime
import os


def simple_card_capture(camera_id=0, output_dir="captured_cards"):
    """
    Simple camera capture with basic card detection.
    
    Args:
        camera_id: Camera index (0 = default, 1+ = mobile/USB cameras)
        output_dir: Directory to save images
    """
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize camera
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        return
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("Press SPACE to capture | Q to quit")
    print("Position a credit/debit card in front of camera\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect edges (card borders)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for card-like shapes
        card_found = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 10000 < area < 500000:  # Card size range
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = w / h
                
                # Credit card aspect ratio ~1.59:1
                if 1.3 < aspect_ratio < 1.8:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Card Detected!", (x, y-10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    card_found = True
        
        # Display status
        status = "CARD DETECTED ✓" if card_found else "Waiting for card..."
        color = (0, 255, 0) if card_found else (0, 0, 255)
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, color, 2)
        
        cv2.imshow("Card Capture", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' ') and card_found:  # Space to capture
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"card_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✓ Saved: {filename}")
        
        if key == ord('q') or key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed")


def auto_capture_on_motion(camera_id=0, sensitivity=10):
    """
    Automatically capture cards when detected with motion.
    """
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    os.makedirs("auto_captured_cards", exist_ok=True)
    
    previous_gray = None
    capture_count = 0
    
    print("Auto-capture mode: Moving cards will be captured automatically\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        if previous_gray is not None:
            # Calculate frame difference (motion detection)
            diff = cv2.absdiff(previous_gray, gray)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            
            motion = cv2.countNonZero(thresh)
            
            if motion > sensitivity * 1000:  # Motion detected
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = f"auto_captured_cards/card_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                capture_count += 1
                print(f"✓ Auto-captured: {filename}")
        
        cv2.putText(frame, f"Auto-captures: {capture_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Auto Capture Mode", frame)
        
        previous_gray = gray
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Choose mode
    print("\n1. Manual capture (press SPACE when card is detected)")
    print("2. Auto-capture (captures on motion)")
    
    choice = input("\nSelect mode (1 or 2): ").strip()
    
    if choice == "2":
        auto_capture_on_motion()
    else:
        simple_card_capture()
