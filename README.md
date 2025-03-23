# Audio Transcription App

A web application that extracts text from audio files using Python speech recognition on the backend and a responsive web interface for the frontend.

## Features

- 🎤 Convert speech from audio files (.wav, .mp3, .ogg, .flac, .m4a) to text
- 📱 Responsive web interface for easy file uploads
- 🖱️ Drag-and-drop interface for a smooth user experience
- 📋 One-click copy of transcription results to clipboard
- 🚀 Simple setup and installation process

## Demo

![Demo of Audio Transcription App](https://via.placeholder.com/800x400?text=Audio+Transcription+App+Demo)

## Technology Stack

- **Backend**: Python with Flask, SpeechRecognition, and pydub
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Speech Recognition**: Google Speech Recognition API (free tier)

## Installation

### Prerequisites

- Python 3.7+
- Web browser (Chrome, Firefox, Safari, etc.)
- Internet connection (for the Google Speech API)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio-transcription-app.git
cd audio-transcription-app
```

2. Set up a Python virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install the required Python packages:
```bash
pip install -r requirements.txt
```

5. Additional system dependencies:
   - For PyAudio (which may be needed for some audio processing):
     - Windows: PyAudio wheel will be installed automatically
     - macOS: `brew install portaudio`
     - Linux: `sudo apt-get install python3-pyaudio`

## Usage

1. Start the backend server:
```bash
cd backend
python app.py
```

2. Open the frontend:
   - Simply open `frontend/index.html` in your web browser
   - Alternatively, you can serve it using a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Then navigate to `http://localhost:8000` in your browser.

3. Use the application:
   - Drag and drop an audio file onto the upload area, or click "Browse Files"
   - Select a supported audio file (.wav, .mp3, .ogg, .flac, .m4a)
   - Click "Transcribe Audio"
   - View the transcription results
   - Use the "Copy to Clipboard" button to copy the text

## Project Structure

```
audio-transcription-app/
├── backend/
│   ├── app.py           # Flask server and speech recognition logic
│   └── requirements.txt # Python dependencies
├── frontend/
│   └── index.html       # Web interface (HTML, CSS, JS)
└── README.md            # This file
```

## API Endpoints

The backend server exposes the following API endpoint:

- **POST /transcribe**
  - Accepts multipart form data with an audio file
  - Returns JSON with the transcription result

## Limitations

- Maximum file size: 16MB
- Uses Google's free Speech Recognition API, which has usage limits
- Currently supports only the languages available in the Google Speech API
- Not optimized for very long audio files (>10 minutes)

## Future Enhancements

- [ ] Support for longer audio files through chunking
- [ ] Real-time transcription from microphone
- [ ] Multiple language support
- [ ] Export options (TXT, PDF, DOCX)
- [ ] User accounts and transcription history
- [ ] Progress indicator for transcription process
- [ ] Advanced audio processing (noise reduction, speaker diarization)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Python library for performing speech recognition
- [Flask](https://flask.palletsprojects.com/) - Web framework for Python
- [pydub](https://github.com/jiaaro/pydub) - Audio file manipulation library