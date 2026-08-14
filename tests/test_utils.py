"""
Tests for Camera Capture Module
"""

import unittest
import os
from src.utils import (
    find_available_cameras,
    generate_timestamp_filename,
    create_output_directory,
    list_captured_images,
)


class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_generate_timestamp_filename(self):
        """Test timestamp filename generation"""
        filename = generate_timestamp_filename()
        self.assertTrue(filename.startswith("card_"))
        self.assertTrue(filename.endswith(".jpg"))
    
    def test_generate_custom_prefix(self):
        """Test custom filename prefix"""
        filename = generate_timestamp_filename(prefix="test")
        self.assertTrue(filename.startswith("test_"))
    
    def test_create_output_directory(self):
        """Test directory creation"""
        test_dir = "test_output"
        result = create_output_directory(test_dir)
        self.assertTrue(result)
        
        if os.path.exists(test_dir):
            os.rmdir(test_dir)
    
    def test_list_images_empty(self):
        """Test listing images in non-existent directory"""
        images = list_captured_images("nonexistent_dir")
        self.assertEqual(images, [])


class TestCameraDetection(unittest.TestCase):
    """Test card detection"""
    
    def test_detector_initialization(self):
        """Test CardDetector initialization"""
        from src.card_detector import CardDetector
        
        detector = CardDetector()
        self.assertEqual(detector.min_area, 10000)
        self.assertEqual(detector.max_area, 500000)
    
    def test_detector_custom_params(self):
        """Test custom detection parameters"""
        from src.card_detector import CardDetector
        
        detector = CardDetector(min_area=5000, max_area=300000)
        self.assertEqual(detector.min_area, 5000)
        self.assertEqual(detector.max_area, 300000)


if __name__ == "__main__":
    unittest.main()
