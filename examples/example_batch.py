"""
Example 2: Batch Capture Multiple Cards
Capture multiple cards in sequence
"""

import cv2
from src import CardCameraCapture


def main():
    """Capture multiple cards"""
    print("\n" + "="*60)
    print("Example 2: Batch Capture Multiple Cards")
    print("="*60 + "\n")
    
    capture = CardCameraCapture(output_dir="output/batch_cards")
    
    if not capture.initialize_camera():
        print("Camera initialization failed!")
        return
    
    print("Capturing up to 5 cards (press Q to exit)...")
    print("Position cards in front of camera\n")
    
    captured = 0
    consecutive_detections = 0
    
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
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    capture.cleanup()
    print(f"\n✓ Captured {captured} card(s)")


if __name__ == "__main__":
    main()
