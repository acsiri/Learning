"""
Simple Card Capture Module
Basic card capture functionality for quick usage
"""

import cv2
import os
from datetime import datetime
from .card_detector import CardDetector
from .utils import create_output_directory


def simple_card_capture(camera_id: int = 0, output_dir: str = "output/captured_cards"):
    """Simple camera capture with basic card detection."""
    
    create_output_directory(output_dir)
    
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("Press SPACE to capture | Q to quit")
    print("Position a credit/debit card in front of camera\n")
    
    detector = CardDetector()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect card
        detected, contours = detector.detect(frame)
        
        # Draw detection
        display_frame = frame.copy()
        for contour in contours:
            display_frame = detector.draw_contour(display_frame, contour)
        
        # Display status
        status = "CARD DETECTED ✓" if detected else "Waiting for card..."
        color = (0, 255, 0) if detected else (0, 0, 255)
        cv2.putText(display_frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, color, 2)
        
        cv2.imshow("Card Capture", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' ') and detected and contours:
            # Capture
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_dir, f"card_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✓ Saved: {filename}")
        
        if key == ord('q') or key == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed")


def auto_capture_on_motion(camera_id: int = 0, sensitivity: int = 10):
    """Automatically capture cards when detected with motion."""
    
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    output_dir = "output/auto_captured_cards"
    create_output_directory(output_dir)
    
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
            # Calculate motion
            diff = cv2.absdiff(previous_gray, gray)
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            motion = cv2.countNonZero(thresh)
            
            if motion > sensitivity * 1000:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                filename = os.path.join(output_dir, f"card_{timestamp}.jpg")
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
