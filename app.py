from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pytesseract
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error('API key not found. Please set the GOOGLE_API_KEY environment variable.')
    st.stop()

genai.configure(api_key=api_key)

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No File Uploaded')

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def get_gemini_response(input_text, prompt):
    try:
        model = genai.GenerativeModel()
        response = model.generate_content([input_text, prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

st.set_page_config(page_title='MultiLanguage Invoice Extractor')
input_prompt = st.text_input('Input Prompt:', key='input')
uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button('Tell me about the invoice')

default_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice and
you will have to answer any question based on the uploaded invoice image.
"""

if submit:
    if uploaded_file is None:
        st.error('Please upload an image file.')
    else:
        image_text = extract_text_from_image(image)
        response = get_gemini_response(image_text, input_prompt or default_prompt)
        st.subheader('The Response Is')
        st.write(response)
