import os
import json
import feedparser
from urllib.parse import quote_plus
from dotenv import load_dotenv
import streamlit as st
from vertex_chat import get_vertex_response

# Load environment variables (if needed later)
load_dotenv()

# --------------------- Tool Utilities ---------------------

def unwrap_tool_result(raw):
    """Safely extract JSON from raw MCP tool response."""
    try:
        return json.loads(raw.get("result", {}).get("text", "{}"))
    except (TypeError, json.JSONDecodeError):
        return {}

def fetch_portfolio_names():
    """Fetch relevant investment keywords from user session."""
    from modules.mcp_tools import call_mcp_tool

    session_id = st.session_state.get("session_id")
    base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
    tools = ["fetch_mf_transactions", "fetch_stock_transactions", "fetch_net_worth"]
    keywords = set()

    for tool in tools:
        raw_result = call_mcp_tool(tool, session_id, base_url)
        result = unwrap_tool_result(raw_result)

        if tool == "fetch_mf_transactions":
            for txn in result.get("mfTransactions", []):
                name = txn.get("schemeName") or txn.get("fund_name") or txn.get("scheme")
                if name:
                    keywords.add(clean_name(name))

        elif tool == "fetch_stock_transactions":
            for stk in result.get("stockTransactions", []):
                name = stk.get("symbol") or stk.get("stock_name")
                if name:
                    keywords.add(clean_name(name))

        elif tool == "fetch_net_worth":
            for mf in result.get("mfSchemeAnalytics", {}).get("schemeAnalytics", []):
                scheme = mf.get("schemeDetail", {}).get("nameData", {}).get("longName")
                if scheme:
                    keywords.add(clean_name(scheme))
            for acc in result.get("accountDetailsBulkResponse", {}).get("accountDetailsMap", {}).values():
                holdings = acc.get("equitySummary", {}).get("holdingsInfo", [])
                for h in holdings:
                    name = h.get("issuerName") or h.get("isinDescription")
                    if name:
                        keywords.add(clean_name(name))

    print("✅ Extracted Portfolio Keywords:", keywords)
    return list(keywords)

def clean_name(name):
    """Clean and simplify extracted financial name."""
    return name.replace("LIMITED", "").replace("ETF", "").strip().split()[0]

# --------------------- LLM Query Builder ---------------------

def build_news_query(keywords):
    """Use LLM to construct a clean OR-based search query."""
    if not keywords:
        return "Indian stock market OR Sensex OR Nifty OR NSE OR BSE"

    prompt = f"""
You are a financial assistant. The user has invested in the following stocks or mutual funds:

{', '.join(keywords)}

Create a search query using OR logic (e.g., "HDFC OR ICICI OR SBI") from these names.
Only include as many terms as will fit within a 100-character limit.
Prioritize well-known or large-cap entities first. 
Return only the final query string — no explanation, no quotes.
"""
    query = get_vertex_response(prompt).strip()
    print("🧠 LLM Generated Query:", query)
    return query

# --------------------- Google News RSS Fetcher ---------------------

def get_google_news_for_session(max_results=5):
    """Fetch top finance news based on portfolio using Google News RSS."""
    keywords = fetch_portfolio_names()
    query_string = build_news_query(keywords)

    trusted_sources = [
        "moneycontrol.com",
        "livemint.com",
        "economictimes.indiatimes.com"
    ]
    site_filter = ' OR '.join([f"site:{s}" for s in trusted_sources])
    full_query = f"{query_string} {site_filter}"

    encoded_query = quote_plus(full_query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    print("🔗 Google News RSS URL:", rss_url)

    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print("⚠️ No articles found.")
        return [{"title": "⚠️ No personalized news found", "link": "#"}]

    return [
        {
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "N/A")
        }
        for entry in feed.entries[:max_results]
    ]

# --------------------- CLI/Debug Mode ---------------------

if __name__ == "__main__":
    st.session_state["session_id"] = "test-user-session"  # For manual testing
    articles = get_google_news_for_session()
    for i, item in enumerate(articles, 1):
        print(f"\n{i}. {item['title']}\n{item['link']}\n🗓️ {item['published']}")

###################################################### BELOW IS WORKING CODE #################################################################

# import requests
# import streamlit as st
# import json
# from vertex_chat import get_vertex_response
# import os
# from dotenv import load_dotenv

# load_dotenv()
# NEWS_API_KEY =os.getenv("NEWSDATA_API_KEY")
# FINNHUB_API_KEY=os.getenv("FINNHUB_API_KEY")
# print(FINNHUB_API_KEY)
# # NEWS_API_KEY = "pub_dc38fb3b5f664ce2807e2eb5f5e46b76"

# def unwrap_tool_result(raw):
#     """Safely extract and decode the 'text' field from tool response."""
#     try:
#         return json.loads(raw.get("result", {}).get("text", "{}"))
#     except (TypeError, json.JSONDecodeError):
#         return {}

# def fetch_portfolio_names():
#     """Fetch names using MCP tools directly."""
#     from modules.mcp_tools import call_mcp_tool

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

#     tools = ["fetch_mf_transactions", "fetch_stock_transactions", "fetch_net_worth"]
#     keywords = set()

#     for tool in tools:
#         raw_result = call_mcp_tool(tool, session_id, base_url)
#         print(f"📦 Tool: {tool} | Raw Result: {raw_result}")
#         result = unwrap_tool_result(raw_result)

#         if tool == "fetch_mf_transactions":
#             for txn in result.get("mfTransactions", []):
#                 name = txn.get("schemeName") or txn.get("fund_name") or txn.get("scheme")
#                 if name:
#                     cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                     keywords.add(cleaned.split()[0])

#         elif tool == "fetch_stock_transactions":
#             for stk in result.get("stockTransactions", []):
#                 name = stk.get("symbol") or stk.get("stock_name")
#                 if name:
#                     cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                     keywords.add(cleaned.split()[0])

#         elif tool == "fetch_net_worth":
#             for mf in result.get("mfSchemeAnalytics", {}).get("schemeAnalytics", []):
#                 scheme = mf.get("schemeDetail", {}).get("nameData", {}).get("longName")
#                 if scheme:
#                     cleaned = scheme.replace("LIMITED", "").replace("ETF", "").strip()
#                     keywords.add(cleaned.split()[0])

#             for acc in result.get("accountDetailsBulkResponse", {}).get("accountDetailsMap", {}).values():
#                 holdings = acc.get("equitySummary", {}).get("holdingsInfo", [])
#                 for h in holdings:
#                     name = h.get("issuerName") or h.get("isinDescription")
#                     if name:
#                         cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                         keywords.add(cleaned.split()[0])

#     print("✅ Extracted Keywords:", keywords)
#     return list(keywords)

# def build_news_query(keywords):
#     if not keywords:
#         return "Indian stock market OR Sensex OR Nifty OR NSE OR BSE"

# #     prompt = f"""
# # You are a financial assistant. The user has invested in the following stocks or mutual funds:

# # {', '.join(keywords)}

# # Generate a short, clean search query using OR logic to get related news. Do not return any explanation, only the query string.
# # """ 
#     prompt = f"""
# You are a financial assistant. The user has invested in the following stocks or mutual funds:

# {', '.join(keywords)}

# Create a search query using OR logic (e.g., "HDFC OR ICICI OR SBI") from these names.

# Only include as many terms as will fit within a 100-character limit. Prioritize well-known or large-cap entities first. 

# Return only the final query string — no explanation, no quotes.
# """

#     query = get_vertex_response(prompt).strip()
#     print("🧠 Generated Query:", query)
#     return query

# def get_indian_stock_market_news():
#     keywords = fetch_portfolio_names()
#     query_string = build_news_query(keywords)
#     # fallback_clause = "OR BSE OR NSE OR financial OR market OR stock"
#     fallback_clause = "OR financial Stock"
#     full_query = f"{query_string} {fallback_clause}"
#     print(full_query )
#     print("🔍 Final Query String for News API:", query_string)

#     url = "https://newsdata.io/api/1/news"
#     params = {
#         "apikey": NEWS_API_KEY,
#         "q": full_query,
#         "language": "en",
#         "country": "in"
#     }

#     print("🌐 News API Request URL:", url)
#     # print("📨 Request Params:", params)

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         # print("📬 Raw Response:", response.text)

#         if response.status_code != 200:
#             return [{"title": f"❌ API Error {response.status_code}", "link": response.text}]

#         data = response.json()
#         results = data.get("results", [])
#         if not results:
#             return [{"title": "⚠️ No personalized news found.", "link": "#"}]

#         return results[:5]
#     except Exception as e:
#         return [{"title": "❌ Exception while fetching news", "link": str(e)}]


############################################WORKING FINAL CODE ########################


# import requests
# import streamlit as st
# import json
# from vertex_chat import get_vertex_response

# NEWS_API_KEY = "pub_dc38fb3b5f664ce2807e2eb5f5e46b76"

# def unwrap_tool_result(raw):
#     """Safely extract and decode the 'text' field from tool response."""
#     try:
#         return json.loads(raw.get("result", {}).get("text", "{}"))
#     except (TypeError, json.JSONDecodeError):
#         return {}

# def fetch_portfolio_names():
#     """Fetch names using MCP tools directly."""
#     from modules.mcp_tools import call_mcp_tool

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

#     tools = ["fetch_mf_transactions", "fetch_stock_transactions", "fetch_net_worth"]
#     keywords = set()

#     for tool in tools:
#         raw_result = call_mcp_tool(tool, session_id, base_url)
#         print(f"📦 Tool: {tool} | Raw Result: {raw_result}")
#         result = unwrap_tool_result(raw_result)

#         if tool == "fetch_mf_transactions":
#             for txn in result.get("mfTransactions", []):
#                 name = txn.get("schemeName") or txn.get("fund_name") or txn.get("scheme")
#                 if name:
#                     cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                     keywords.add(cleaned.split()[0])

#         elif tool == "fetch_stock_transactions":
#             for stk in result.get("stockTransactions", []):
#                 name = stk.get("symbol") or stk.get("stock_name")
#                 if name:
#                     cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                     keywords.add(cleaned.split()[0])

#         elif tool == "fetch_net_worth":
#             for mf in result.get("mfSchemeAnalytics", {}).get("schemeAnalytics", []):
#                 scheme = mf.get("schemeDetail", {}).get("nameData", {}).get("longName")
#                 if scheme:
#                     cleaned = scheme.replace("LIMITED", "").replace("ETF", "").strip()
#                     keywords.add(cleaned.split()[0])

#             for acc in result.get("accountDetailsBulkResponse", {}).get("accountDetailsMap", {}).values():
#                 holdings = acc.get("equitySummary", {}).get("holdingsInfo", [])
#                 for h in holdings:
#                     name = h.get("issuerName") or h.get("isinDescription")
#                     if name:
#                         cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                         keywords.add(cleaned.split()[0])

#     print("✅ Extracted Keywords:", keywords)
#     return list(keywords)

# def build_news_query(keywords):
#     if not keywords:
#         return "Indian stock market OR Sensex OR Nifty OR NSE OR BSE"

#     prompt = f"""
# You are a financial assistant. The user has invested in the following stocks or mutual funds:

# {', '.join(keywords)}

# Generate a short, clean search query using OR logic to get related news. Do not return any explanation, only the query string.
# """
#     query = get_vertex_response(prompt).strip()
#     print("🧠 Generated Query:", query)
#     return query

# def get_indian_stock_market_news():
#     keywords = fetch_portfolio_names()
#     query_string = build_news_query(keywords)

#     url = "https://newsdata.io/api/1/news"
#     params = {
#         "apikey": NEWS_API_KEY,
#         "q": query_string,
#         "language": "en",
#         "country": "in"
#     }

#     print("🌐 News API Request URL:", url)
#     print("📨 Request Params:", params)

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         print("📬 Raw Response:", response.text)

#         if response.status_code != 200:
#             return [{"title": f"❌ API Error {response.status_code}", "link": response.text}]

#         data = response.json()
#         results = data.get("results", [])
#         if not results:
#             return [{"title": "⚠️ No personalized news found.", "link": "#"}]

#         return results[:5]
#     except Exception as e:
#         return [{"title": "❌ Exception while fetching news", "link": str(e)}]


##################################### DEBUGGING CODE $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import requests
# import streamlit as st
# import json
# from vertex_chat import get_vertex_response

# NEWS_API_KEY = "pub_dc38fb3b5f664ce2807e2eb5f5e46b76"

# def fetch_portfolio_names():
#     """Fetch names using MCP tools directly."""
#     from modules.mcp_tools import call_mcp_tool

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

#     tools = ["fetch_mf_transactions", "fetch_stock_transactions", "fetch_net_worth"]
#     keywords = set()

#     for tool in tools:
#         result = call_mcp_tool(tool, session_id, base_url)

#         print(f"📦 Tool: {tool} | Raw Result: {result}")

#         # Parse string JSON if needed
#         if isinstance(result, str):
#             try:
#                 result = json.loads(result)
#             except json.JSONDecodeError:
#                 continue

#         if result:
#             if tool == "fetch_mf_transactions":
#                 for txn in result:
#                     if isinstance(txn, dict):
#                         name = txn.get("fund_name") or txn.get("scheme")
#                         if name:
#                             cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                             keywords.add(cleaned.split()[0])
#             elif tool == "fetch_stock_transactions":
#                 for stk in result:
#                     if isinstance(stk, dict):
#                         name = stk.get("stock_name") or stk.get("symbol")
#                         if name:
#                             cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                             keywords.add(cleaned.split()[0])
#             elif tool == "fetch_net_worth":
#                 mutual_funds = result.get("mutualFunds", [])
#                 if isinstance(mutual_funds, str):
#                     try:
#                         mutual_funds = json.loads(mutual_funds)
#                     except json.JSONDecodeError:
#                         mutual_funds = []
#                 for mf in mutual_funds:
#                     if isinstance(mf, dict):
#                         name = mf.get("name") or mf.get("fund_name")
#                         if name:
#                             cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                             keywords.add(cleaned.split()[0])
#                 for stk in result.get("stocks", []):
#                     if isinstance(stk, dict):
#                         name = stk.get("name") or stk.get("symbol")
#                         if name:
#                             cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                             keywords.add(cleaned.split()[0])

#     print("✅ Extracted Keywords:", keywords)
#     return list(keywords)

# def build_news_query(keywords):
#     if not keywords:
#         return "Indian stock market OR Sensex OR Nifty OR NSE OR BSE"

#     prompt = f"""
# You are a financial assistant. The user has invested in the following stocks or mutual funds:

# {', '.join(keywords)}

# Generate a short, clean search query using OR logic to get related news. Do not return any explanation, only the query string.
# """
#     query = get_vertex_response(prompt).strip()
#     print("🧠 Generated Query:", query)
#     return query

# def get_indian_stock_market_news():
#     keywords = fetch_portfolio_names()
#     query_string = build_news_query(keywords)

#     url = "https://newsdata.io/api/1/news"
#     params = {
#         "apikey": NEWS_API_KEY,
#         "q": query_string,
#         "language": "en",
#         "country": "in"
#     }

#     print("🌐 News API Request URL:", url)
#     print("📨 Request Params:", params)

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         print("📬 Raw Response:", response.text)

#         if response.status_code != 200:
#             return [{"title": f"❌ API Error {response.status_code}", "link": response.text}]

#         data = response.json()
#         results = data.get("results", [])
#         if not results:
#             return [{"title": "⚠️ No personalized news found.", "link": "#"}]

#         return results[:5]
#     except Exception as e:
#         return [{"title": "❌ Exception while fetching news", "link": str(e)}]


################################################### WORKING #######################################
# import requests
# import streamlit as st
# import json
# from vertex_chat import get_vertex_response

# NEWS_API_KEY = "pub_dc38fb3b5f664ce2807e2eb5f5e46b76"

# def extract_keywords_from_user_data():
#     data = st.session_state.get("fetched_data", {})
#     keywords = set()

#     # Ensure data is a dict
#     if isinstance(data, str):
#         try:
#             data = json.loads(data)
#         except json.JSONDecodeError:
#             return list(keywords)

#     for txn in data.get("fetch_mf_transactions", []):
#         if isinstance(txn, dict):
#             name = txn.get("fund_name") or txn.get("scheme")
#             if name:
#                 cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                 keywords.add(cleaned.split()[0])

#     for stk in data.get("fetch_stock_transactions", []):
#         if isinstance(stk, dict):
#             name = stk.get("stock_name") or stk.get("symbol")
#             if name:
#                 cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                 keywords.add(cleaned.split()[0])

#     for mf in data.get("fetch_net_worth", {}).get("mutualFunds", []):
#         if isinstance(mf, dict):
#             name = mf.get("name") or mf.get("fund_name")
#             if name:
#                 cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                 keywords.add(cleaned.split()[0])

#     for stk in data.get("fetch_net_worth", {}).get("stocks", []):
#         if isinstance(stk, dict):
#             name = stk.get("name") or stk.get("symbol")
#             if name:
#                 cleaned = name.replace("LIMITED", "").replace("ETF", "").strip()
#                 keywords.add(cleaned.split()[0])

#     return list(keywords)

# def build_news_query(keywords):
#     if not keywords:
#         return "Indian stock market OR Sensex OR Nifty OR NSE OR BSE"

#     prompt = f"""
# You are a financial assistant. The user has invested in the following stocks or mutual funds:

# {', '.join(keywords)}

# Generate a short, clean search query using OR logic to get related news. Do not return any explanation, only the query string.
# """
#     return get_vertex_response(prompt).strip()

# def get_indian_stock_market_news():
#     keywords = extract_keywords_from_user_data()
#     query_string = build_news_query(keywords)

#     url = "https://newsdata.io/api/1/news"
#     params = {
#         "apikey": NEWS_API_KEY,
#         "q": query_string,
#         "language": "en",
#         "country": "in"
#     }

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         if response.status_code != 200:
#             return [{"title": f"❌ API Error {response.status_code}", "link": response.text}]

#         data = response.json()
#         results = data.get("results", [])
#         if not results:
#             return [{"title": "⚠️ No personalized news found.", "link": "#"}]

#         return results[:5]
#     except Exception as e:
#         return [{"title": "❌ Exception while fetching news", "link": str(e)}]




# import requests
# import streamlit as st
# from vertex_chat import get_vertex_response  # Your Gemini wrapper from earlier

# NEWS_API_KEY = "pub_dc38fb3b5f664ce2807e2eb5f5e46b76"

# # ✅ Extract relevant stock/mutual fund keywords from MCP data
# def extract_portfolio_keywords():
#     data = st.session_state.get("fetched_data", {})
#     keywords = set()

#     # Mutual funds and stocks from fetch_mf_transactions
#     for txn in data.get("fetch_mf_transactions", []):
#         name = txn.get("fund_name") or txn.get("scheme")
#         if name:
#             keywords.add(name.split()[0])

#     for stk in data.get("fetch_stock_transactions", []):
#         name = stk.get("stock_name") or stk.get("symbol")
#         if name:
#             keywords.add(name.split()[0])

#     # Also scan fetch_net_worth if available
#     networth_data = data.get("fetch_net_worth", {})
#     mf_assets = networth_data.get("mutualFunds", [])
#     stock_assets = networth_data.get("stocks", [])

#     for mf in mf_assets:
#         name = mf.get("name") or mf.get("fund_name")
#         if name:
#             keywords.add(name.split()[0])

#     for stock in stock_assets:
#         name = stock.get("name") or stock.get("symbol")
#         if name:
#             keywords.add(name.split()[0])

#     return list(keywords)

# # ✅ Ask LLM to convert keywords into a clean OR search string
# def build_news_query_from_portfolio(keywords: list[str]) -> str:
#     if not keywords:
#         return "Indian stock market OR Sensex OR Nifty OR NSE OR BSE"

#     prompt = f"""
# You are a financial assistant. The user owns or has invested in the following companies or mutual funds:

# {', '.join(keywords)}

# Construct a clean news search query using OR logic for a stock news API. Keep it short and relevant.
# Just return the final search string for the 'q' parameter (no other text).
# """
#     return get_vertex_response(prompt).strip()

# # ✅ Fetch Indian stock market news using the generated query
# def get_indian_stock_market_news():
#     keywords = extract_portfolio_keywords()
#     query_string = build_news_query_from_portfolio(keywords)

#     url = "https://newsdata.io/api/1/news"
#     params = {
#         "apikey": NEWS_API_KEY,
#         "q": query_string,
#         "language": "en",
#         "country": "in"
#     }

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         if response.status_code != 200:
#             return [{"title": "Error fetching news", "link": f"{response.status_code}: {response.text}"}]
#         return response.json().get("results", [])[:5]
#     except Exception as e:
#         return [{"title": "❌ Exception while fetching news", "link": str(e)}]