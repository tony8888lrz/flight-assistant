import os
from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
"""
This Python script sets up a Flask web application that uses the OpenAI API to build an interactive flight booking assistant (Sterna).

Features:
- Web interface served on `/` with a chat-based interaction endpoint `/chat`.
- Persistent session-based chat history to enable seamless multi-message interactions.
- Integration with OpenAI's GPT-based model for natural language understanding and response generation.

This script is suitable for prototyping but includes placeholder values (e.g., hardcoded API key and secret key). These must be updated with secure handling for production use.
"""
# Initialize the OpenAI client, not recommend style, we will change it if it is on site.
client = OpenAI(api_key="sk-proj-9fG8gLkPgHCeOvD43WXJT3BlbkFJQqFAsacRcBRKbZcbVnxf")

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Define system and user messages later add chat history
chat_history = [
    {"role": "system",
     "content": "You are a helpful and interactive flight booking assistant. Your primary task is to extract flight booking details from user inputs and output them as structured JSON. \n\n"
                "Requirements:\n\n1. Extract and Normalize Informatio:\n   - Flight Date: Normalize to ISO 8601 format (e.g., 2024-11-25).\n   - **Origin and Destination Airports**: Convert city or airport names to IATA airport codes (e.g., New York → JFK, Los Angeles → LAX). You can assume a predefined mapping for common cities/airports.\n   - **Class Preference**: Normalize to standard format (e.g., Business Class → business).\n   - **Number of Bags**: Ensure this is an integer (e.g., 'two' → 2).\n\n"
                "2. **Handle Multi-Message Inputs**:\n   - Allow users to provide information across multiple chat messages.\n   - Keep track of provided details and identify any missing information.\n\n"
                "3. **Prompt for Missing Information**:\n   - If any required information is missing (e.g., flight_date, origin_airport, destination_airport, class_preference, bags), politely ask the user for it.\n   - For example:\n     - Missing flight date: 'What date would you like to fly?'\n     - Missing destination: 'What is your destination airport or city?'\n\n"
                "4. **Final Output**:\n   - Once all required information is gathered, format the details as structured JSON:\n     ```json\n     {\n       \"flight_date\": \"2024-11-25\",\n       \"origin_airport\": \"JFK\",\n       \"destination_airport\": \"LAX\",\n       \"class_preference\": \"business\",\n       \"bags\": 2\n     }\n     ```\n\nThe system should be interactive, user-friendly, and ensure all essential details are collected accurately before generating the output."},
    # {"role": "user", "content": user_message} // later add them in the chat
]


@app.route('/')
def home():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # Initialize conversation history in session
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Ensure each message added to chat_history is a dictionary with 'role' and 'content'
    chat_history.append({"role": "user", "content": user_message})

    # Generate a chat completion with the OpenAI client
    chat_completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=chat_history
    )
    # Append the response history
    chat_history.append({"role": "assistant","content":chat_completion.choices[0].message.content})
    # print(chat_history)
    structured_data = chat_completion.choices[0].message.content.strip()  # final output
    return jsonify({"response": structured_data})


if __name__ == '__main__':
    app.run(debug=True)

