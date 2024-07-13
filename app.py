import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the Google API key
GOOGLE_API_KEY = "AIzaSyBAvNAAXJOJ-RU6q1mi5LKUB31zz0b9tow"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro-vision')

# Set up the Streamlit app
st.title("Invoice Analyzer")
st.write("Upload an invoice image and ask a question about it.")

# Initialize session state for the question input
if 'question' not in st.session_state:
    st.session_state.question = ''

# Upload the image
uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Invoice', use_column_width=True)
    
    # Input prompt for the question
    st.session_state.question = st.text_input("Enter your question about the invoice:", st.session_state.question)
    
    # Add buttons for analyzing and clearing the input field
    col1, col2 = st.columns(2)
    
    with col1:
        analyze = st.button("Analyze Invoice")
    with col2:
        clear = st.button("Clear Input")
    
    if analyze:
        # Prepare the input prompt
        input_prompt = '''
        You are an expert in understanding invoices. We will upload a simple image as an invoice and you will have to
        answer any question based on the uploaded invoice image.
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

# Run the Streamlit app

