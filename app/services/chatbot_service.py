from app.services.graph_builder import get_graph
from app.services.history_service import get_chat_history
import uuid

graph = get_graph()


def get_bot_response(message: str, session_id):
    """
    Nhận câu hỏi từ user, chạy graph, và trả về câu trả lời cuối cùng.
    """
    try:
        return chat(message, session_id)
    except Exception as e:
        print(f"Error in get_bot_response: {e}")
        return f"Error: {str(e)}"


def chat(question: str, session_id: str = None):
    """Process a chat message and return the response."""
    if session_id is None:
        session_id = str(uuid.uuid4())

    chat_history_store = get_chat_history(session_id)
    chat_history_store.add_user_message(question)

    messages = [
        {"role": "user" if msg.type == "human" else "bot", "content": msg.content}
        for msg in chat_history_store.messages
    ]

    # Create the initial state with all required fields
    initial_state = {
        "question": question,
        "query": "",
        "result": "",
        "answer": "",
        "chat_history": messages,
        "session_id": session_id,
        "intent": None,
        "faq_results": []
    }

    # Invoke the graph with the initial state
    result = graph.invoke(initial_state)

    # Add the bot's response to history
    chat_history_store.add_ai_message(result["answer"])

    return {
        "answer": result["answer"],
        "session_id": session_id,
    }
