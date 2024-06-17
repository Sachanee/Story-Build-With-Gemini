from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(images, input_text):
    # Convert images to the format expected by the model
    formatted_images = [Image.open(img) for img in images]
    if input_text != "":
        response = model.generate_content([input_text] + formatted_images)
    else:
        response = model.generate_content(formatted_images)
    return response.text

st.set_page_config(page_title = "Story Telling")
st.header("Let's Build a Story with Gemini Application")

input = st.text_input("Input: ", key="input")

# Upload multiple images
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Display uploaded images
if uploaded_files:
    images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
    for img in images:
        st.image(img, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the image")

# If submit button is clicked
if submit:
    if uploaded_files:
        response = get_gemini_response(uploaded_files, input)
        st.subheader("Hey, Let's build an amazing Story together!!")
        st.write(response)
    else:
        st.error("Please upload at least one image.")