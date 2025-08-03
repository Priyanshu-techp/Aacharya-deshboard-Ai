import requests 
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import traceback
import re
app = Flask(__name__)
CORS(app)
 # make sure this is at the top if not already




# Gemini API key
GEMINI_API_KEY = "AIzaSyCqpK4AssbLK6EfFr6lBlGGMAa9nkvD-cY"
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

def get_ai_response(query):
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "parts": [{"text": query}]
                }
            ]
        }

        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"[Gemini API Error] Status code: {response.status_code}, Response: {response.text}")
            return "Sorry, I couldn't get a response from Gemini AI."
    except Exception as e:
        print(f"[Gemini Error] {e}")
        traceback.print_exc()
        return "Sorry, I couldn't get a response from the AI."



def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" 
                           u"\U0001F300-\U0001F5FF"  
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002500-\U00002BEF"  
                           u"\U00002702-\U000027B0"
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

def get_ai_response(query):
    try:
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "parts": [{"text": query}]
                }
            ]
        }

        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=data)
        if response.status_code == 200:
            raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            clean_text = remove_emojis(raw_text)
            return clean_text
        else:
            print(f"[Gemini API Error] Status code: {response.status_code}, Response: {response.text}")
            return "Sorry, I couldn't get a response from Gemini AI."
    except Exception as e:
        print(f"[Gemini Error] {e}")
        traceback.print_exc()
        return "Sorry, I couldn't get a response from the AI."


@app.route('/')
def index():
    return render_template('3D_AI.html')

@app.route('/api/process-voice', methods=['POST'])
def process_voice():
    try:
        data = request.get_json()
        query = data.get("query", "")

        if not query:
            return jsonify({"status": "error", "message": "No query provided"}), 400

        response = get_ai_response(query)

        return jsonify({
            "status": "success",
            "query": query,
            "response": response
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Optional: Auto open browser
    # threading.Thread(
    #     target=lambda: (time.sleep(1), webbrowser.open("http://127.0.0.1:5000")),
    #     daemon=True
    # ).start()

    print("✅ Aacharya AI is running at http://127.0.0.1:5006")
    app.run(debug=True, port=5006)
