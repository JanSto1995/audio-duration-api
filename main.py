from flask import Flask, request, jsonify
import soundfile as sf
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
        # Use soundfile to load only metadata
        f = sf.SoundFile(filepath)
        duration = len(f) / f.samplerate

        return jsonify({
            'filename': filename,
            'duration_seconds': round(duration, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
