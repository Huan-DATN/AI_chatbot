# query check for PostgreSQL
from langchain_google_genai import ChatGoogleGenerativeAI
from app.clients.genimi_client import get_model
from app.models.state import QueryOutput, State


def check_query(state: State) -> str:
    structured_llm = ChatGoogleGenerativeAI(
        model=get_model(), temperature=0.1
    ).with_structured_output(QueryOutput)
    result = structured_llm.invoke(
        f"""
Rewrite the following PostgreSQL raw SQL query so that it is syntactically correct and unambiguous.
You must follow these rules:
- Use valid PostgreSQL syntax and PostgreSQL-specific features where appropriate.
- Enclose all table and column names in double quotes.
- Always qualify **all** column names with their table alias (e.g., p."name", cp."id").
- Use single quotes for string literals.
- Use ILIKE for case-insensitive string matching, and include '%' wildcards for partial matches unless exact match is required.
- Use LIMIT and OFFSET for pagination if present.
- Properly use PostgreSQL data types and functions.
- Do NOT add any backslashes or escape characters to the query.
- Do NOT escape single quotes in string literals.
- Return the raw SQL query string without any modifications or extra formatting.

SQL query: {state["query"]}
"""
    )

    print(result["query"])
    return {"query": result["query"]}
