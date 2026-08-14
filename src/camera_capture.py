"""
Camera Capture Module
Main module for credit/debit card camera capture
"""

import cv2
import numpy as np
import imutils
from typing import Tuple, Optional, List
from datetime import datetime
import os

from .card_detector import CardDetector
from .utils import create_output_directory, generate_timestamp_filename, save_image


class CardCameraCapture:
    """Captures images of credit/debit cards using camera feed."""
    
    def __init__(self, output_dir: str = "output/captured_cards", camera_index: int = 0):
        """
        Initialize the card camera capture system.
        
        Args:
            output_dir: Directory to save captured card images
            camera_index: Camera index (0 for default)
        """
        self.output_dir = output_dir
        self.camera_index = camera_index
        self.cap = None
        self.detector = CardDetector()
        
        create_output_directory(output_dir)
        print(f"Output directory: {output_dir}")
    
    def initialize_camera(self) -> bool:
        """Initialize camera connection."""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                print(f"Error: Could not open camera at index {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"✓ Camera initialized at index {self.camera_index}")
            return True
        
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def detect_card(self, frame: np.ndarray) -> Tuple[bool, np.ndarray, List]:
        """Detect cards in frame."""
        detected, contours = self.detector.detect(frame)
        return detected, frame, contours
    
    def draw_detection(self, frame: np.ndarray, contours: list) -> np.ndarray:
        """Draw detection results on frame."""
        output_frame = frame.copy()
        
        for contour in contours:
            output_frame = self.detector.draw_contour(output_frame, contour)
        
        return output_frame
    
    def capture_card_image(self, frame: np.ndarray, contours: list) -> bool:
        """Capture and save detected card image."""
        if not contours:
            return False
        
        try:
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Extract card region
            card_region = frame[y:y+h, x:x+w]
            
            # Generate filename
            filename = generate_timestamp_filename()
            
            # Save image
            if save_image(card_region, self.output_dir, filename):
                print(f"✓ Card captured: {filename}")
                return True
            
            return False
        
        except Exception as e:
            print(f"Error capturing card: {e}")
            return False
    
    def run_camera_feed(self, confidence_threshold: int = 3, 
                       save_every_n_frames: int = 1):
        """Run continuous camera feed with card detection."""
        if not self.initialize_camera():
            return
        
        consecutive_detections = 0
        frame_count = 0
        
        print("\n" + "="*60)
        print("Camera Feed Active - Card Detection Running")
        print("="*60)
        print("Controls:")
        print("  - Press 'SPACE' to manually capture")
        print("  - Press 'ESC' or 'Q' to exit")
        print("="*60 + "\n")
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Failed to read frame")
                    break
                
                # Resize for processing
                frame = imutils.resize(frame, width=1280)
                
                # Detect card
                detected, _, contours = self.detect_card(frame)
                
                # Draw detection
                display_frame = self.draw_detection(frame, contours if detected else [])
                
                # Add status text
                status = "CARD DETECTED" if detected else "No card"
                color = (0, 255, 0) if detected else (0, 0, 255)
                cv2.putText(display_frame, f"Status: {status}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(display_frame, f"Frames: {frame_count}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Update detection counter
                if detected:
                    consecutive_detections += 1
                    
                    if consecutive_detections >= confidence_threshold and \
                       frame_count % save_every_n_frames == 0:
                        self.capture_card_image(frame, contours)
                        consecutive_detections = 0
                else:
                    consecutive_detections = 0
                
                # Display frame
                cv2.imshow("Card Camera Capture", display_frame)
                frame_count += 1
                
                # Handle input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == 27:  # Q or ESC
                    print("\nExiting camera feed...")
                    break
                elif key == ord(' '):  # Space for manual capture
                    if detected and contours:
                        self.capture_card_image(frame, contours)
                    else:
                        print("No card in current frame")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Camera closed")
