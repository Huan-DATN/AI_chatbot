from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.state import State, IntentOutput
from app.clients.genimi_client import get_api_key, get_model
from app.services.history_service import get_history_str


def detect_intent(state: State):
    """Detect the intent of the question using LLM."""
    try:
        history_str = get_history_str(state.get("chat_history", []))

        structured_llm = ChatGoogleGenerativeAI(
            model=get_model(),
            temperature=0.1,
            google_api_key=get_api_key(),
        ).with_structured_output(IntentOutput)

        prompt = f"""
        You are an intent classifier for a chatbot system that serves customers interested in OCOP (One Commune One Product) products.

        Based on the user's question, determine if the intent is:

        1. "faq" - For general questions about OCOP products, services, or information that can be answered from a FAQ database.
           Examples:
           - "What is an OCOP product?"
           - "How are OCOP products rated?"
           - "Where can I buy OCOP products?"
           - "What are the benefits of OCOP products?"
           - "How do I become an OCOP seller?"

        2. "sql" - For specific data queries that require database lookups about products, prices, inventory, etc.
           Examples:
           - "Show me all products under 500,000 VND"
           - "List the top 5 highest rated products"
           - "How many products are in the food category?"
           - "Which sellers have the most products?"
           - "Compare prices of products from Hanoi and Ho Chi Minh City"

        User's question: {state["question"]}

        Chat history:
        {history_str}

        Think step by step:
        1. Analyze if the question is asking for general information (FAQ) or specific data that would require querying a database (SQL)
        2. Consider if the question is about general concepts, definitions, or processes (FAQ) versus specific listings, counts, or comparisons of products/data (SQL)
        3. Determine the most appropriate intent category

        Respond with just the intent classification as either "faq" or "sql".
        """

        result = structured_llm.invoke(prompt)
        intent = result["intent"].lower()

        print("intent: ", intent)

        # Validate intent
        if intent not in ["faq", "sql"]:
            intent = "sql"  # Default to SQL if invalid

        # Return the full state with updated intent
        return {"intent": intent}
    except Exception as e:
        print(f"Error in detect_intent: {e}")
        # Default to SQL on error
        return {"intent": "sql"}
