import os
import sys
from ReadCardExtract import EasyTextExtractor

print("=" * 60)
print("DEBUG: Starting ReadCardExtract Debugger")
print("=" * 60)

# Check if image exists
image_path = 'sample.jpg'
print(f"\n1. Checking image file...")
print(f"   Looking for: {image_path}")
print(f"   Exists: {os.path.exists(image_path)}")
if os.path.exists(image_path):
    file_size = os.path.getsize(image_path)
    print(f"   File size: {file_size} bytes")

# Initialize extractor
print(f"\n2. Initializing EasyTextExtractor...")
try:
    extractor = EasyTextExtractor(languages=['en'])
    print("   ✓ Extractor created successfully")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test extract_text method
print(f"\n3. Testing extract_text()...")
try:
    result = extractor.extract_text(image_path)
    
    if 'error' in result:
        print(f"   ✗ Error in result: {result['error']}")
    else:
        print(f"   ✓ Extraction successful!")
        print(f"\n   Full Text:")
        print(f"   {'-' * 50}")
        print(result['full_text'])
        print(f"   {'-' * 50}")
        
        print(f"\n   Detailed Results ({len(result['detailed_results'])} regions):")
        for i, item in enumerate(result['detailed_results']):
            print(f"   [{i}] Text: '{item['text']}'")
            print(f"       Confidence: {item['confidence']:.4f}")
            print(f"       Coordinates: {item['coordinates']}")
            
except Exception as e:
    print(f"   ✗ Exception: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("DEBUG: Complete")
print("=" * 60)
