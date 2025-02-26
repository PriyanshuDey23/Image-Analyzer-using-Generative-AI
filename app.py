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
    model = genai.GenerativeModel('gemini-2.0-flash')
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
import streamlit as st
from PIL import Image

# Set Streamlit page configuration
st.set_page_config(page_title="Image Analyzer", layout="wide")

# Page Header with Styling
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>📷 Image Analyzer</h1>", unsafe_allow_html=True)

# Create two columns: Left (Upload & Input) | Right (Response)
col1, col2 = st.columns([1, 1])

# Left Column: File Upload & Input
with col1:
    st.markdown("### 📤 Upload an Image")
    uploaded_file = st.file_uploader("Upload your image (JPEG, PNG)", type=["jpg", "jpeg", "png"])

    st.markdown("### 🔍 Describe what you want to know about the image")
    input_text = st.text_area("Enter your query here...", key="input", height=100)

    # Submit Button
    submit = st.button("Tell me About the Image", use_container_width=True)

# Right Column: Display Image & Response
with col2:
    if uploaded_file is not None:
        st.success("✅ File Uploaded Successfully!")
        if uploaded_file.type in ["image/jpeg", "image/png"]:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

    if submit:
        if uploaded_file is not None and input_text:
            with st.spinner("🔄 Processing your image..."):
                # Prepare image data for the model
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input=input_text, image_content=image_data, prompt=PROMPT)

            # Display response
            st.subheader("📝 Response:")
            st.write(response)
        else:
            st.warning("⚠️ Please upload an image and enter your query!")
