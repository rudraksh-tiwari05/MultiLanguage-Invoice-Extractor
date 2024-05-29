import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if the API key is retrieved correctly
api_key = os.getenv('GOOGLE_API_KEY')
if api_key is None:
    st.error('API key is missing. Please set the GOOGLE_API_KEY environment variable.')
else:
    # Initialize the generative AI model
    genai_model = genai.GenerativeModel(api_key=api_key)

    def input_image_setup(uploaded_file):
        if uploaded_file is not None:
            # Check if the uploaded file is an image
            if uploaded_file.type.startswith('image'):
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
                raise ValueError('Uploaded file is not an image.')
        else:
            raise FileNotFoundError('No File Uploaded')

    def get_gemini_response(input_text, image_data, prompt):
        # Generate content using the generative AI model
        response = genai_model.generate_content([input_text, image_data[0], prompt])
        return response.text

    st.set_page_config(page_title='MultiLanguage Invoice Extractor')
    input_prompt = st.text_input('Input Prompt:', key='input')
    uploaded_file = st.file_uploader('Choose an image of the invoice...', type=['jpg', 'jpeg', 'png'])
    image_data = None

    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        submit = st.button('Tell me about the invoice')

        default_prompt = """
        You are an expert in understanding invoices. We will upload an image of an invoice and
        you will have to answer any question based on the uploaded invoice image.
        """

        if submit:
            if image_data is None:
                st.error('Please upload an image file.')
            else:
                response = get_gemini_response(default_prompt, image_data, input_prompt)
                st.subheader('The Response Is')
                st.write(response)
