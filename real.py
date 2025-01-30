from flask import Flask, redirect, render_template, request, jsonify, url_for
import requests

app = Flask(__name__)

# API key directly in code
api_key = "AIzaSyApzj5jfJITJCgEu_2RKNUlpfFLAJQ41hI"

# Agro-related keywords for filtering
keywords = ["agriculture", "crops", "grow", "weather", "harvest", "irrigation", 
           "farming", "soil", "pesticides", "fertilizers", "rabi", "kharif", 
           "season", "summer", "winter", "plant", "sowing", "seeds"]

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route("/gemini", methods=['POST'])
def api_call():
    if not api_key:
        return jsonify({"error": "Gemini API key is missing."}), 500
    
    try:
        data = request.get_json()
        if not data or 'input' not in data:
            return jsonify({"error": "No input provided"}), 400
        
        chat_input = data.get("input")
        
        # Changed the model to gemini-pro which is more stable
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"You are an agricultural expert assistant. Please provide information about: {chat_input}"
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        response = requests.post(gemini_url, json=payload)
        response.raise_for_status()
        
        gemini_response = response.json()
        
        # Debug logging
        print("Gemini Response:", gemini_response)
        
        if 'candidates' in gemini_response and gemini_response['candidates']:
            complete_response = gemini_response['candidates'][0]['content']['parts'][0]['text']
            
            # Check if the input contains agricultural keywords
            if any(keyword in chat_input.lower() for keyword in keywords):
                return jsonify({"response": complete_response})
            else:
                return jsonify({"response": "This query is not agro-related. Please try again with a question about agriculture!"})
        else:
            print("Unexpected response structure:", gemini_response)
            return jsonify({"response": "Could not extract response from Gemini. Please try again."}), 500

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except KeyError as e:
        print(f"Key error: {str(e)}")
        return jsonify({"error": "Invalid response format from Gemini API"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)