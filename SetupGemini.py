import os
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

genai.configure(api_key=api_key)

# Initialize models
print("Loading Gemini model...")
model = genai.GenerativeModel("gemini-1.5-flash")

print("Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Test function
def test_gemini_setup():
    """Test that Gemini API is properly configured and working."""
    try:
        response = model.generate_content("Say 'Hello from Gemini!'")
        print("✓ Gemini API test passed:")
        print(f"  Response: {response.text}")
        return True
    except Exception as e:
        print(f"✗ Gemini API test failed: {e}")
        return False

def test_embedding_setup():
    """Test that embedding model is properly loaded and working."""
    try:
        test_text = "This is a test sentence."
        embedding = embedding_model.encode(test_text)
        print(f"✓ Embedding model test passed:")
        print(f"  Embedding dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"✗ Embedding model test failed: {e}")
        return False

# Run tests if script is executed directly
if __name__ == "__main__":
    print("Testing SetupGemini configuration...\n")
    test_gemini_setup()
    print()
    test_embedding_setup()
    print("\n✓ All setup tests completed!")