from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from app.models.state import State
from app.clients.db_client import db


def execute_query(state: State):
    """Execute SQL query."""
    try:


        execute_query_tool = QuerySQLDatabaseTool(db=db)
        result = execute_query_tool.invoke(state["query"])

        return {"result": result}
    except Exception as e:
        print("Error executing query:", e)
        return {"result": f"Error executing query: {e}"}
