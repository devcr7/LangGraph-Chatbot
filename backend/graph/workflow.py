from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from backend.graph.state import ChatState
from backend.graph.nodes import chat_node

def build_graph():
    graph = StateGraph(ChatState)

    # nodes
    graph.add_node('chat_node', chat_node)

    # edges
    graph.add_edge(START, 'chat_node')
    graph.add_edge('chat_node', END)

    # memory
    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)