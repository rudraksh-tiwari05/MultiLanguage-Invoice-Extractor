import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if the API key is retrieved correctly
api_key = os.getenv('GOOGLE_API_KEY')
print(f'API Key: {api_key}')  # Debug statement

if api_key is None:
    st.error('API key is missing. Please set the GOOGLE_API_KEY environment variable.')
else:
    try:
        # Initialize the generative AI model
        genai_model = genai.GenerativeModel(api_key=api_key)
    except Exception as e:
        st.error(f'Error initializing GenerativeModel: {e}')

    def input_image_setup(uploaded_file):
        ...

    def get_gemini_response(input_text, image_data, prompt):
        ...

    st.set_page_config(page_title='MultiLanguage Invoice Extractor')
    input_prompt = st.text_input('Input Prompt:', key='input')
    uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])
    image_data = None

    if uploaded_file is not None:
        ...
