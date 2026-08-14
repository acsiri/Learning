"""
Utility Functions for Card Camera Capture
"""

import os
import cv2
from datetime import datetime
from typing import List, Tuple


def find_available_cameras(max_index: int = 10) -> List[int]:
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


def create_output_directory(directory: str) -> bool:
    """
    Create output directory if it doesn't exist.
    
    Args:
        directory: Path to create
        
    Returns:
        True if successful
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False


def generate_timestamp_filename(prefix: str = "card", 
                               suffix: str = ".jpg") -> str:
    """
    Generate timestamp-based filename.
    
    Args:
        prefix: Filename prefix
        suffix: File extension
        
    Returns:
        Formatted filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    return f"{prefix}_{timestamp}{suffix}"


def save_image(frame, output_dir: str, filename: str) -> bool:
    """
    Save image to disk.
    
    Args:
        frame: Image frame to save
        output_dir: Output directory
        filename: Filename
        
    Returns:
        True if successful
    """
    try:
        if not create_output_directory(output_dir):
            return False
        
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, frame)
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


def get_image_info(image_path: str) -> dict:
    """
    Get information about an image file.
    
    Args:
        image_path: Path to image
        
    Returns:
        Dictionary with image info
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {}
        
        h, w = img.shape[:2]
        return {
            'width': w,
            'height': h,
            'size': os.path.getsize(image_path),
            'path': image_path,
        }
    except Exception as e:
        print(f"Error reading image: {e}")
        return {}


def list_captured_images(directory: str) -> List[str]:
    """
    List all captured images in directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of image filenames
    """
    try:
        if not os.path.exists(directory):
            return []
        
        extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        images = []
        
        for file in os.listdir(directory):
            if os.path.splitext(file)[1].lower() in extensions:
                images.append(file)
        
        return sorted(images)
    except Exception as e:
        print(f"Error listing images: {e}")
        return []
