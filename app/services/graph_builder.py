from langgraph.graph import START, StateGraph, END

from app.models.state import State
from app.nodes.answer.generate_answer_node import generate_answer
from app.nodes.sql.check_query_node import check_query
from app.nodes.sql.execute_query_node import execute_query
from app.nodes.sql.write_query_node import write_query
from app.nodes.intent.detect_intent_node import detect_intent
from app.nodes.faq.retrieve_faq_node import retrieve_faq
from app.nodes.faq.generate_faq_answer_node import generate_faq_answer


def build_graph():
    """Build the state graph with a unified processing path."""
    # Create a new graph
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node("detect_intent", detect_intent)
    graph_builder.add_node("retrieve_faq", retrieve_faq)
    graph_builder.add_node("write_query", write_query)
    graph_builder.add_node("check_query", check_query)
    graph_builder.add_node("execute_query", execute_query)
    graph_builder.add_node("generate_sql_answer", generate_answer)
    graph_builder.add_node("generate_faq_answer", generate_faq_answer)

    # Connect the nodes in a unified path
    graph_builder.add_edge(START, "detect_intent")

    graph_builder.add_edge("retrieve_faq", "generate_faq_answer")

    graph_builder.add_edge("write_query", "check_query")
    graph_builder.add_edge("check_query", "execute_query")
    graph_builder.add_edge("execute_query", "generate_sql_answer")

    graph_builder.add_edge("generate_faq_answer", END)
    graph_builder.add_edge("generate_sql_answer", END)

    def conditional_edge_for_detect_intent(state: State):
        intent = state.get("intent")

        if(intent == "faq"):
            return "retrieve_faq"
        else:
            return "write_query"

    graph_builder.add_conditional_edges(
        "detect_intent",
        conditional_edge_for_detect_intent
    )



    # Compile the graph
    return graph_builder.compile()


# Create a singleton instance
_graph = None

def get_graph():
    """Get the graph singleton."""
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
