"""
Card Camera Capture Package
Automatic detection and capture of credit/debit cards from camera feed
"""

__version__ = "1.0.0"
__author__ = "Card Vision Team"

from .camera_capture import CardCameraCapture
from .simple_capture import simple_card_capture, auto_capture_on_motion
from .card_detector import CardDetector
from .utils import find_available_cameras
from .chatbot import SimpleChatbot, CardCaptureBot, ConversationalBot

__all__ = [
    'CardCameraCapture',
    'simple_card_capture',
    'auto_capture_on_motion',
    'CardDetector',
    'find_available_cameras',
    'SimpleChatbot',
    'CardCaptureBot',
    'ConversationalBot',
]
