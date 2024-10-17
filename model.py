import os
import json
from langchain_groq import ChatGroq
from config import API_KEY, MODEL_NAME

def initialize_model():
    """Initialize the ChatGroq model."""
    os.environ['API_KEY'] = API_KEY
    model = ChatGroq(api_key=API_KEY, model=MODEL_NAME, temperature=0)
    return model

def extract_category(response: str) -> str:
    """Extract category from model's response, handling errors."""
    try:
        json_data = json.loads(response[response.find('{'):response.find('}')+1])
        return json_data.get('category', "Information Not Enough")
    except (json.JSONDecodeError, ValueError):
        return "Information Not Enough"

def invoke_model(prompt):
    """Invoke the model and return the response."""
    try:
        model = initialize_model()
        response = model.invoke(prompt).content
        return extract_category(response)
    except Exception as e:
        print(f"Error invoking model: {e}")
        return None
