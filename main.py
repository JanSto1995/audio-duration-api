from flask import Flask, request, jsonify
import librosa
import os

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
        y, sr = librosa.load(filepath)
        duration = librosa.get_duration(y=y, sr=sr)
        return jsonify({
            'filename': filename,
            'duration_seconds': round(duration, 2)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
