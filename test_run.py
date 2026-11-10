import os
from google import genai

client = genai.Client()

print("Testing Gemini connection...")
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Hello! Confirm that you are online and ready to build the BidAgent."
)

print("\n--- AI Response ---")
print(response.text)