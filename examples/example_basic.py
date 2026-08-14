"""
Example 1: Basic Camera Capture
Simple demonstration of card capture functionality
"""

from src import CardCameraCapture, find_available_cameras


def main():
    """Run basic capture example"""
    print("\n" + "="*60)
    print("Example 1: Basic Camera Capture")
    print("="*60 + "\n")
    
    # Find cameras
    cameras = find_available_cameras()
    if not cameras:
        print("No cameras found!")
        return
    
    print(f"Found cameras: {cameras}")
    
    # Create capture instance
    capture = CardCameraCapture(camera_index=cameras[0])
    
    # Run with default settings
    capture.run_camera_feed()


if __name__ == "__main__":
    main()
