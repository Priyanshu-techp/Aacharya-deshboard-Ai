from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import traceback
import re

app = Flask(__name__)
CORS(app)

# ✅ Gemini API config
GEMINI_API_KEY = "AIzaSyCqpK4AssbLK6EfFr6lBlGGMAa9nkvD-cY"
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

# ✅ Remove emoji (optional cleaner)
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002500-\U00002BEF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# 🔍 Analyze news using Gemini
def analyze_news_gemini(user_input):
    try:
        headers = {"Content-Type": "application/json"}
        prompt = (
            "You are a fake news detection expert. Analyze the following news and determine "
            "whether it is real or fake. Give a clear answer ('Real' or 'Fake') followed by "
            "a short explanation.\n\nNews: \"" + user_input + "\""
        )

        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)

        if response.status_code == 200:
            result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return remove_emojis(result_text)
        else:
            print("[Gemini API Error]", response.text)
            return "Sorry, couldn't analyze the news right now."

    except Exception as e:
        traceback.print_exc()
        return f"Error occurred: {str(e)}"

@app.route('/')
def news():
    return render_template('fake.html')

@app.route('/analyze', methods=['POST'])
def analyze_news():
    data = request.json
    user_input = data.get("news")

    if not user_input:
        return jsonify({"error": "No news provided"}), 400

    print("Received input:", user_input)
    result = analyze_news_gemini(user_input)

    return jsonify({"analysis": result})

if __name__ == '__main__':
    print("✅ Fake News Detector (Gemini) running at http://127.0.0.1:5003")
    app.run(debug=True, port=5003)
