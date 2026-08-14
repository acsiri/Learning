import easyocr
import cv2
import os
from matplotlib import pyplot as plt

class EasyTextExtractor:
    def __init__(self, languages=['en']):
        """Initialize EasyOCR reader"""
        self.reader = easyocr.Reader(languages)
    
    def extract_text(self, image_path):
        """Extract text from image"""
        try:
            results = self.reader.readtext(image_path)
            
            extracted_data = {
                "full_text": "\n".join([text[1] for text in results]),
                "detailed_results": [
                    {
                        "text": text[1],
                        "confidence": text[2],
                        "coordinates": text[0]
                    }
                    for text in results
                ]
            }
            
            return extracted_data
        
        except Exception as e:
            return {"error": str(e)}
    
    def extract_with_visualization(self, image_path):
        """Extract text and visualize results"""
        img = cv2.imread(image_path)
        results = self.reader.readtext(image_path)
        
        # Draw bounding boxes
        for (bbox, text, confidence) in results:
            bbox = [[int(x), int(y)] for x, y in bbox]
            cv2.polylines(img, [bbox], True, (0, 255, 0), 2)
            cv2.putText(img, text, (bbox[0][0], bbox[0][1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title("Text Detection")
        plt.show()
        
        # Return extracted text
        return "\n".join([text[1] for text in results])
    
    def extract_multiple_languages(self, image_path, languages=['en', 'es', 'fr']):
        """Extract text in multiple languages"""
        results = {}
        for lang in languages:
            reader = easyocr.Reader([lang])
            ocr_results = reader.readtext(image_path)
            results[lang] = "\n".join([text[1] for text in ocr_results])
        return results

# Usage
if __name__ == "__main__":
   
    
    print("\n" + "="*70)
    print("VISUAL DEBUG: ReadCardExtract")
    print("="*70)
    
    # BREAKPOINT 1: Initialize
    print("\n[DEBUG 1] Initializing EasyTextExtractor...")
    extractor = EasyTextExtractor(languages=['en'])
    print("✓ Extractor initialized")
    
    # BREAKPOINT 2: Check image
    print("\n[DEBUG 2] Checking for sample.jpg...")
    image_path = 'sample.jpg'
    if not os.path.exists(image_path):
        print(f"✗ File not found: {image_path}")
        exit(1)
    print(f"✓ Found: {image_path} ({os.path.getsize(image_path)} bytes)")
    
    # BREAKPOINT 3: Extract text
    print("\n[DEBUG 3] Extracting text from image...")
    result = extractor.extract_text(image_path)
    
    # BREAKPOINT 4: Check results
    print("\n[DEBUG 4] Processing results...")
    if 'error' in result:
        print(f"✗ Error: {result['error']}")
    else:
        print(f"✓ Extracted {len(result['detailed_results'])} text regions")
    
    # BREAKPOINT 5: Display results
    print("\n[DEBUG 5] Displaying extracted text...")
    print("-"*70)
    print("FULL TEXT:")
    print(result['full_text'])
    print("-"*70)
    
    # BREAKPOINT 6: Show confidence scores
    print("\n[DEBUG 6] Confidence scores:")
    scores = [(r['text'], r['confidence']) for r in result['detailed_results']]
    for text, confidence in scores:
        status = "✓" if confidence > 0.5 else "⚠"
        print(f"  {status} '{text}': {confidence:.4f}")
    
    print("\n" + "="*70)
    print("DEBUGGING COMPLETE")
    print("="*70 + "\n")