"""
Vision AI Card Extractor - Comprehensive Test & Comparison Script
Tests all extraction methods and compares results
"""

import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent))

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_section(title):
    """Print formatted section"""
    print(f"\n  ▶ {title}")
    print("  " + "-"*76)

def test_setup():
    """Test if environment is properly set up"""
    print_header("ENVIRONMENT SETUP TEST")
    
    # Check .env file
    print_section("Checking .env file")
    if os.path.exists(".env"):
        print("  ✓ .env file found")
        load_dotenv()
        
        if os.getenv("GEMINI_API_KEY"):
            api_key = os.getenv("GEMINI_API_KEY")
           
            masked_key = api_key[:10] + "..." + api_key[-5:]
            print(f"  ✓ GEMINI_API_KEY configured: {masked_key}")
        else:
            print("  ✗ GEMINI_API_KEY not set in .env")
            return False
    else:
        print("  ⚠ .env file not found - create one with GEMINI_API_KEY")
        return False
    
    # Check required packages
    print_section("Checking required packages")
    required = {
        "google.generativeai": "google-generativeai",
        "dotenv": "python-dotenv",
        "cv2": "opencv-python (optional)"
    }
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            if "optional" in package:
                print(f"  ⚠ {package} - optional")
            else:
                print(f"  ✗ {package} - install with: pip install {package}")
    
    # Test Gemini connection
    print_section("Testing Gemini API connection")
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'OK' - just one word")
        
        if "OK" in response.text or "ok" in response.text.lower():
            print("  ✓ Gemini API working")
            return True
        else:
            print(f"  ✗ Unexpected response: {response.text[:50]}")
            return False
    
    except Exception as e:
        print(f"  ✗ Gemini API error: {e}")
        return False

def test_quick_start():
    """Test CardVisionQuickStart methods"""
    print_header("QUICK START EXAMPLES TEST")
    
    try:
        from CardVisionQuickStart import read_card_simple, read_card_with_structure, read_id_card
        
        # Find test image
        test_image = None
        for img in ["sample_card.jpg", "card.jpg", "test_card.jpg"]:
            if os.path.exists(img):
                test_image = img
                break
        
        if not test_image:
            print_section("No test image found")
            print("  ⚠ Skipping tests - provide a card image (sample_card.jpg)")
            return False
        
        # Test 1: Simple extraction
        print_section("Test 1: Simple Card Text Extraction")
        print(f"  Processing: {test_image}")
        try:
            result = read_card_simple(test_image)
            print(f"  ✓ Success - Extracted {len(result)} characters")
            print(f"  Preview: {result[:100]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        # Test 2: Structured extraction
        print_section("Test 2: Structured Card Details (JSON)")
        try:
            result = read_card_with_structure(test_image)
            print(f"  ✓ Success")
            if result.startswith('{'):
                try:
                    data = json.loads(result)
                    print(f"  Fields extracted: {list(data.keys())}")
                except:
                    print(f"  Preview: {result[:100]}...")
            else:
                print(f"  Preview: {result[:100]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        # Test 3: ID Card extraction
        print_section("Test 3: ID Card Extraction")
        id_images = ["sample_id.jpg", "id_card.jpg"]
        id_found = any(os.path.exists(img) for img in id_images)
        
        if id_found:
            id_image = next(img for img in id_images if os.path.exists(img))
            try:
                result = read_id_card(id_image)
                print(f"  ✓ Success - Extracted ID information")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print("  ⚠ No ID image found - skipping")
        
        return True
    
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False

def test_card_extractor():
    """Test CardVisionExtractor class"""
    print_header("CARD VISION EXTRACTOR CLASS TEST")
    
    try:
        from CardVisionExtractor import CardVisionExtractor
        
        # Find test image
        test_image = None
        for img in ["sample_card.jpg", "card.jpg", "test_card.jpg"]:
            if os.path.exists(img):
                test_image = img
                break
        
        if not test_image:
            print_section("No test image found")
            print("  ⚠ Skipping - provide a card image")
            return False
        
        # Initialize extractor
        print_section("Initializing CardVisionExtractor")
        extractor = CardVisionExtractor()
        print("  ✓ Extractor initialized")
        
        # Test 1: Basic extraction
        print_section("Test 1: Extract Card Details")
        result = extractor.extract_card_details(test_image)
        
        if result["status"] == "success":
            print("  ✓ Extraction successful")
            if isinstance(result["details"], dict):
                for key, value in result["details"].items():
                    if not str(value).startswith("<"):
                        print(f"    - {key}: {str(value)[:60]}")
        else:
            print(f"  ✗ Error: {result.get('message', 'Unknown error')}")
        
        # Test 2: Confidence scoring
        print_section("Test 2: Extract with Confidence Scores")
        result = extractor.extract_with_confidence(test_image)
        
        if result["status"] == "success":
            print("  ✓ Extraction with confidence successful")
        else:
            print(f"  ✗ Error: {result.get('message')}")
        
        # Test 3: Verification
        print_section("Test 3: Verify Details")
        details_to_verify = {
            "card_type": "Visa",
            "expiry": "12/25"
        }
        
        result = extractor.verify_card_details(test_image, details_to_verify)
        
        if result["status"] == "success":
            print("  ✓ Verification completed")
        else:
            print(f"  ✗ Error: {result.get('message')}")
        
        return True
    
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_advanced_processor():
    """Test AdvancedCardVisionProcessor"""
    print_header("ADVANCED CARD PROCESSOR TEST")
    
    try:
        from AdvancedCardVisionProcessor import AdvancedCardProcessor
        
        # Find test images
        test_images = []
        for img in ["sample_card.jpg", "card.jpg", "test_card.jpg"]:
            if os.path.exists(img):
                test_images.append(img)
        
        if not test_images:
            print_section("No test images found")
            print("  ⚠ Skipping - provide card images")
            return False
        
        # Initialize processor
        print_section("Initializing AdvancedCardProcessor")
        processor = AdvancedCardProcessor()
        print("  ✓ Processor initialized")
        
        # Test 1: Caching
        print_section("Test 1: Process with Caching")
        result = processor.process_with_cache(test_images[0])
        print("  ✓ First run - result cached")
        
        result2 = processor.process_with_cache(test_images[0])
        print("  ✓ Second run - loaded from cache")
        
        # Test 2: Batch processing
        print_section("Test 2: Batch Processing")
        if len(test_images) > 1:
            results = processor.batch_process(test_images[:2])
            print(f"  ✓ Processed {len(results)} images")
            for r in results:
                print(f"    - {r.get('status')}")
        else:
            print("  ⚠ Only one test image - skipping batch test")
        
        # Test 3: Consistency check
        print_section("Test 3: Consistency Verification")
        consistency = processor.compare_multiple_extractions(test_images[0], num_passes=2)
        consistency_score = consistency['consistency_analysis'].get('consistency_score', 0)
        print(f"  ✓ Consistency score: {consistency_score:.1f}%")
        
        # Test 4: Validation
        print_section("Test 4: Extract and Validate")
        validation = processor.extract_and_validate(test_images[0])
        print(f"  ✓ Validation completed")
        
        # Clear cache at end
        print_section("Cleanup")
        processor.clear_cache()
        print("  ✓ Cache cleared")
        
        return True
    
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_file_operations():
    """Test file operations and formats"""
    print_header("FILE OPERATIONS TEST")
    
    print_section("Checking Python files")
    
    required_files = {
        "CardVisionExtractor.py": "Full-featured extractor",
        "CardVisionQuickStart.py": "Quick start examples",
        "AdvancedCardVisionProcessor.py": "Advanced processor",
        "VisionAI_Reference_Guide.py": "Reference guide",
        "VISION_AI_GUIDE.md": "Complete guide",
    }
    
    for filename, description in required_files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✓ {filename} ({size:,} bytes) - {description}")
        else:
            print(f"  ✗ {filename} - MISSING")
    
    print_section("Checking .env configuration")
    if os.path.exists(".env"):
        print("  ✓ .env file exists")
    else:
        print("  ⚠ .env file not found")
        print("    Create with: GEMINI_API_KEY=your_key_here")

def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    
    print_section("Results")
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"  {status} - {test_name}")
    
    print_section("Overall")
    print(f"  Passed: {passed}/{total}")
    
    if passed == total:
        print("  🎉 All tests passed!")
    elif passed > 0:
        print(f"  ⚠ {total - passed} test(s) failed")
    else:
        print("  ✗ All tests failed - check setup")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  VISION AI CARD EXTRACTOR - COMPREHENSIVE TEST SUITE".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run all tests
    results = {
        "Environment Setup": test_setup(),
        "Quick Start": test_quick_start(),
        "Card Extractor": test_card_extractor(),
        "Advanced Processor": test_advanced_processor(),
        "File Operations": test_file_operations(),
    }
    
    # Print summary
    print_summary(results)
    
    print("\n" + "="*80)
    print("  For detailed usage, see: VISION_AI_GUIDE.md")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
