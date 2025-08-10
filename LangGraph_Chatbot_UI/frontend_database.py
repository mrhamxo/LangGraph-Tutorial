import streamlit as st
from streamlit import session_state
from langchain_core.messages import HumanMessage
from database_backend import chatbot,  retrieve_all_threads
from langchain_core.runnables.config import RunnableConfig
import uuid

st.set_page_config(page_title="My Chatbot App")

# **************************** Utility Functions ****************************

def generate_id():
    thread_id = uuid.uuid4() # Generate a unique thread ID
    return thread_id

def reset_chat():
    thread_id = generate_id()
    session_state['thread_id'] = thread_id
    add_thread(session_state['thread_id'])
    session_state['messages_history'] = []
    
def add_thread(thread_id):
    if thread_id not in session_state['chat_threads']:
        session_state['chat_threads'].append(thread_id)   
        
def load_conversation(thread_id):
    # This function can be implemented to load conversation history for a specific thread
    return chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values['messages']

# **************************** Session setup ***************************

if 'messages_history' not in session_state:
    session_state['messages_history'] = []

if 'thread_id' not in session_state:
    session_state['thread_id'] = generate_id()

if 'chat_threads' not in session_state:
    session_state['chat_threads'] =  retrieve_all_threads()
    
add_thread(session_state['thread_id'])
    
# *************************** Sidebar UI *********************************

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversion")

for thread_id in session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        
        temp_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': message.content})
            
        session_state['messages_history'] = temp_messages     
    
# ***************************** Main UI *********************************
    
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
        
    CONFIG: RunnableConfig = {
       "configurable": {
            "thread_id": session_state['thread_id']
        }
    }
        
    # add the user input to the workflow state using streaming
    with st.chat_message('assistant'):
        # Streaming response
        ai_response = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode='messages'
            )
        )
    
    session_state['messages_history'].append({'role': 'assistant', 'content': ai_response})