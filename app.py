import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai
from io import BytesIO

# Configure the Google API key
GOOGLE_API_KEY = "AIzaSyBAvNAAXJOJ-RU6q1mi5LKUB31zz0b9tow"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')

# Function to extract the first page of a PDF as an image
def extract_image_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = doc.load_page(0)  # Load the first page
    pix = page.get_pixmap()
    img_bytes = pix.tobytes("png")
    img = Image.open(BytesIO(img_bytes))
    return img

# Set up the Streamlit app
st.title("Document Query")
st.write("Upload an image or PDF and ask a question about it.")

# Initialize session state for the question input
if 'question' not in st.session_state:
    st.session_state.question = ''

# Upload the file
uploaded_file = st.file_uploader("Choose an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.type
    
    if file_type == "application/pdf":
        img = extract_image_from_pdf(uploaded_file)
    else:
        img = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(img, caption='Uploaded', use_column_width=True)
    
    # Input prompt for the question
    st.session_state.question = st.text_input("Enter your question:", st.session_state.question)
    
    # Add buttons for analyzing and clearing the input field
    col1, col2 = st.columns(2)
    
    with col1:
        analyze = st.button("Submit")
    with col2:
        clear = st.button("Clear Input")
    
    if analyze:
        # Prepare the input prompt
        input_prompt = '''
        You are an expert in understanding images and pdf. We will upload a  image or pdf and you will have to
        answer any question based on the uploaded image or pdf.

        if you dont find question relevant say "sorry please ask relavant question!"
        or you don't find answer or nable to generate relevnt content say "sorry unable to find "
        '''
        
        # Generate the response from the AI model
        response = model.generate_content([input_prompt, img, st.session_state.question], stream=True)
        response.resolve()
        
        # Display the response
        st.write("Response:", response.text)
    
    if clear:
        # Clear the input field
        st.session_state.question = ''
        st.experimental_rerun()

