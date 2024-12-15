import base64
import io
import re 
from groq import Groq
from PIL import Image
import requests
import json
from config import API_KEY, MODEL_NAME
import time


def extract_category(response: str) -> str:
    """Extract category from model's response, handling errors."""
    try:
        json_data = json.loads(response[response.find('{'):response.find('}')+1])
        return json_data.get('category', "Information Not Enough")
    except (json.JSONDecodeError, ValueError):
        return "Information Not Enough"
    

def encode_image(image_path):
    """
    Encode the image for Vision model input
    Input : Image path 
    Output: Image in base64 format
    """
    with open(image_path, "rb") as image_file:  # Open the image file in binary mode
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def invoke_model(image, prompt,api_key =API_KEY,model_name= MODEL_NAME):
    client = Groq(api_key=api_key)

    base64_image = encode_image(image)
    image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        image_content,
                    ],
                }
            ],
            model=model_name, response_format={"type": "json_object"}
        )
        return extract_category(chat_completion.choices[0].message.content)
    except Exception as e:
        error_string = str(e)
        if "429" in error_string:
            error = error_string.split("Please try again")[-1]
            match = re.search(r'(\d+)m(\d+\.\d+)s', error)

            if match:
                minutes = int(match.group(1))
                seconds = float(match.group(2))
                
                # Convert to total seconds
                total_seconds = minutes * 60 + seconds
                time.sleep(total_seconds)
                return invoke_model(image, prompt)
        elif "400" in error_string:
            chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                    model="llama-3.1-8b-instant"
                )
            return extract_category(chat_completion.choices[0].message.content)
        elif "413" in error_string:
            return "Decrease the content size to long for processing"
        else:
            return e 

def invoke_model_w_31(prompt,api_key =API_KEY,model_name= "llama-3.1-8b-instant"):
    client = Groq(api_key=api_key)
    chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                    model="llama-3.1-8b-instant"
                )
    return extract_category(chat_completion.choices[0].message.content)

# def invoke_model_wo_json(image, prompt,api_key =API_KEY,model_name= MODEL_NAME):
#     client = Groq(api_key=api_key)

#     base64_image = encode_image(image)
#     image_content = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         image_content,
#                     ],
#                 }
#             ],
#             model=model_name
#         )
#         return extract_category(chat_completion.choices[0].message.content)
#     except Exception as e:
#         return f"Error: {str(e)}"