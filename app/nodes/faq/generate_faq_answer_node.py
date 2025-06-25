from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.state import State
from app.clients.genimi_client import get_api_key, get_model
from app.services.history_service import get_history_str
import redis
from app.config import get_config

config = get_config()

redis_client = redis.StrictRedis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    username=config.REDIS_USERNAME,
    password=config.REDIS_PASSWORD,
    decode_responses=True,
)


def generate_faq_answer(state: State):
    """Generate answer using FAQ results with enhanced LLM prompting."""
    try:
        history_str = get_history_str(state.get("chat_history", []))
        faq_results = state.get("faq_results", [])

        # Format the FAQ results for the prompt
        faq_context = ""
        for i, result in enumerate(faq_results):
            similarity = result.get("similarity", 0)
            faq_context += f"FAQ {i+1} (Similarity: {similarity:.2f}):\n"
            faq_context += f"Question: {result.get('question', '')}\n"
            faq_context += f"Answer: {result.get('answer', '')}\n"
            if result.get("category"):
                faq_context += f"Category: {result.get('category')}\n"
            if result.get("tags"):
                faq_context += f"Tags: {', '.join(result.get('tags'))}\n"
            faq_context += "\n"

        prompt = f"""
        You are a knowledgeable and helpful AI assistant for a system of stores selling OCOP (One Commune One Product) products in Vietnam.
        Your task is to provide accurate, helpful, and friendly responses to customer questions about OCOP products and services.

        Chat history:
        {history_str}

        User's question: {state["question"]}

        Retrieved FAQ results:
        {faq_context}

        Instructions:
        1. Analyze the retrieved FAQ results and their similarity scores to determine their relevance to the user's question.
        2. If the FAQ results are highly relevant (similarity > 0.8), use them as the primary source for your answer.
        3. If the FAQ results are moderately relevant (similarity between 0.7-0.8), use them but supplement with general knowledge about OCOP products.
        4. If multiple FAQ results are relevant, synthesize the information from all relevant entries.
        5. If the FAQ results don't seem relevant enough, inform the user that you don't have specific information on their question and suggest they rephrase or ask about general OCOP topics.
        6. Maintain a friendly, helpful, and professional tone appropriate for customer service.
        7. Keep your answer concise and focused on answering the specific question.
        8. If appropriate, suggest related questions the user might be interested in.

        Your response should be in Vietnamese and should be helpful to someone interested in OCOP products.
        """

        stream = ChatGoogleGenerativeAI(
            model=get_model(),
            temperature=0.7,
            google_api_key=get_api_key(),
        ).stream(prompt)

        full_response = ""
        for chunk in stream:
            if chunk.content:
                redis_client.publish(state["session_id"], chunk.content)
                full_response += chunk.content

        redis_client.publish(state["session_id"], "DONE")
        print("answer: ", full_response)

        return {"answer": full_response}
    except Exception as e:
        print(f"Error generating FAQ answer: {e}")
        return {"answer": f"Lỗi khi tạo câu trả lời: {e}"}
