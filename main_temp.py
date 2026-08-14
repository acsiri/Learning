"""
Main entry point for Card Camera Capture project
"""

if __name__ == "__main__":
    from src import CardCameraCapture, find_available_cameras
    
    print("\n" + "="*60)
    print("CREDIT/DEBIT CARD CAMERA CAPTURE")
    print("="*60 + "\n")
    
    # Find cameras
    print("Scanning for available cameras...")
    cameras = find_available_cameras()
    
    if not cameras:
        print("Error: No cameras found!")
        exit(1)
    
    print(f"Found {len(cameras)} camera(s): {cameras}\n")
    
    # Select camera
    if len(cameras) > 1:
        print("Available cameras:")
        for i, cam in enumerate(cameras):
            print(f"  {i}: Camera {cam}")
        choice = input("\nSelect camera (default=0): ").strip()
        camera_index = int(choice) if choice and choice.isdigit() else cameras[0]
    else:
        camera_index = cameras[0]
    
    print(f"Using camera {camera_index}\n")
    
    # Start capture
    capture = CardCameraCapture(camera_index=camera_index)
    capture.run_camera_feed(confidence_threshold=3)
