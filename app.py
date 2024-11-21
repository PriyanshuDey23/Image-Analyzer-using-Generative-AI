from dotenv import load_dotenv
import google.generativeai as genai
import os
import streamlit as st
from PIL import Image


# Import from prompt.py
from prompt import *


# Load environment variables from .env file
load_dotenv()

# Set up the API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get a response from the Gemini model
def get_gemini_response(input,image_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash-8b')
    if input!="":
        response = model.generate_content([input, image_content[0], prompt])
    else:
        response=model.generate_content(image_content)
    return response.text



# Function to convert image to bytes(The function reads the uploaded file, converts it into bytes, )
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        image_bytes = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": image_bytes}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# Initialize the Streamlit app
st.set_page_config(page_title="Image Analyzer")
st.header("Image Analyzer")

# Input Prompt for the user
input_text = st.text_area("What do you want to know about the image", key="input")

# File uploader for images and PDFs
uploaded_file = st.file_uploader("Upload your image...", type=["jpg", "jpeg", "png"])


# Initialize variable for storing image  content
image = None

if uploaded_file is not None:
    st.write("File Uploaded Successfully")
    if uploaded_file.type in ["image/jpeg", "image/png"]:
        image = Image.open(uploaded_file)
        # Display the imge
        st.image(image, caption="Uploaded Image", use_column_width=True)
        content_text = "Image content displayed."


# Button to trigger processing and generate response
submit=st.button("Tell me About the Image")


# Submit
if submit:
    if uploaded_file is not None and input_text:
        # Prepare image data for the model
        image_data = input_image_setup(uploaded_file)
        response=get_gemini_response(input=input_text,image_content=image_data,prompt=PROMPT)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload Image")