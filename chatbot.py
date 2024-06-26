from flask import Flask, render_template, request
import re
import json
import http.client as http
import urllib.parse as io
import random

app = Flask(__name__)

# Define the file path for storing conversation history
FILE_PATH = "conversation_history.txt"

# Dictionary to store user input and corresponding bot responses
conversation_history = {}

# Dictionary to cache Wikipedia article content
article_cache = {}

# Function to match user input to patterns and return a response
def get_response(user_input):
    # Normalize user input (remove punctuation and convert to lowercase)
    normalized_input = normalize_input(user_input)

    # Check if the user input is already in the conversation history
    if normalized_input in conversation_history:
        return conversation_history[normalized_input]
    else:
        # If the user input is not in the conversation history, fetch data
        response = fetch_data_from_wikipedia(normalized_input)
        conversation_history[normalized_input] = response
        return response

# Function to normalize user input
def normalize_input(input_str):
    # Convert input to lowercase and remove punctuation
    return re.sub(r'[^\w\s]', '', input_str.lower())

# Function to fetch data from Wikipedia API with caching
def fetch_data_from_wikipedia(query):
    # Check if article content is cached
    if query in article_cache:
        return article_cache[query]
    else:
        # Construct the Wikipedia API request URL
        url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&titles=" + io.quote(query)

        # Make the HTTP request to the Wikipedia API
        conn = http.HTTPSConnection("en.wikipedia.org")
        conn.request("GET", url)
        response = conn.getresponse()

        # Parse the JSON response
        data = json.loads(response.read().decode())
        
        # Extract the introductory text from the response
        pages = data["query"]["pages"]
        for page_id, page_data in pages.items():
            if "extract" in page_data:
                extract = page_data["extract"]
                # Cache the article content
                article_cache[query] = extract
                return extract
        
        # If no extract is found, return a default response
        return f"Sorry, I couldn't find any information on '{query}' on Wikipedia."

# Function to save conversation history to a file
def save_history_to_file(history):
    with open(FILE_PATH, "w") as file:
        for user_input, bot_response in history.items():
            file.write(user_input + "," + bot_response + "\n")

# Function to load conversation history from a file
def load_history_from_file():
    history = {}
    try:
        with open(FILE_PATH, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    history[parts[0]] = parts[1]
    except FileNotFoundError:
        pass
    return history

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    bot_response = get_response(user_input)
    return {"bot_response": bot_response}

if __name__ == "__main__":
    # Load conversation history from file
    conversation_history = load_history_from_file()
    app.run(debug=True)
