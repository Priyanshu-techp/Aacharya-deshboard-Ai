from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import time
import traceback

app = Flask(__name__)
CORS(app)

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyCqpK4AssbLK6EfFr6lBlGGMAa9nkvD-cY"
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

def get_health_info(query):
    try:
        start_time = time.time()
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "parts": [{"text": f"You are a professional health assistant. Answer in clear, helpful and friendly tone. The user asks: {query}"}]
                }
            ]
        }

        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)
        if response.status_code == 200:
            result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            print(f"AI responded in {time.time() - start_time:.2f}s")
            return {
                'title': "Aacharya:",
                'content': result_text,
                'source': "Source: Aacharya (via Gemini AI)"
            }
        else:
            print(f"[Gemini Error] Status: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"[Exception] {e}")
        traceback.print_exc()
        return None

@app.route('/')
def health():
    return render_template('index.html')

@app.route('/api/health-query', methods=['POST'])
def handle_query():
    try:
        data = request.get_json()
        if not data or not data.get('query'):
            return jsonify({'error': 'Query parameter missing'}), 400

        query = data['query'].strip()
        if len(query) < 3:
            return jsonify({'error': 'Query must be at least 3 characters'}), 400

        result = get_health_info(query)

        if result:
            return jsonify({
                'status': 'success',
                'data': result
            })

        return jsonify({
            'status': 'not_found',
            'message': 'No information available for this query'
        }), 404

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

if __name__ == '__main__':
    app.run(port=5002, threaded=True)
