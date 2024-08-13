from flask import Flask, request, jsonify
from openai_parameters import extract_keywords, query_ai

app = Flask(__name__)

model = "its"

@app.route("/chat", methods=["POST"])
def chat():
    global model
    mode_changed = False
    user_message = request.json.get("message")
    keyword_message = extract_keywords(user_message)

    if keyword_message == "ITS MODE":
        model = "its"
        response_message = "ITS MODE"
        mode_changed = True
    elif keyword_message == "TLS MODE":
        model = "tls"
        response_message = "TLS MODE"
        mode_changed = True
    
    # Ensure 'model' is initialized before it's used
    
    if not mode_changed:
        ai_message = query_ai(keyword_message, 10, user_message, model)
        response_message = f"{ai_message}"
    
    return jsonify({"response": response_message})

if __name__ == "__main__":
    app.run(debug=True)



