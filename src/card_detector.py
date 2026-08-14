"""
Card Detection Module
Handles detection of credit/debit cards in image frames
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List


class CardDetector:
    """Detects credit/debit cards in images using computer vision."""
    
    def __init__(self, min_area: int = 10000, max_area: int = 500000):
        """
        Initialize the card detector.
        
        Args:
            min_area: Minimum card area in pixels
            max_area: Maximum card area in pixels
        """
        self.min_area = min_area
        self.max_area = max_area
        self.min_aspect_ratio = 1.3
        self.max_aspect_ratio = 1.8
    
    def detect(self, frame: np.ndarray) -> Tuple[bool, List[np.ndarray]]:
        """
        Detect cards in the frame.
        
        Args:
            frame: Input image frame
            
        Returns:
            Tuple of (detected: bool, contours: list)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilate to connect edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(edges, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours for card-like shapes
        card_contours = self._filter_contours(contours)
        
        return len(card_contours) > 0, card_contours
    
    def _filter_contours(self, contours: List) -> List[np.ndarray]:
        """
        Filter contours by card characteristics.
        
        Args:
            contours: List of detected contours
            
        Returns:
            List of filtered card contours
        """
        card_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Check area bounds
            if area < self.min_area or area > self.max_area:
                continue
            
            # Check if quadrilateral
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) != 4:
                continue
            
            # Check aspect ratio
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            
            if self.min_aspect_ratio < aspect_ratio < self.max_aspect_ratio:
                card_contours.append(contour)
        
        return card_contours
    
    def get_bounding_box(self, contour: np.ndarray) -> Tuple[int, int, int, int]:
        """Get bounding box coordinates."""
        return cv2.boundingRect(contour)
    
    def draw_contour(self, frame: np.ndarray, contour: np.ndarray, 
                    color: Tuple[int, int, int] = (0, 255, 0), 
                    thickness: int = 2) -> np.ndarray:
        """Draw contour on frame."""
        output = frame.copy()
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(output, (x, y), (x + w, y + h), color, thickness)
        cv2.putText(output, "Card Detected", (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return output
