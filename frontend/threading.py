import streamlit as st
import uuid
from backend.graph.workflow import build_graph
from langchain_core.messages import HumanMessage


# --- UTILITY FUNCTIONS ---

def generate_thread_id():
    """Generates a unique ID for a new chat thread."""
    return str(uuid.uuid4())


def add_thread(thread_id):
    """Adds a thread ID to the sidebar list if it doesn't exist."""
    if 'chat_threads' not in st.session_state:
        st.session_state['chat_threads'] = []
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def reset_chat():
    """Resets the state for a brand new conversation."""
    new_id = generate_thread_id()
    st.session_state['thread_id'] = new_id
    st.session_state['message_history'] = []
    add_thread(new_id)


# --- SESSION INITIALIZATION ---

if 'chatbot' not in st.session_state:
    # This assumes build_graph() returns a compiled LangGraph with a checkpointer
    st.session_state['chatbot'] = build_graph()

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Ensure the current thread is in the sidebar list
add_thread(st.session_state['thread_id'])

chatbot = st.session_state['chatbot']

# --- SIDEBAR UI ---

st.sidebar.title("🤖 Chatbot")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    reset_chat()
    st.rerun()

st.sidebar.divider()
st.sidebar.header("My Conversations")

# Display clickable thread history
for thread_id in st.session_state['chat_threads'][::-1]:
    # Highlight the active thread button
    is_active = (thread_id == st.session_state['thread_id'])
    label = f"💬 {thread_id[:8]}..."

    if st.sidebar.button(label, key=f"btn_{thread_id}", disabled=is_active, use_container_width=True):
        st.session_state['thread_id'] = thread_id

        # Load state from LangGraph checkpointer
        state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
        messages = state.values.get('messages', [])

        # Sync session history with LangGraph history
        temp_history = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            if msg.content:
                temp_history.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_history
        st.rerun()

# --- MAIN CHAT UI ---

st.title("Chat")
st.caption(f"Current Thread: `{st.session_state['thread_id']}`")

# Display previous messages from history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Chat Input
user_input = st.chat_input('Type your message...')

if user_input:
    # 1. Add user message to UI
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    # 2. Generate AI response with streaming
    with st.chat_message('assistant'):
        # Dynamic config for the current active thread
        current_config = {'configurable': {'thread_id': st.session_state['thread_id']}}


        def stream_generator():
            for chunk, metadata in chatbot.stream(
                    {"messages": [HumanMessage(content=user_input)]},
                    config=current_config,
                    stream_mode="messages"
            ):
                if chunk.content:
                    yield chunk.content


        ai_response = st.write_stream(stream_generator())

    # 3. Save AI response to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_response})