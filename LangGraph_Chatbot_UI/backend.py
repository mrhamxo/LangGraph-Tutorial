from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv

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

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')

graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)
