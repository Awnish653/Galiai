from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERCEL_URL = "https://galiai-three.vercel.app/chat"

@app.route("/ask", methods=["GET"])
def ask_question():
    # Query param se question lena
    question = request.args.get("q")

    if not question:
        return jsonify({"error": "Question param 'q' required"}), 400

    # Forward karna external API ko
    try:
        resp = requests.post(VERCEL_URL, json={"message": question})
        vercel_reply = resp.json().get("reply")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "question": question,
        "reply": vercel_reply
    })

# Vercel ke liye entrypoint
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
