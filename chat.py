from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai
from waitress import serve

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Setup Gemini
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

# Flask setup
app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('chat.html')

# API route
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    if question:
        response_chunks = chat.send_message(question, stream=True)
        full_response = "".join([chunk.text for chunk in response_chunks])
        return jsonify({'response': full_response})
    return jsonify({'error': 'No question provided'}), 400

# ✅ Correct way to run with Waitress
if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=8080)
