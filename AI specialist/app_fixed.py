
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from speech_service import transcribe_audio
from scoring_service import evaluate_response

app = Flask(__name__)
CORS(app)

@app.route('/api/start-test', methods=['POST'])
def start_test():
    # Load topics from static file
    with open('static/topics.json') as f:
        topics = json.load(f)
    return jsonify({"status": "success", "topics": topics})

@app.route('/api/submit-response', methods=['POST'])
def submit_response():
    audio_data = request.files['audio']
    transcription = transcribe_audio(audio_data)
    feedback = evaluate_response(transcription)
    return jsonify(feedback)

if __name__ == '__main__':
    app.run(debug=True)
