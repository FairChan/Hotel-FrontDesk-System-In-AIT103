from flask import Flask, request, jsonify
import aiml
import os

app = Flask(__name__)

#Get paths to AIML and brain files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AIML_PATH = os.path.join(BASE_DIR, "basic.aiml")
BRAIN_PATH = os.path.join(BASE_DIR, "bot_brain.brn")

#Initialzing AIML Kernel
kernel = aiml.Kernel()

print("Loading AIML files...")
kernel.learn(AIML_PATH)
kernel.saveBrain(BRAIN_PATH)
print("AIML loaded and brain saved successfully.")


#Welcome Message Interface
@app.route("/welcome")
def welcome():
    welcome_msg = (
        "Hello, it's a chatbot assistant here.\n"
        "You can ask questions below:\n"
        "1. Register\n"
        "2. Where is the swimming pool?\n"
        "3. When is breakfast?\n"
        "4. Where is the gym?\n"
        "5. What about WIFI?\n"
        "6. When should I check out?\n"
    )
    return jsonify({"response": welcome_msg})


# Chat Interface
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Please enter a message."})

    response = kernel.respond(message)
    if not response.strip():
        response = "Sorry, I didn't understand that."

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
