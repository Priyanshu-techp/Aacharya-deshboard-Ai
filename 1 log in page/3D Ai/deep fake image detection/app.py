from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import requests
import os

app = Flask(__name__)
CORS(app)

# Gemini API Key and URL
GEMINI_API_KEY = "AIzaSyCqpK4AssbLK6EfFr6lBlGGMAa9nkvD-cY"
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = file.filename
    ext = filename.split('.')[-1].lower()
    file_type = "image" if ext in ["jpg", "jpeg", "png"] else "video"

    file_data = base64.b64encode(file.read()).decode("utf-8")

    if file_type == "image":
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "inline_data": {
                                "mime_type": f"image/{ext}",
                                "data": file_data
                            }
                        },
                        {
                            "text": "This is a real image of a person taken in normal conditions. Is this image digitally manipulated or AI-generated? Only reply with: real or fake."
                        }
                    ]
                }
            ]
        }
    else:
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"This is a video in base64 format. Is it real or fake? Answer only: real or fake.\n{file_data[:1000]}..."
                        }
                    ]
                }
            ]
        }

    try:
        response = requests.post(GEMINI_API_URL, json=data)
        response.raise_for_status()
        result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip().lower()
        result = "real" if "real" in result_text else "fake"
    except Exception as e:
        print("API response error:", e)
        result = "error"

    return jsonify({
        "result": result,
        "type": file_type
    })

if __name__ == '__main__':
    print("Fake Image/Video Detector running on http://127.0.0.1:5004")
    app.run(debug=True, port=5004)
