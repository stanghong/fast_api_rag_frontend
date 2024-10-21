# %%
import streamlit as st
import requests
import logging
import numpy as np
# import soundfile as sf  # Commented out as it's causing an import error

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API_ENDPOINT = 'http://127.0.0.1:8000/api/combined_voicebot/'  # Replace with your FastAPI URL
API_ENDPOINT = 'https://fastapirag-production.up.railway.app/api/combined_voicebot/'

# Initialize session state for recording
if 'audio_buffer' not in st.session_state:
    st.session_state.audio_buffer = None

# Streamlit interface
st.title("Combined Voicebot with PDF QA")

# PDF file uploader
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Option to record audio or enter text manually
audio_option = st.radio("Choose input method:", ("Record Audio", "Type Text"))

# Function to record audio using streamlit-webrtc
def record_audio_with_webrtc():
    st.warning("Audio recording functionality is currently unavailable. Please use the 'Type Text' option instead.")

# Record audio if selected
if audio_option == "Record Audio":
    st.header("Record Audio")
    st.warning("Audio recording functionality is currently unavailable. Please use the 'Type Text' option instead.")

elif audio_option == "Type Text":
    text_input = st.text_area("Enter your text here")

# Submit button for processing the PDF and audio or text
if st.button("Submit"):
    if pdf_file:
        with st.spinner("Processing..."):
            try:
                files = {'pdf': pdf_file}
                data = {}

                if audio_option == "Record Audio":
                    st.warning("Audio recording is currently unavailable. Please use the 'Type Text' option.")
                    st.stop()
                elif audio_option == "Type Text" and text_input:
                    data = {"text": text_input}
                    logger.info("Text input added to the request.")
                else:
                    st.warning("Please provide text input.")
                    st.stop()

                response = requests.post(API_ENDPOINT, files=files, data=data, timeout=60)
                response.raise_for_status()

                response_data = response.json()
                response_text = response_data.get("return_text", "No response text.")
                audio_url = response_data.get("output_wav_url")

                # Display the response
                st.success("Processing completed!")
                st.write("Response Text:", response_text)

                # Play the audio if available
                if audio_url:
                    st.audio(audio_url, format="audio/mp3")
                    st.markdown(f"[Download Audio]({audio_url})", unsafe_allow_html=True)
                    logger.info("Audio response received and displayed.")
                else:
                    st.warning("No audio output was generated.")

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                st.error(f"Failed to process the request: {e}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please upload a PDF file first.")

# Provide instructions for use
st.markdown("""
### Instructions:
1. Upload a PDF file that you want to analyze.
2. Choose the 'Type Text' option for your question.
3. Enter your question in the text area provided.
4. Click 'Submit' to process your input and get a response.
5. If an audio response is generated, you can play it directly or download it.
""")
