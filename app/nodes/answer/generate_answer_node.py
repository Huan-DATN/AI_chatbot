import json
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.state import State
from app.clients.genimi_client import get_api_key, get_model
from app.prompts.postgres_agent_prompt import generate_prompt_answer
import redis
from app.config import get_config

config = get_config()

redis_client = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    try:
        stream = ChatGoogleGenerativeAI(
            model=get_model(),
            temperature=0.7,
            google_api_key=get_api_key(),
        ).stream(generate_prompt_answer(state))

        full_response = ""
        for chunk in stream:
            if chunk.content:
                redis_client.publish(state["session_id"], chunk.content)
                full_response += chunk.content

        redis_client.publish(state["session_id"], "DONE")
        print(full_response)
        return {"answer": full_response}
    except Exception as e:
        print("Error generating answer:", e)
        return {"answer": f"Lỗi khi tạo câu trả lời: {e}"}
