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
        genai_model = genai.GenerativeModel()

        def input_image_setup(uploaded_file):
            # Your implementation for processing uploaded images
            pass

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
    except Exception as e:
        st.error(f'Error: {e}')


# Set the title of the app
st.set_page_config(page_title='Image Upload App')

# Create a file uploader widget for image files
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Check if an image is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Image uploaded successfully!")

    # Add your processing logic here
    # For example, you can perform image analysis or processing on 'image'

else:
    st.write("Please upload an image file.")

