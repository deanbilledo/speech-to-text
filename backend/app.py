import speech_recognition as sr
from pydub import AudioSegment
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Enable CORS for all routes with additional options
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_wav(file_path):
    """Convert audio file to WAV format for processing"""
    logger.debug(f"Converting file: {file_path}")
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found for conversion: {file_path}")
            raise FileNotFoundError(f"Input file not found: {file_path}")
            
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path + ".wav"
        audio.export(wav_path, format="wav")
        logger.debug(f"Successfully converted to: {wav_path}")
        return wav_path
    except Exception as e:
        logger.error(f"Error converting audio file: {str(e)}")
        raise

def transcribe_audio(file_path):
    """Transcribe audio file to text"""
    logger.debug(f"Starting transcription of: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found for transcription: {file_path}")
        return "Error: Audio file not found"
    
    # Convert to WAV if not already in that format
    wav_path = file_path
    if not file_path.lower().endswith('.wav'):
        try:
            wav_path = convert_to_wav(file_path)
        except Exception as e:
            logger.error(f"Failed to convert audio: {str(e)}")
            return f"Error converting audio: {str(e)}"
    
    # Check if the WAV file exists
    if not os.path.exists(wav_path):
        logger.error(f"WAV file not found: {wav_path}")
        return "Error: WAV file not found after conversion"
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(wav_path) as source:
            # Record audio from file
            audio_data = recognizer.record(source)
            
            try:
                # Use Google's speech recognition (free API)
                text = recognizer.recognize_google(audio_data)
                logger.debug("Transcription successful")
                return text
            except sr.UnknownValueError:
                logger.warning("Speech Recognition could not understand the audio")
                return "Speech Recognition could not understand the audio"
            except sr.RequestError as e:
                logger.error(f"Request error: {str(e)}")
                return f"Could not request results from Speech Recognition service; {e}"
    except Exception as e:
        logger.error(f"Error during audio processing: {str(e)}")
        return f"Error processing audio: {str(e)}"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Server is running. Use the HTML interface to upload files."})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "Connection successful"})

@app.route('/transcribe', methods=['POST', 'OPTIONS'])
def transcribe():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    # Check if a file was included in the request
    if 'file' not in request.files:
        logger.warning("No file part in request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        logger.warning("No file selected")
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        logger.debug(f"Saving file to: {file_path}")
        file.save(file_path)
        
        # Verify file was saved
        if not os.path.exists(file_path):
            logger.error(f"File not saved successfully: {file_path}")
            return jsonify({'error': 'Failed to save uploaded file'}), 500
        
        # Transcribe the audio file
        transcription = transcribe_audio(file_path)
        
        # Clean up temporary files
        try:
            logger.debug(f"Cleaning up files. Original: {file_path}")
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.debug(f"Removed original file: {file_path}")
                
            wav_path = file_path + ".wav"
            logger.debug(f"Checking for WAV file: {wav_path}")
            if os.path.exists(wav_path):
                os.remove(wav_path)
                logger.debug(f"Removed WAV file: {wav_path}")
        except Exception as e:
            logger.error(f"Failed to clean up files: {str(e)}")
        
        return jsonify({'transcription': transcription})
    
    logger.warning(f"File type not allowed: {file.filename}")
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    print("Server starting on http://localhost:5000")
    logger.info("Server starting on http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')