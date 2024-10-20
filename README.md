# Combined Voicebot with PDF QA - Frontend

This is the frontend application for the Combined Voicebot with PDF QA system. It provides a user-friendly interface for interacting with the voicebot and PDF question-answering system.

## GitHub Repository

[https://github.com/stanghong/fast_api_rag_frontend.git](https://github.com/stanghong/fast_api_rag_frontend.git)

## Features

- PDF file upload
- Audio recording for voice input
- Text input option
- Audio playback of responses
- Download options for recorded audio and responses

## Technologies Used

- Streamlit
- PyAudio
- Requests

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/stanghong/fast_api_rag_frontend.git
   ```

2. Navigate to the project directory:
   ```
   cd fast_api_rag_frontend
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```
   streamlit run streamlit.py
   ```

## Usage

1. Upload a PDF file that you want to analyze.
2. Choose between recording audio or typing text for your question.
3. If recording audio, click 'Start Recording' to start and stop recording.
4. Click 'Submit' to process your input and get a response.
5. If an audio response is generated, you can play it directly or download it.

## API Configuration

The application is configured to use the following API endpoint:

## Logging

The application uses Python's built-in logging module. Logs are output at the INFO level by default.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
