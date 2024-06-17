from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


genai.configure(api_key= os.getenv('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-pro-vision')


st.set_page_config(page_title = "Story Telling")


page = st.sidebar.selectbox(
    "Select a Solution",
    [
        "Image-to-text Generation with GEmini AI",
        "Chatbot"      
    ],
)


if page ==  "Image-to-text Generation with GEmini AI":

    st.markdown("<h1 style='text-align: center;'>Let's Build a Story with Gemini Application</h1>", unsafe_allow_html=True)

    image_path = "ui-image.jpg"
    # Display the image with alignment to the middle
    st.image(image_path, 
         clamp=False, 
         channels="RGB", 
         output_format="auto", 
         use_column_width=True,
         caption='Image aligned to the middle'
)

    def get_gemini_response(images, input_text):
        # Convert images to the format expected by the model
        formatted_images = [Image.open(img) for img in images]
        if input_text != "":
            response = model.generate_content([input_text] + formatted_images)
        else:
            response = model.generate_content(formatted_images)
        return response.text

    input = st.text_input("Please explain your requirements. For example, specify if you need features like word count or if you prefer to leave this field empty.: ", key="input")

    # Upload multiple images
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # Display uploaded images
    if uploaded_files:
        images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
        for img in images:
            st.image(img, caption="Uploaded Image", use_column_width=True)

    submit = st.button("Build a creative story")

    # If submit button is clicked
    if submit:
        if uploaded_files:
            response = get_gemini_response(uploaded_files, input)
            st.subheader("Hey, Let's build an amazing Story together!!")
            st.write(response)
        else:
            st.error("Please upload at least one image.")

else:
    st.markdown("<h1 style='text-align: center;'>Chatbot</h1>", unsafe_allow_html=True)

    # Display chat UI image
    image_path = "bot.png"
    st.image(image_path,
             clamp=False,
             channels="RGB",
             output_format="auto",
             use_column_width=True,
             caption='Image aligned to the middle')

    model = genai.GenerativeModel('gemini-pro')

    # Start chat session
    chat = model.start_chat(history=[])

    # Function to send question to Gemini AI chat
    def gemini_response(question):
        response = chat.send_message(question, stream=True)
        return response

    # Initialize chat history in session state if not already present
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Text input for user to start chat
    input_text = st.text_input('Start your chat here:', key="chat_input")
    submit = st.button("Ask the Question")

    # Handle submit action
    if submit and input_text:
        response = gemini_response(input_text)
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader('The response is')

        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    # Display chat history
    st.subheader("The chat history is")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
 