"""
Camera Card Capture - Detects credit/debit cards and captures images
Supports both system camera and mobile camera via USB connection
"""

import cv2
import numpy as np
import os
from datetime import datetime
from typing import Tuple, Optional
import imutils


class CardCameraCapture:
    """
    Captures images of credit/debit cards using camera feed.
    Detects cards based on shape, color, and size characteristics.
    """
    
    def __init__(self, output_dir: str = "captured_cards", camera_index: int = 0):
        """
        Initialize the card camera capture system.
        
        Args:
            output_dir: Directory to save captured card images
            camera_index: Camera index (0 for default, 1+ for additional cameras/mobiles)
        """
        self.output_dir = output_dir
        self.camera_index = camera_index
        self.cap = None
        self.card_detected = False
        self.min_area = 10000  # Minimum card area in pixels
        self.max_area = 500000  # Maximum card area in pixels
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
    
    def initialize_camera(self) -> bool:
        """
        Initialize camera connection.
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                print(f"Error: Could not open camera at index {self.camera_index}")
                return False
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"Camera initialized successfully at index {self.camera_index}")
            return True
        
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def detect_card(self, frame: np.ndarray) -> Tuple[bool, Optional[np.ndarray], Optional[list]]:
        """
        Detect credit/debit card in the frame using contour detection.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Tuple of (card_detected, processed_frame, contours)
        """
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilate edges to connect nearby edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(edges, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by card-like characteristics
        card_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < self.min_area or area > self.max_area:
                continue
            
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Check if it's a quadrilateral (4 corners)
            if len(approx) == 4:
                # Calculate aspect ratio (credit cards are ~1.59:1)
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                
                # Check if aspect ratio is close to credit card ratio
                if 1.3 < aspect_ratio < 1.8:
                    card_contours.append(contour)
        
        detected = len(card_contours) > 0
        return detected, frame, card_contours
    
    def draw_detection(self, frame: np.ndarray, contours: list) -> np.ndarray:
        """
        Draw detection rectangles on the frame.
        
        Args:
            frame: Input frame
            contours: List of detected card contours
            
        Returns:
            Frame with drawn rectangles
        """
        output_frame = frame.copy()
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(output_frame, "Card Detected", (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return output_frame
    
    def capture_card_image(self, frame: np.ndarray, contours: list) -> bool:
        """
        Capture and save the detected card image.
        
        Args:
            frame: Input frame
            contours: List of detected card contours
            
        Returns:
            True if image saved successfully
        """
        if not contours:
            return False
        
        try:
            # Get the largest contour (most likely the card)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Extract the card region
            card_region = frame[y:y+h, x:x+w]
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = os.path.join(self.output_dir, f"card_{timestamp}.jpg")
            
            # Save the image
            cv2.imwrite(filename, card_region)
            print(f"✓ Card image captured: {filename}")
            
            return True
        
        except Exception as e:
            print(f"Error capturing card image: {e}")
            return False
    
    def run_camera_feed(self, confidence_threshold: int = 3, save_every_n_frames: int = 1):
        """
        Run continuous camera feed with card detection and capture.
        
        Args:
            confidence_threshold: Number of consecutive frames to confirm card detection
            save_every_n_frames: Save an image every N detected frames (prevents duplicates)
            
        Returns:
            None
        """
        if not self.initialize_camera():
            return
        
        consecutive_detections = 0
        frame_count = 0
        
        print("\n" + "="*60)
        print("Camera Feed Active - Card Detection Running")
        print("="*60)
        print("Controls:")
        print("  - Press 'SPACE' to manually capture a frame")
        print("  - Press 'ESC' or 'Q' to exit")
        print("="*60 + "\n")
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Failed to read frame from camera")
                    break
                
                # Resize frame for faster processing
                frame = imutils.resize(frame, width=1280)
                
                # Detect card
                card_detected, processed_frame, contours = self.detect_card(frame)
                
                # Draw detection results
                display_frame = self.draw_detection(frame, contours if card_detected else [])
                
                # Add status text
                status = "CARD DETECTED" if card_detected else "No card detected"
                color = (0, 255, 0) if card_detected else (0, 0, 255)
                cv2.putText(display_frame, f"Status: {status}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(display_frame, f"Frames: {frame_count}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Update consecutive detection counter
                if card_detected:
                    consecutive_detections += 1
                    
                    # Capture on confidence threshold
                    if consecutive_detections >= confidence_threshold and frame_count % save_every_n_frames == 0:
                        self.capture_card_image(frame, contours)
                        consecutive_detections = 0  # Reset counter
                else:
                    consecutive_detections = 0
                
                # Display the frame
                cv2.imshow("Card Camera Capture", display_frame)
                
                frame_count += 1
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:  # 'Q' or ESC
                    print("\nExiting camera feed...")
                    break
                elif key == ord(' '):  # SPACE for manual capture
                    if card_detected and contours:
                        self.capture_card_image(frame, contours)
                    else:
                        print("No card detected in current frame for manual capture")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        print("\nCamera feed closed successfully")


def find_available_cameras(max_index: int = 10) -> list:
    """
    Scan for available cameras on the system.
    
    Args:
        max_index: Maximum camera index to check
        
    Returns:
        List of available camera indices
    """
    available_cameras = []
    
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    
    return available_cameras


def main():
    """Main function to run the card capture system."""
    
    print("\n" + "="*60)
    print("CREDIT/DEBIT CARD CAMERA CAPTURE SYSTEM")
    print("="*60 + "\n")
    
    # Find available cameras
    print("Scanning for available cameras...")
    available_cameras = find_available_cameras()
    
    if not available_cameras:
        print("Error: No cameras found on the system!")
        return
    
    print(f"Found {len(available_cameras)} camera(s): {available_cameras}\n")
    
    # Select camera
    if len(available_cameras) > 1:
        print("Available cameras:")
        for i, cam_idx in enumerate(available_cameras):
            print(f"  {i}: Camera {cam_idx}")
        
        choice = input("\nSelect camera index (0-9, default=0): ").strip()
        camera_index = int(choice) if choice and choice.isdigit() else available_cameras[0]
    else:
        camera_index = available_cameras[0]
    
    print(f"Using camera index: {camera_index}\n")
    
    # Initialize and run capture system
    capture = CardCameraCapture(output_dir="captured_cards", camera_index=camera_index)
    capture.run_camera_feed(confidence_threshold=3, save_every_n_frames=1)


if __name__ == "__main__":
    main()
