from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from speech_service import transcribe_audio
from scoring_service import evaluate_response
import openai
import os
import tempfile

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = 'your-api-key-here'

@app.route('/', methods=['GET'])
def home():
    user_data = {
        'sessionsCompleted': 0,
        'averageScore': None
    }
    return render_template('dashboard.component.html', userData=user_data)

@app.route('/practice', methods=['GET'])
def practice():
    return render_template('practice.html')

@app.route('/api/start-test', methods=['POST'])
def start_test():
    try:
        # Load topics from static file
        with open('static/topics.json') as f:
            topics = json.load(f)
        return jsonify({"status": "success", "topics": topics})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/submit-response', methods=['POST'])
def submit_response():
    try:
        if 'audio' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No audio file provided"
            }), 400
            
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No selected file"
            }), 400
        
        # First get the transcription
        transcription = transcribe_audio(audio_file)
        
        # Then get the detailed feedback
        feedback = generate_detailed_feedback(transcription)
        
        return jsonify({
            "status": "success",
            "feedback": feedback
        })
        
    except Exception as e:
        print("Error processing submission:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"status": "error", "message": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

def transcribe_audio(audio_file):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            # Write the audio data to the temporary file
            audio_file.save(tmp_file)
            tmp_file.flush()
            
            # Open and transcribe the temporary file
            with open(tmp_file.name, 'rb') as audio:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    response_format="text"
                )
            
            # Clean up the temporary file
            os.unlink(tmp_file.name)
            
        return transcript
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        raise

def generate_detailed_feedback(transcription):
    try:
        prompt = f"""
        As an IELTS speaking examiner, provide detailed feedback on the following response:
        
        "{transcription}"
        
        Provide specific feedback and a score (1-9) for each of these criteria:
        1. Fluency and Coherence: Evaluate speech flow, hesitation, repetition, and self-correction
        2. Pronunciation: Assess individual sounds, word stress, and sentence stress
        3. Grammar: Evaluate accuracy and range of grammatical structures
        4. Vocabulary: Assess range and accuracy of vocabulary use
        
        For each category, provide:
        - Specific examples from the response
        - Areas of strength
        - Areas for improvement
        - Practical tips for improvement
        - Score out of 9
        
        End with an overall band score.
        """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an experienced IELTS speaking examiner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Feedback generation error: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)#, ssl_context='adhoc')

