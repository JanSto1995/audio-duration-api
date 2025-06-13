from flask import Flask, request, jsonify
import librosa
import os
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return '🎵 Duration API is running.'

@app.route('/duration', methods=['POST'])
def get_duration():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = file.filename
    filepath = os.path.join('/tmp', filename)
    file.save(filepath)

    try:
        # Load audio file using librosa
        y, sr = librosa.load(filepath, sr=44100)
        duration = librosa.get_duration(y=y, sr=sr)

        return jsonify({
            'filename': filename,
            'duration_seconds': round(duration, 2)
        })
    except Exception as e:
        # Log error in Render logs
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
