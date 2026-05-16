from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from langgraph.prebuilt import ToolNode, tools_condition

import requests
import os

load_dotenv()
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

from duckduckgo_search import DDGS
from langchain_core.tools import tool

@tool
def search_tool(query: str) -> str:
    """
    Search the web for current events, news, stock movements, or general information.
    Use this when you need real-time data or answers not present in your training data.
    """
    try:
        # First, ensure you ran: pip install -U duckduckgo-search
        with DDGS() as ddgs:
            results = [r["body"] for r in ddgs.text(query, max_results=3)]
            return "\n\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Error performing search: {str(e)}"

@tool
def calculator(first_num: float, second_num: float, operation: str) -> float | dict[str, str]:
    """
    Perform basic arithmetic operation on two numbers
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            return first_num + second_num
        elif operation == "sub":
            return first_num - second_num
        elif operation == "mul":
            return first_num * second_num
        elif operation == "div":
            return first_num / second_num
        else:
            return {"error": f"Unsupported operation: '{operation}'"}
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": None}
    except Exception as ex:
        return {"error": str(ex)}


@tool
def get_stock_price(symbol: str) -> float | dict[str, str]:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA')
    using Alpha Vantage API key in the URL
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    r = requests.get(url)
    return r.json()

tools = [search_tool, calculator, get_stock_price]