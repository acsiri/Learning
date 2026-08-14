"""
Advanced Vision AI Card Processing Examples
Shows batch processing, caching, and best practices
"""

import os
import base64
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class AdvancedCardProcessor:
    """Advanced card processing with caching, batch processing, and verification"""
    
    def __init__(self, cache_dir=".card_cache"):
        """Initialize with optional caching"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        print(f"✓ Initialized advanced processor (cache: {cache_dir})")
    
    def _get_cache_key(self, image_path):
        """Generate cache key from image hash"""
        with open(image_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _load_image(self, image_path):
        """Load image as base64"""
        with open(image_path, 'rb') as f:
            data = base64.standard_b64encode(f.read()).decode('utf-8')
        
        ext = Path(image_path).suffix.lower()
        media_types = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'
        }
        
        return {
            'inline_data': {
                'mime_type': media_types.get(ext, 'image/jpeg'),
                'data': data
            }
        }
    
    def process_with_cache(self, image_path, force_reprocess=False):
        """Process image with caching"""
        cache_key = self._get_cache_key(image_path)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        # Return cached result if available
        if cache_file.exists() and not force_reprocess:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            print(f"✓ Using cached result for {image_path}")
            return cached
        
        # Process new image
        print(f"Processing {image_path}...")
        image = self._load_image(image_path)
        
        response = self.model.generate_content([
            image,
            """Extract card details as JSON:
            {
                "card_holder": "...",
                "card_type": "...",
                "expiry": "...",
                "issuer": "...",
                "last_4_digits": "...",
                "processing_timestamp": "..."
            }"""
        ])
        
        # Parse and cache result
        try:
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            result = json.loads(response.text[json_start:json_end])
        except:
            result = {"raw_response": response.text}
        
        result['processing_timestamp'] = datetime.now().isoformat()
        result['image_path'] = str(image_path)
        
        # Save to cache
        with open(cache_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✓ Cached result to {cache_file}")
        return result
    
    def batch_process(self, image_paths: List[str]):
        """Process multiple card images in batch"""
        results = []
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"\n[{i}/{len(image_paths)}] Processing: {image_path}")
            
            if not os.path.exists(image_path):
                results.append({
                    "image_path": image_path,
                    "status": "error",
                    "message": "File not found"
                })
                continue
            
            try:
                result = self.process_with_cache(image_path)
                result['status'] = 'success'
                results.append(result)
            except Exception as e:
                results.append({
                    "image_path": image_path,
                    "status": "error",
                    "message": str(e)
                })
        
        return results
    
    def compare_multiple_extractions(self, image_path, num_passes=3):
        """
        Extract same card multiple times to verify consistency
        Useful for validation and confidence scoring
        """
        extractions = []
        image = self._load_image(image_path)
        
        prompts = [
            "Extract: cardholder name, card type, expiry date. Return as JSON.",
            "What is the card holder's name, card type, and expiration date? JSON format.",
            "List all visible numbers and names on this card. JSON format."
        ]
        
        for i, prompt in enumerate(prompts[:num_passes], 1):
            print(f"Pass {i}/{num_passes}...")
            response = self.model.generate_content([image, prompt])
            
            try:
                json_start = response.text.find('{')
                json_end = response.text.rfind('}') + 1
                data = json.loads(response.text[json_start:json_end])
            except:
                data = {"raw_response": response.text}
            
            extractions.append(data)
        
        # Analyze consistency
        return {
            "extractions": extractions,
            "consistency_analysis": self._analyze_consistency(extractions)
        }
    
    def _analyze_consistency(self, extractions):
        """Analyze consistency across multiple extractions"""
        if not extractions:
            return {"status": "no_data"}
        
        # This is a simple example - in production, use more sophisticated comparison
        analysis = {
            "total_passes": len(extractions),
            "fields_analyzed": {},
            "consistency_score": 0
        }
        
        # Extract common fields
        all_keys = set()
        for ext in extractions:
            all_keys.update(ext.keys())
        
        matches = {}
        for key in all_keys:
            values = [str(ext.get(key, "")).lower() for ext in extractions]
            unique_values = set(v for v in values if v)
            matches[key] = {
                "unique_values": len(unique_values),
                "values": list(unique_values),
                "consistent": len(unique_values) == 1
            }
        
        analysis["fields_analyzed"] = matches
        
        # Calculate consistency score
        consistent_fields = sum(1 for m in matches.values() if m['consistent'])
        analysis["consistency_score"] = (consistent_fields / len(matches) * 100) if matches else 0
        
        return analysis
    
    def extract_and_validate(self, image_path, expected_holder=None):
        """Extract card details and validate against expected values"""
        image = self._load_image(image_path)
        
        prompt = f"""
        Extract card details as JSON. Include:
        - cardholder name
        - card type
        - last 4 digits
        - expiry
        - issuer
        - validity assessment (is it clearly readable?)
        {f'Expected cardholder: {expected_holder}' if expected_holder else ''}
        """
        
        response = self.model.generate_content([image, prompt])
        
        try:
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            extracted = json.loads(response.text[json_start:json_end])
        except:
            extracted = {"raw_response": response.text}
        
        # Validation
        validation_result = {
            "extracted_data": extracted,
            "validations": {}
        }
        
        if expected_holder and "cardholder" in extracted:
            validation_result["validations"]["holder_match"] = (
                expected_holder.lower() in str(extracted.get("cardholder", "")).lower()
            )
        
        validation_result["validations"]["has_expiry"] = "expiry" in extracted
        validation_result["validations"]["has_last_4"] = "last_4_digits" in extracted
        validation_result["validations"]["readable"] = extracted.get("validity", "").lower() in [
            "clear", "readable", "good", "high"
        ]
        
        return validation_result
    
    def clear_cache(self):
        """Clear all cached results"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir()
            print("✓ Cache cleared")


# ============================================================================
# EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("ADVANCED VISION AI CARD PROCESSING")
    print("="*70)
    
    try:
        processor = AdvancedCardProcessor()
        
        # Example 1: Single image with caching
        print("\n[1] Process with Caching")
        print("-" * 70)
        sample_image = "sample_card.jpg"
        if os.path.exists(sample_image):
            result = processor.process_with_cache(sample_image)
            print(json.dumps(result, indent=2))
        else:
            print(f"⚠ {sample_image} not found")
        
        # Example 2: Batch processing
        print("\n[2] Batch Process Multiple Cards")
        print("-" * 70)
        card_images = [
            "card1.jpg",
            "card2.jpg",
            "card3.jpg"
        ]
        existing_images = [img for img in card_images if os.path.exists(img)]
        
        if existing_images:
            batch_results = processor.batch_process(existing_images)
            print(f"Processed {len(batch_results)} images")
            for r in batch_results:
                print(f"  - {r.get('image_path', 'unknown')}: {r.get('status', 'unknown')}")
        else:
            print("⚠ No card images found for batch processing")
        
        # Example 3: Consistency check
        print("\n[3] Consistency Verification (Multiple Passes)")
        print("-" * 70)
        if os.path.exists(sample_image):
            consistency = processor.compare_multiple_extractions(sample_image, num_passes=2)
            print(f"Consistency Score: {consistency['consistency_analysis'].get('consistency_score', 0):.1f}%")
        
        # Example 4: Validation
        print("\n[4] Extract and Validate")
        print("-" * 70)
        if os.path.exists(sample_image):
            validation = processor.extract_and_validate(sample_image, expected_holder="JOHN DOE")
            print(json.dumps(validation, indent=2))
        
        print("\n" + "="*70)
        print("✓ All examples completed")
        print("="*70)
    
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
