from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import io
import pytesseract

# Load environment variables from a .env file
load_dotenv()

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.getvalue()
    else:
        raise FileNotFoundError('No File Uploaded')

def extract_text_from_image(image):
    image_bytes = input_image_setup(image)
    image = Image.open(io.BytesIO(image_bytes))
    
    # Use pytesseract to perform OCR on the image
    text = pytesseract.image_to_string(image)
    return text

def get_gemini_response(input_text, prompt):
    # Call your generative model here with input_text and prompt
    # For example:
    # model_response = my_generative_model(input_text, prompt)
    # return model_response
    return f"Input Text: {input_text}, Prompt: {prompt}"  # Placeholder for model response

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
        image_text = extract_text_from_image(uploaded_file)
        response = get_gemini_response(image_text, input_prompt or default_prompt)
        st.subheader('The Response Is')
        st.write(response)
