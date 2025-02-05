import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from flask import Flask, render_template, request, jsonify
import whisper
import os
import uuid

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("tiny")

# Directory to save uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}_{audio_file.filename}"
    audio_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    audio_file.save(audio_path)

    # Transcribe the audio file
    result = model.transcribe(audio_path)
    transcription = result["text"]

    # Clean up the uploaded file
    os.remove(audio_path)

    return jsonify({"transcription": transcription})

if __name__ == '__main__':
    app.run(debug=True, port=5500)