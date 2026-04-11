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

    # generator
    # stream = chatbot.stream(
    #     {'messages': [HumanMessage(content=user_message)]},
    #     config=config,
    #     stream_mode='messages'
    # )
    #
    # for message_chunk, metadata in stream:
    #     if message_chunk.content:
    #         print(message_chunk.content, end = " ", flush=True)

    # response = chatbot.invoke(
    #     {"messages": [HumanMessage(content=user_message)]},
    #     config=config
    # )

    # print("AI:", response['messages'][-1].content)


    # accessing state via thead_id
    CONFIG = {'configurable': {'thread_id': "thread-1"}}

    response = chatbot.invoke(
        {'messages': [HumanMessage(content="Hi I'm Divyanshu")]},
        config=CONFIG
    )

    print(chatbot.get_state(config=CONFIG).values['messages'])