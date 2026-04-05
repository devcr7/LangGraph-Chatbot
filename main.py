from langchain_core.messages import HumanMessage
from backend.graph.workflow import build_graph

chatbot = build_graph()
thread_id = "1"

while True:
    user_message = input('Type your message: ')
    print('User:', user_message)

    if user_message.strip().lower() in ['exit', 'quit', 'bye']:
        break

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    response = chatbot.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=config
    )

    print("AI:", response['messages'][-1].content)