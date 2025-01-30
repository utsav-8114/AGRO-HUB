from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv  # Importing the API key
import os
import google.generativeai as genai

app = Flask(__name__)

# Load the environment variables (API key) from .env file
load_dotenv()

# Retrieve the Gemini API key from the environment
api_key = "AIzaSyApzj5jfJITJCgEu_2RKNUlpfFLAJQ41hI"  # Ensure the correct API key name is used here

# Agro-related keywords for filtering
keywords = ["agriculture", "crops", "grow", "weather", "harvest", "irrigation", "farming", "soil", "pesticides", "fertilizers"]

@app.route("/gemini", methods=["POST"])
def api_call():
    if not api_key:
        return jsonify({"error": "Gemini API key is missing."}), 500

    
    
    data = request.get_json()
    chat_input = data.get("input")  # user input lena

    # Construct the Gemini API URL
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # headers assign krna
    headers = {}
    
    # payload banana
    payload = {"query": chat_input}

    try:
        #send the request to gemini api
        response = requests.post(gemini_url, json=payload, headers=headers)

        # If the request is successful, process the response
        response.raise_for_status()  # This will raise an error if the response code isn't 200

        # Extract the JSON response from the Gemini API
        gemini_response = response.json()

        # Get the full response text from Gemini
        complete_response = gemini_response.get("response", "")

        # Check if the response contains any agro-related keywords
        if any(keyword in complete_response.lower() for keyword in keywords):
            return jsonify({"response": complete_response})  # Return the response if matching with list
        else:
            return jsonify({"response": "This query is not agro-related. Please try again with a question about agriculture!"})

    except requests.exceptions.RequestException as e:
        # exception block defining
        return jsonify({"error": "Failed to contact the server. Please try again!"}), 500

if __name__ == "__main__":
    app.run(debug=True)  #debug mode
