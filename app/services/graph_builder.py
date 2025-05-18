from langgraph.graph import START, StateGraph

from app.models.state import State
from app.nodes.answer.generate_answer_node import generate_answer
from app.nodes.sql.check_query_node import check_query
from app.nodes.sql.execute_query_node import execute_query
from app.nodes.sql.write_query_node import write_query

graph_builder = StateGraph(State).add_sequence(
    [write_query, check_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()


def get_graph():
    return graph
