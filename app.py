import load_dotenv
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure the generative AI API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

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

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel(api_key=os.getenv('GOOGLE_API_KEY'))
    response = model.generate_content([input, image[0], prompt])
    return response.text

st.set_page_config(page_title='MultiLanguage Invoice Extractor')
input_prompt = st.text_input('Input Prompt:', key='input')
uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])
image = ''
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button('Tell me about the invoice')

default_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice and
you will have to answer any question based on the uploaded invoice image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(default_prompt, image_data, input_prompt)
    st.subheader('The Response Is')
    st.write(response)
