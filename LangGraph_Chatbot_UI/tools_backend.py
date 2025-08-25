from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests
import os

from dotenv import load_dotenv
import sqlite3

load_dotenv()

# ✅ Get API key from env
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# 1. LLM Model
model = ChatGroq(model="llama-3.3-70b-versatile")

# 2. Tools
# Search Tool
search_tool = DuckDuckGoSearchRun(region="us-en")

# Calculator Tool
@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}

# Stock Price Tool
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    r = requests.get(url)
    return r.json()

# Make tool list
tools = [get_stock_price, search_tool, calculator]

# Make the LLM tool-aware
llm_with_tools = model.bind_tools(tools)

# 3. State 
class ChatState(TypedDict):    
    messages: Annotated[list[BaseMessage], add_messages]
    
# 4. Node
def chat_node(state: ChatState):
    """LLM that may  answer or request a tool call."""
    # take user query from the state
    messages = state['messages']
    # send the query to the model
    response = llm_with_tools.invoke(messages)
    # add the model response to the state
    return {'messages': [response]}

tool_node = ToolNode(tools)  # Executes tool calls

# 5. checkpointer
connect = sqlite3.connect('chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=connect)

# 6. Graph
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")    
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

# 7. Helpers to retrieve all thread ids from the checkpointer
def  retrieve_all_threads():
    
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)