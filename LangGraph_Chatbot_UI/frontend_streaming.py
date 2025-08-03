import streamlit as st
from streamlit import session_state
from langchain_core.messages import HumanMessage
from backend import chatbot
from langchain_core.runnables.config import RunnableConfig

thread_id = '1'

CONFIG: RunnableConfig = {
    "configurable": {
        "thread_id": thread_id
    }
}

if 'messages_history' not in session_state:
    session_state['messages_history'] = []
    
# loading conversion history
for message in session_state['messages_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type your message here...")

if user_input:
    
    # first add the user input to the messages history
    session_state['messages_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
        
    # add the user input to the workflow state using streaming
    with st.chat_message('assistant'):
        # Streaming response
        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = {"configurable": {"thread_id": "1"}},
                stream_mode='messages'
            )
        )
    
    session_state['messages_history'].append({'role': 'assistant', 'content': ai_response})