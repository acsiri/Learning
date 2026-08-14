import os
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from google import genai

# Initialize Gemini client
#client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client = genai.Client(api_key="AIzaSyDiB0cBwVeG_cXUwW5ecOjTWfOpQ2AOFiM")

app = FastAPI()

# Enable CORS for HTML access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "OK"}


@app.post("/ocr")
async def extract_text(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))


    prompt = """
      You are an Credit card , Debit Card , master card, visa card and document image reading and understanding system.
      Extract all readable text from this image. 
      Do not mask any digits. 
      Ensure card number is not having any alphabets and is in the format of 16 digits in a row.
      Preserve line breaks and formatting. 
      Get Trained to read cards in various formats and layouts.
      provide details in JSON FORMAT
      WHICH CONSISTS OF 
      card_vendor
      card_holder_name 
      card_number
      expiry_date
      validity
      """
  

 

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )
    return {"text": response.text}