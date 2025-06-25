from app.models.state import State, QueryOutput, examples
from app.prompts.postgres_agent_prompt import prefix_prompt
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.clients.db_client import db
import os
from app.clients.genimi_client import get_api_key, get_model
from app.services.history_service import get_history_str


os.environ["GOOGLE_API_KEY"] = get_api_key()


example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    FAISS,
    k=5,
    input_keys=["question"],
)


prompt_few_shot = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User question: {question}\nSQL query: {query}"
    ),
    prefix=prefix_prompt,
    suffix="""
    History context:
    {chat_history}

    User question: {question}

    Think step by step:
    1. Identify the tables and columns needed to answer this question
    2. Determine the appropriate joins between tables
    3. Consider any filtering conditions needed
    4. Decide if aggregation, grouping, or ordering is required
    5. Ensure all table and column names are enclosed in double quotes

    Now, generate a syntactically correct PostgreSQL query to answer the question:
    SQL query:
    """,
    input_variables=["question", "top_k", "table_info", "chat_history"],
)


def write_query(state: State):
    """Generate SQL query to fetch information using enhanced LLM prompting."""

    try:

        history_str = get_history_str(state.get("chat_history", []))
        prompt = prompt_few_shot.invoke(
            {
                "top_k": 10,
                "table_info": db.get_table_info(),
                "question": state["question"],
                "chat_history": history_str,
            }
        )
        structured_llm = ChatGoogleGenerativeAI(
            model=get_model(), temperature=0.1
        ).with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)

        return {"query": result["query"]}
    except Exception as e:
        print(f"Error in write_query: {e}")
        return {"query": "SELECT 1;"}
