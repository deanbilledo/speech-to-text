import speech_recognition as sr
from pydub import AudioSegment
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_wav(file_path):
    """Convert audio file to WAV format for processing"""
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_audio(file_path):
    """Transcribe audio file to text"""
    # Convert to WAV if not already in that format
    if not file_path.lower().endswith('.wav'):
        file_path = convert_to_wav(file_path)
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file_path) as source:
        # Record audio from file
        audio_data = recognizer.record(source)
        
        try:
            # Use Google's speech recognition (free API)
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Speech Recognition service; {e}"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Check if a file was included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Transcribe the audio file
        transcription = transcribe_audio(file_path)
        
        # Clean up temporary files
        try:
            os.remove(file_path)
            if os.path.exists(file_path + ".wav"):
                os.remove(file_path + ".wav")
        except:
            pass
        
        return jsonify({'transcription': transcription})
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)