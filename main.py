import streamlit as st
import tiktoken
import json
import time
from scrape_text import scrapper
from model import invoke_model
from prompt import generate_prompt

# Set the title of the Streamlit app
st.title('Website Categorizer')

# Function to calculate token count
def num_tokens_from_string(text: str, encoding_name='cl100k_base') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

# Function to read a text file (not used in the web app but kept for reference)
def read_txt_file(text_file_path: str) -> str:
    """Read the text from a file."""
    with open(text_file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Main function to categorize websites based on their content
def categorize_websites(url):
    """Main function to categorize websites by analyzing their content."""
    html_code = scrapper(url)


    # Generate prompt
    prompt = generate_prompt(url, html_code)
    # Adjust prompt if token count exceeds the limit
    if num_tokens_from_string(prompt) > 8000:
        html_code = html_code[:32000]
        prompt = generate_prompt(url, html_code)
    
    # Invoke model and handle exceptions
    response = invoke_model(prompt)
    if response:
        return response
    else:
        time.sleep(60)
        response = invoke_model(prompt)
        return response

# # Example usage
# if __name__ == "__main__":
#     url = "amazon.com"
#     category = categorize_websites(url)
#     print(f"Merchant Categorized is {category}")

# Streamlit interface
st.write("Enter a URL to categorize the website's content:")

# Input field for user to input URL
url_input = st.text_input("URL")

# Button to trigger the categorization
if st.button('Categorize'):
    if url_input:
        with st.spinner('Categorizing website...'):
            category = categorize_websites(url_input)
        st.success(f"Website categorized as: {category}")
