import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch the API key
api_key = os.getenv("api_key")
if not api_key:
    raise RuntimeError("API key not set in .env file or as an environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Chat log to maintain context
chat_log = []

# Define the root route
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the ChatGPT Server API!"

# Define the /chatgpt route
@app.route("/chatgpt", methods=["POST"])
def chatgpt():
    global chat_log
    try:
        # Get user query from the request
        user_message = request.json.get("query", "")

        # Append the user message to the chat log
        chat_log.append({"role": "user", "content": user_message})

        # Generate response from ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with "gpt-4" if needed
            messages=chat_log
        )

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content.strip()

        # Append the assistant response to the chat log
        chat_log.append({"role": "assistant", "content": assistant_response})

        # Return the assistant's response as JSON
        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Custom 404 error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found. Use /chatgpt for API requests."}), 404

# Entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
