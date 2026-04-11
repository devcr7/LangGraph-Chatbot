from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from backend.graph.state import ChatState
from backend.graph.nodes import chat_node

import sqlite3

# memory
conn = sqlite3.connect('chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

def build_graph():
    graph = StateGraph(ChatState)

    # nodes
    graph.add_node('chat_node', chat_node)

    # edges
    graph.add_edge(START, 'chat_node')
    graph.add_edge('chat_node', END)

    return graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    # List all checkpoints and extract thread IDs
    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config.get('configurable', {}).get('thread_id')
        if thread_id:
            all_threads.add(thread_id)
    return list(all_threads)