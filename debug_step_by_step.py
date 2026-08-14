import os
import sys
import pdb
from ReadCardExtract import EasyTextExtractor

print("=" * 70)
print("STEP-BY-STEP DEBUGGER FOR ReadCardExtract.py")
print("=" * 70)
print("\nCommands: n (next), s (step), c (continue), p variable (print), q (quit)")
print()

# Step 1: Create extractor
print("\n[STEP 1] Creating EasyTextExtractor...")
pdb.set_trace()  # BREAKPOINT - Debug will start here
extractor = EasyTextExtractor(languages=['en'])

# Step 2: Define image path
print("\n[STEP 2] Setting image path...")
pdb.set_trace()  # BREAKPOINT
image_path = 'sample.jpg'

# Step 3: Check if file exists
print("\n[STEP 3] Checking if file exists...")
pdb.set_trace()  # BREAKPOINT
file_exists = os.path.exists(image_path)
print(f"File exists: {file_exists}")

# Step 4: Call extract_text
print("\n[STEP 4] Calling extract_text()...")
pdb.set_trace()  # BREAKPOINT
result = extractor.extract_text(image_path)

# Step 5: Check for errors
print("\n[STEP 5] Checking result for errors...")
pdb.set_trace()  # BREAKPOINT
has_error = 'error' in result

# Step 6: Print results
print("\n[STEP 6] Displaying results...")
pdb.set_trace()  # BREAKPOINT

if has_error:
    print(f"ERROR: {result['error']}")
else:
    print(f"\n✓ SUCCESS! Extracted {len(result['detailed_results'])} text regions:")
    print(f"\nFull Text:\n{result['full_text']}")
    
    print(f"\n\nDetailed Breakdown:")
    for i, item in enumerate(result['detailed_results']):
        print(f"\n  Region {i}:")
        print(f"    Text: '{item['text']}'")
        print(f"    Confidence: {item['confidence']:.4f}")
        print(f"    Position: {item['coordinates']}")

print("\n" + "=" * 70)
print("DEBUGGING COMPLETE")
print("=" * 70)
