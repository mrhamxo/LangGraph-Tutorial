from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

model = ChatGroq(model="llama-3.3-70b-versatile")

class ChatState(TypedDict):    
    messages: Annotated[list[BaseMessage], add_messages]
    
def chat_node(state: ChatState):
    
    # take user query from the state
    messages = state['messages']
    # send the query to the model
    response = model.invoke(messages)
    # add the model response to the state
    return {'messages': [response]}

connect = sqlite3.connect('chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=connect)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def  retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)