from langgraph.prebuilt import ToolNode

from backend.config.settings import llm
from backend.graph.state import ChatState
from backend.graph.tools import tools

def chat_node(state: ChatState):
    messages = state['messages']
    llm_with_tools = llm.bind_tools(tools)
    response = llm_with_tools.invoke(messages)

    return {
        'messages': [response]
    }

tool_node = ToolNode(tools)