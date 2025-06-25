from flask import Blueprint, request, jsonify
from app.services.chatbot_service import get_bot_response

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print(data)
    user_message = data.get("message", "")

    data = request.get_json()
    session_id = data.get("session_id", None)
    print("session_id: ", session_id)

    if not user_message:
        return jsonify({"error": "Message is required."}), 400

    bot_response = get_bot_response(user_message, session_id)
    return jsonify({"response": bot_response})
