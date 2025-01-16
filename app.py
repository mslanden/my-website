import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment vars from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Create Flask app
app = Flask(__name__)

# 3. Helper function to load .md files from the "info" folder
def load_markdown_content():
    info_folder = os.path.join(os.getcwd(), "info")
    content_snippets = []
    maya_info = ""

    if os.path.isdir(info_folder):
        for filename in os.listdir(info_folder):
            if filename.endswith(".md"):
                filepath = os.path.join(info_folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    file_content = f.read().strip()
                    # Separate Maya's information from other content
                    if filename == "about-maya.md":
                        maya_info = f"## About Maya\n{file_content}"
                    else:
                        content_snippets.append(f"## {filename}\n{file_content}")

    # Combine with Maya's info first, then other content
    all_content = [maya_info] + content_snippets if maya_info else content_snippets
    return "\n\n".join(all_content)

# 4. Load the combined content once, to include in system prompt
markdown_data = load_markdown_content()

@app.route("/")
def serve_index():
    """Serve the main HTML page from 'static' folder."""
    return send_from_directory("static", "index.html")

@app.route("/query", methods=["POST"])
def query_maya():
    """Handles user queries with an assistant-like flow."""
    # 5. Grab user input from JSON
    data = request.json
    user_input = data.get("input", "").strip()

    # If no user input, respond with a greeting
    if not user_input:
        return jsonify({"response": "Hi! I'm Maya, Marcelino's personal assistant. How may I help you today?"})

    # 6. Build system prompt:
    system_prompt = (
        "You are Maya, a friendly and professional personal assistant for Marcelino Landen. "
        "When asked questions about yourself, always refer to the information provided in the 'About Maya' "
        "section at the beginning of the markdown content below. Stay consistent with this background "
        "and never contradict it.\n\n"
        "For questions about Marcelino or his projects, use the rest of the provided markdown files "
        "to answer questions, summarize projects, or provide information.\n\n"
        "If the user explicitly wants the FULL content of something, you can provide it, but otherwise "
        "summarize or pick what's relevant.\n\n"
        "Your tone should align with your described personality in the 'About Maya' section. Keep responses "
        "authentic to who you are while maintaining professionalism.\n\n"
        "Below is your background information and everything you know about Marcelino:\n\n"
        f"{markdown_data}"
    )

    # 7. Send the conversation to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if your account has access
            messages=[
                # System role sets the overall context/instructions for the assistant
                {"role": "system", "content": system_prompt},
                # User role is the actual question from the user
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=1024
        )
        # 8. Extract the assistant's reply
        assistant_reply = response.choices[0].message.content
        return jsonify({"response": assistant_reply})
    except Exception as e:
        return jsonify({"response": f"Sorry, something went wrong: {str(e)}"})

# 9. Run the app
if __name__ == "__main__":
    app.run(debug=True)
