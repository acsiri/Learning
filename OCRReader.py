
import os
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)

    print(client.models.list())
    
    prompt = (
       "Extract all readable text from this image. "
        "Preserve line breaks and formatting. "
        "provide details in JSON FORMAT" 
        "WHICH CONSISTS OF "
        "card_vendor" 
        "card_holder_name" 
        "card_number" 
        "expiry_date" 
        "validity"
       # "Do not summarize."
       #" If there are 16 digits in a row, read them as [CCNUMBER] prefixed"
       #"Extract only the expiration date if they are in the format MM/YY or MM/YYYY and prefix them with [EXPDATE]"
    )
    
 

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    return response.text


if __name__ == "__main__":
    print(extract_text_from_image("sample.jpg"))
