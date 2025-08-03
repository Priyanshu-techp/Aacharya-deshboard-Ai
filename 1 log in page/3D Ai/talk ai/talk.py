from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

# ✅ Gemini API Config
GEMINI_API_KEY = "AIzaSyCqpK4AssbLK6EfFr6lBlGGMAa9nkvD-cY"  # Replace with your actual key
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

def get_gemini_reply(user_query):
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "parts": [{"text": user_query}]
                }
            ]
        }

        start = time.time()
        res = requests.post(GEMINI_URL, headers=headers, json=data)
        duration = time.time() - start
        print(f"✅ Gemini response time: {duration:.2f}s")

        if res.status_code == 200:
            reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            return reply
        else:
            print("❌ Gemini Error:", res.text)
            return "Sorry, I couldn't process your message at the moment."

    except Exception as e:
        print("❌ Exception:", str(e))
        return "An error occurred while contacting Gemini AI."

@app.route('/api/health-query', methods=['POST'])
def handle_query():
    data = request.get_json()
    user_query = data.get("query", "").strip()

    if not user_query or len(user_query) < 2:
        return jsonify({'status': 'error', 'message': 'Query too short'}), 400

    reply = get_gemini_reply(user_query)
    return jsonify({
        'status': 'success',
        'data': {
            'title': "Acharya:",
            'content': reply,
            'source': "Source: Aacharya AI (via Gemini)"
        }
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)
