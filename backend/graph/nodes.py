from backend.config.settings import llm
from backend.graph.state import ChatState

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)

    return {
        'messages': [response]
    }