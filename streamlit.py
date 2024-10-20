import streamlit as st
import pyaudio
import wave
import io
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API_ENDPOINT = 'http://127.0.0.1:8000/api/combined_voicebot/'  # Replace with your FastAPI URL
API_ENDPOINT =  'https://fastapirag-production.up.railway.app/api/combined_voicebot/'
# Initialize session state for recording
if 'audio_buffer' not in st.session_state:
    st.session_state.audio_buffer = None

# Audio recording parameters
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second

# Input for recording duration
seconds = st.number_input("Recording duration (seconds):", min_value=1, max_value=60, value=3, step=1)

# Streamlit interface
st.title("Combined Voicebot with PDF QA")

# PDF file uploader
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Option to record audio or enter text manually
audio_option = st.radio("Choose input method:", ("Record Audio", "Type Text"))

# Function to record audio
def record_audio():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
    except Exception as e:
        st.error(f"Could not open microphone: {e}")
        return

    frames = []

    st.write("Recording...")
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    st.write("Recording complete.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file in memory
    buffer = io.BytesIO()
    wf = wave.open(buffer, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    buffer.seek(0)

    st.session_state.audio_buffer = buffer

# Record audio if selected
if audio_option == "Record Audio":
    st.header("Record Audio")
    if st.button("Start Recording"):
        record_audio()

    # Playback the recorded audio if available
    if st.session_state.audio_buffer:
        st.audio(st.session_state.audio_buffer.getvalue(), format='audio/wav')
        st.download_button(
            label="Download recorded audio",
            data=st.session_state.audio_buffer,
            file_name="recorded_audio.wav",
            mime="audio/wav"
        )

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
                    audio_buffer = st.session_state.get('audio_buffer', None)
                    if audio_buffer and audio_buffer.getbuffer().nbytes > 0:
                        audio_buffer.seek(0)
                        files['audio'] = ("audio.wav", audio_buffer, "audio/wav")
                        logger.info("Audio file added to the request.")
                    else:
                        st.warning("No audio recorded. Please record your question.")
                        st.stop()
                elif audio_option == "Type Text" and text_input:
                    data = {"text": text_input}
                    logger.info("Text input added to the request.")
                else:
                    st.warning("Please provide either audio input or text input.")
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
2. Choose between recording audio or typing text for your question.
3. If recording audio, click 'Start Recording' to start and stop recording.
4. Click 'Submit' to process your input and get a response.
5. If an audio response is generated, you can play it directly or download it.
""")
