# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html
# import asyncio # Import asyncio for running async agent calls

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # Add the 'utils' directory to the Python path
# # This is derived from the image showing 'mcp_clie' pointing to '~/Downloads/UI 4/utils'
# # Assuming 'UI 4' is your project_root here.
# utils_path = os.path.join(project_root, "utils")
# if utils_path not in sys.path:
#     sys.path.append(utils_path)


# # --- Module Imports ---
# # Standard modules
# from modules.summary_client import get_financial_summary
# from modules import ai_selector, ui_components
# from modules.mcp_tools import load_all_tools
# from modules.news_client import get_google_news_for_session
# from modules.pdf_writer import generate_summary_pdf

# # KPI Definitions
# from modules.kpi_definitions import banking, epf, credit, net_worth, stock
# from modules.kpi_definitions.banking import get_selected_banking_kpis, fetch_cleaned_bank_transactions
# from modules.kpi_definitions.credit import extract_credit_kpis, fetch_cleaned_credit_report
# from modules.kpi_definitions.epf import extract_epf_kpis, fetch_cleaned_epf_report
# from modules.kpi_definitions.net_worth import extract_net_worth_kpis, fetch_cleaned_net_worth, basic_benchmark
# from modules.kpi_definitions.stock import fetch_cleaned_stock_data, extract_stock_kpis
# from modules.kpi_definitions.strategic_kpi import strategic_data # Ensure this is used if needed


# # --- NEW: Import the ADK agent call function from agent.py ---
# # Make sure your agent file is named 'agent.py' in the root directory (UI 4)
# # If it's named 'agentt.py', change 'agent' to 'agentt' below.
# from DashAI.agent import call_agent_async


# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             /* Hide Streamlit elements */
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             /* Fixed Header for DashAI branding and logout */
#             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85); /* Slightly transparent for blur effect */
#                 backdrop-filter: blur(12px); /* Blur behind the header */
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000; /* Ensure header is on top */
#                 border-bottom: 1px solid #30363D; /* Subtle separator */
#             }
#             /* Header Logo and Welcome Message Styling */
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             /* Main Content Padding adjustment */
#             .main-content { padding-top: 2px; }
#             /* Chat Log Container Styling */
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             /* Info Box Styling (for News and Summary) */
#             .info-box { background-color: #152320; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#             /* Gradient Divider Style */
#             .gradient-divider {
#                 height: 2px; /* Controls the thickness of the line */
#                 width: 100%;
#                 background-image: linear-gradient(to right, #081411, #00b6a1, #081411);
#                 border: none; /* Removes any default border */
#                 margin: 2rem 0; /* Adds vertical space, similar to st.divider() */
#             }
#             /* Button Styling */
#             [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)
#     # --- Main Function ---
# def main():
#     apply_layout_styling()

#     # Ensure session_id and user_id are set in st.session_state
#     if "session_id" not in st.session_state:
#         st.session_state["session_id"] = str(uuid.uuid4()) # Generate a new UUID if not set
#     if "user_id" not in st.session_state:
#         st.session_state["user_id"] = "guest_user" # Default user ID if not logged in

#     session_id = st.session_state.session_id
#     user_id = st.session_state.user_id # Get the user_id from session state

#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url) # Load tools for the current session

#     # Fetch all required data
#     banking_data = fetch_cleaned_bank_transactions(session_id, base_url)
#     credit_data = fetch_cleaned_credit_report(session_id, base_url)
#     cleaned_epf_data = fetch_cleaned_epf_report(session_id, base_url)
#     cleaned_networth_data = fetch_cleaned_net_worth(session_id, base_url)
#     cleaned_stock_data = fetch_cleaned_stock_data(session_id, base_url)

#     # Store fetched data in session state for the agent to access (if needed by tools)
#     st.session_state["fetched_data"] = {
#         "banking": banking_data,
#         "credit": credit_data,
#         "epf": cleaned_epf_data,
#         "net_worth": cleaned_networth_data,
#         "stock": cleaned_stock_data
#     }

#     # Extract KPIs only if data is present
#     banking_kpis = get_selected_banking_kpis(banking_data) if banking_data else {}
#     credit_kpis = extract_credit_kpis(credit_data) if credit_data else {}
#     epf_kpis = extract_epf_kpis(cleaned_epf_data) if cleaned_epf_data else {} # Ensure handling of empty data
#     net_worth_kpis = extract_net_worth_kpis(cleaned_networth_data) if cleaned_networth_data else {}
#     stock_kpis = extract_stock_kpis(cleaned_stock_data) if cleaned_stock_data else {}

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 display_user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {display_user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key] # Clear all session state on logout
#                     st.switch_page("login.py")
# # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # Construct data to pass to Gemini-based selector for KPI insights
#         strategic_kpis = {
#             "banking": banking_kpis,
#             "credit": credit_kpis,
#             "epf": epf_kpis,
#             "net_worth": net_worth_kpis,
#             "stock": stock_kpis
#         }

#         # Dynamically generate kpi_map for rendering KPI cards
#         kpi_map = {}
#         for category, kpis in strategic_kpis.items():
#             for kpi_name, kpi_info in kpis.items():
#                 if isinstance(kpi_info, dict) and 'value' in kpi_info:
#                     kpi_map[kpi_name] = {
#                         'function': lambda name=kpi_name, cat_kpis=kpis: cat_kpis.get(name, {'value': 0, 'change': ''}),
#                         'title': kpi_name.replace('_', ' ').title(),
#                         'unit': kpi_info.get('unit', ''),
#                         'icon': kpi_info.get('icon', ''),
#                     }
#                     if 'benchmark' in kpi_info:
#                         kpi_map[kpi_name]['benchmark_key'] = 'benchmark'
#                     elif 'change' in kpi_info and (kpi_info['change'].startswith('⚠️') or kpi_info['change'].startswith('✅') or kpi_info['change'].endswith('⬇️') or kpi_info['change'].endswith('⬆️') or kpi_info['change'].endswith('➡️')):
#                         kpi_map[kpi_name]['benchmark_key'] = 'change'
#                     elif 'icon' in kpi_info and kpi_info['icon'] == '⚠️':
#                          kpi_map[kpi_name]['benchmark_key'] = 'icon'

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         kpi_columns = st.columns(4)
#         recommended_info = ai_selector.get_top_kpis_with_summary(strategic_kpis)
#         recommended_kpis = recommended_info.get("recommended_kpis", [])

#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map and i < len(kpi_columns):
#                 with kpi_columns[i]:
#                     kpi_config = kpi_map[kpi_name]
#                     data = kpi_config["function"]()

#                     benchmark_text_with_icon = None
#                     if 'benchmark_key' in kpi_config:
#                         raw_benchmark_data = data.get(kpi_config['benchmark_key'])
#                         if raw_benchmark_data:
#                             benchmark_text_with_icon = str(raw_benchmark_data)
#                     elif 'benchmark' in kpi_config:
#                         benchmark_text_with_icon = kpi_config['benchmark']

#                     kpi_change_value = data.get("change", "")

#                     ui_components.render_kpi_card(
#                         title=kpi_config["title"],
#                         value=data["value"],
#                         unit=kpi_config["unit"],
#                         change=kpi_change_value,
#                         icon=kpi_config["icon"],
#                         benchmark=benchmark_text_with_icon
#                     )

#         st.write("")

#         # --- News and Summary Boxes ---
#         col1, col2 = st.columns(2)
#         with col1:
#             news_articles = get_google_news_for_session()
#             news_html = "<h3>📰 Personalized Market News</h3><ul>"
#             if news_articles:
#                 for article in news_articles:
#                     title = html.escape(article.get("title", "No Title"))
#                     link = html.escape(article.get("link", "#"))
#                     news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
#             else:
#                 news_html += "<li>No personalized news found.</li>"
#             news_html += "</ul>"
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         with col2:
#             llm_summary_text = get_financial_summary()

#             summary_content = f"""
#                 <h3>💡 AI Summary</h3>
#                 <p>{llm_summary_text}</p>
#             """

#             st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)

#             # Generate and download the financial summary PDF
#             pdf_file = generate_summary_pdf(llm_summary_text)
#             with open(pdf_file, "rb") as f:
#                 st.download_button(
#                     label="📥 Download Financial Summary as PDF",
#                     data=f,
#                     file_name="Financial_Summary.pdf",
#                     mime="application/pdf"
#                 )

#         # --- Chatbot ---
#         st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         # Display messages in reverse order for chat log
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})

#             try:
#                 # --- Calling the ADK agent ---
#                 # Pass the Streamlit session_id and user_id to the async agent call
#                 response = asyncio.run(call_agent_async(
#                     prompt,
#                     st.session_state.session_id,
#                     st.session_state.user_id
#                 ))
#             except Exception as e:
#                 response = f"⚠️ Error with DashAI Agent: {e}"
#                 print(f"Error calling ADK agent: {e}") # Print error to console for debugging

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun() # Rerun to display new message

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# # This block ensures that a user must be logged in to access the dashboard.
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("login.py", label="🔙 Return to Login")
#     st.stop() # Stop execution if not logged in
# else:
#     main() # Run the main dashboard function                    















################################################            ##################################################
import streamlit as st
import sys
import os
import json
import uuid
import html
from modules.summary_client import get_financial_summary

# --- Pathing Logic ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# --- Module Imports ---
from modules import ai_selector, ui_components
from modules.kpi_definitions import investments, net_worth, banking, credit
from modules.mcp_tools import load_all_tools
# from modules.news_client import get_indian_stock_market_news
from modules.news_client import get_google_news_for_session


from vertex_chat import get_vertex_response

#################### NIRPU ##########
from modules.kpi_definitions.strategic_kpi import strategic_data
import re  # Import the re module for regular expressions
# --- Module Imports ---
from modules import ai_selector, ui_components
from modules.kpi_definitions import banking,epf, credit,net_worth,stock
from modules.mcp_tools import load_all_tools
from vertex_chat import get_vertex_response

from modules.kpi_definitions.banking import get_selected_banking_kpis,fetch_cleaned_bank_transactions
from modules.kpi_definitions.credit import extract_credit_kpis,fetch_cleaned_credit_report
from modules.kpi_definitions.epf import extract_epf_kpis, fetch_cleaned_epf_report
from modules.kpi_definitions.net_worth import extract_net_worth_kpis, fetch_cleaned_net_worth,basic_benchmark
from modules.kpi_definitions.stock import fetch_cleaned_stock_data,extract_stock_kpis
# from modules.kpi_definitions.net_worth import classify_status
# --- Page Configuration ---
st.set_page_config(
    page_title="DashAI - Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Layout Styling ---
def apply_layout_styling():
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
                display: none;
            }
            header[data-testid="stHeader"] {
                display: none !important;
                visibility: hidden !important;
            }
            div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                width: 100%;
                background: rgba(10, 10, 10, 0.85);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                padding: 1rem 2.5rem;
                z-index: 1000;
                border-bottom: 1px solid #30363D;
            }
            .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
            .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
            .main-content { padding-top: 2px; }
            .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
            .message-container { width: 100%; margin-bottom: 0.5rem; }
            .user-message { text-align: right; color: #E0E0E0; }
            .assistant-message { text-align: left; color: #A0AEC0; }
            .info-box { background-color: #152320; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
               /* --- NEW: Gradient Divider Style --- */
            .gradient-divider {
                height: 2px; /* Controls the thickness of the line */
                width: 100%;
                background-image: linear-gradient(to right, #081411, #00b6a1, #081411);
                border: none; /* Removes any default border */
                margin: 2rem 0; /* Adds vertical space, similar to st.divider() */
            }
            [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
            [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
        </style>
    """, unsafe_allow_html=True)

from modules.pdf_writer import generate_summary_pdf #, generate_chat_summary_pdf

# --- Main Function ---
def main():
    apply_layout_styling()

    session_id = st.session_state.get("session_id")
    base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
    load_all_tools(session_id, base_url)

    # Fetch all required data
    banking_data = fetch_cleaned_bank_transactions(session_id, base_url)
    credit_data = fetch_cleaned_credit_report(session_id, base_url)
    cleaned_epf_data = fetch_cleaned_epf_report(session_id, base_url)
    cleaned_networth_data = fetch_cleaned_net_worth(session_id, base_url)
    cleaned_stock_data = fetch_cleaned_stock_data(session_id, base_url)

    # Extract KPIs only if data is present
    banking_kpis = get_selected_banking_kpis(banking_data) if banking_data else {}
    credit_kpis = extract_credit_kpis(credit_data) if credit_data else {}
    epf_kpis = extract_epf_kpis(cleaned_epf_data)
    net_worth_kpis = extract_net_worth_kpis(cleaned_networth_data) if cleaned_networth_data else {}
    stock_kpis = extract_stock_kpis(cleaned_stock_data) if cleaned_stock_data else {}

    # --- HEADER ---
    header = st.container()
    with header:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
        with col2:
            sub_col1, sub_col2 = st.columns([3, 1])
            with sub_col1:
                user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
                st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
            with sub_col2:
                if st.button("Logout", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.switch_page("login.py")

    # --- MAIN CONTENT ---
    main_content = st.container()
    with main_content:
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        # Construct data to pass to Gemini-based selector
        strategic_kpis = {
                    "banking": banking_kpis,
                    "credit": credit_kpis,
                    "epf": epf_kpis,
                    "net_worth": net_worth_kpis,
                    "stock": stock_kpis
                    }
        # Dynamically generate kpi_map
        kpi_map = {}
        for category, kpis in strategic_kpis.items():
            for kpi_name, kpi_info in kpis.items():
                # Ensure kpi_info is a dictionary and has 'value' key
                if isinstance(kpi_info, dict) and 'value' in kpi_info:
                    kpi_map[kpi_name] = {
                        'function': lambda name=kpi_name, cat_kpis=kpis: cat_kpis.get(name, {'value': 0, 'change': ''}),
                        'title': kpi_name.replace('_', ' ').title(), # Basic title generation
                        'unit': kpi_info.get('unit', ''),
                        'icon': kpi_info.get('icon', ''),
                    }
                    # Add benchmark_key if it exists in the original data
                    if 'benchmark' in kpi_info:
                        kpi_map[kpi_name]['benchmark_key'] = 'benchmark'
                    elif 'change' in kpi_info and (kpi_info['change'].startswith('⚠️') or kpi_info['change'].startswith('✅') or kpi_info['change'].endswith('⬇️') or kpi_info['change'].endswith('⬆️') or kpi_info['change'].endswith('➡️')):
                        kpi_map[kpi_name]['benchmark_key'] = 'change'
                    elif 'icon' in kpi_info and kpi_info['icon'] == '⚠️':
                         kpi_map[kpi_name]['benchmark_key'] = 'icon'
        # --- KPIs ---
        st.markdown("### Your AI-Recommended Insights")
        # st.write("")
        kpi_columns = st.columns(4)
        recommended_info = ai_selector.get_top_kpis_with_summary(strategic_kpis)
        recommended_kpis = recommended_info.get("recommended_kpis", [])

        for i, kpi_name in enumerate(recommended_kpis):
            if kpi_name in kpi_map and i < len(kpi_columns):
             with kpi_columns[i]:
                kpi_config = kpi_map[kpi_name]
                data = kpi_config["function"]()

                # Determine the benchmark text to display
                benchmark_text_with_icon = None
                if 'benchmark_key' in kpi_config:
                    raw_benchmark_data = data.get(kpi_config['benchmark_key'])
                    if raw_benchmark_data:
                        benchmark_text_with_icon = str(raw_benchmark_data)
                elif 'benchmark' in kpi_config: # Handle explicit 'benchmark' key from kpi_map
                    benchmark_text_with_icon = kpi_config['benchmark']


                # Get the change value for the KPI
                kpi_change_value = data.get("change", "")


                ui_components.render_kpi_card(
                    title=kpi_config["title"],
                    value=data["value"],
                    unit=kpi_config["unit"],
                    change=kpi_change_value, # Pass the original change value
                    icon=kpi_config["icon"],
                    benchmark=benchmark_text_with_icon # Pass the determined benchmark
                )

        # kpi_map = {
        #     'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
        #     'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
        #     'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
        #     'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
        # }
        # recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
        # for i, kpi_name in enumerate(recommended_kpis):
        #     if kpi_name in kpi_map:
        #         with kpi_columns[i]:
        #             data = kpi_map[kpi_name]['function']()
        #             ui_components.render_kpi_card(
        #                 title=kpi_map[kpi_name]['title'], value=data['value'],
        #                 unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
        #             )

        st.write("")

        # --- News and Summary Boxes ---
        col1, col2 = st.columns(2)
        with col1:
            news_articles = get_google_news_for_session()
            news_html = "<h3>📰 Personalized Market News</h3><ul>"
            if news_articles:
                for article in news_articles:
                    title = html.escape(article.get("title", "No Title"))
                    link = html.escape(article.get("link", "#"))
                    news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
            else:
                news_html += "<li>No personalized news found.</li>"
            news_html += "</ul>"
            st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

        with col2:
            llm_summary_text = get_financial_summary() 

            summary_content = f"""
                <h3>💡 AI Summary</h3>
                <p>{llm_summary_text}</p>
            """
           
            st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)

            # Generate and download the financial summary PDF
            pdf_file = generate_summary_pdf(llm_summary_text)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📥 Download Financial Summary as PDF",
                    data=f,
                    file_name="Financial_Summary.pdf",
                    mime="application/pdf"
                )

        # --- Chatbot ---
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        st.markdown("### Chat with DashAI")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        message_html = ""
        for msg in reversed(st.session_state.messages):
            escaped_content = html.escape(msg['content'])
            message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
        st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

        if prompt := st.chat_input("Ask DashAI about your finances..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
                gemini_prompt = f"""
You are a finance assistant. Use the following data to answer the user's question.

User Question:
{prompt}

Financial Data:
{context}
"""
                response = get_vertex_response(gemini_prompt)
            except Exception as e:
                response = f"⚠️ Error: {e}"

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# --- ACCESS GUARD ---
if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
    st.error("Session missing or expired. Please login again.")
    st.page_link("login.py", label="🔙 Return to Login") 
    st.stop()
else:
    main()





# ################################### 7th pdf summmary function ###############
# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html
# from modules.summary_client import get_financial_summary

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# # from modules.news_client import get_indian_stock_market_news
# from modules.news_client import get_google_news_for_session

# from vertex_chat import get_vertex_response
# from modules.pdf_writer import generate_summary_pdf, pdf_financial_summary  # Ensure pdf function is imported

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 2px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             .info-box { background-color: #152320; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#             .gradient-divider {
#                 height: 2px;
#                 width: 100%;
#                 background-image: linear-gradient(to right, #081411, #00b6a1, #081411);
#                 border: none;
#                 margin: 2rem 0;
#             }
#             [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("login.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         st.write("")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.write("")

#         # --- News and Summary Boxes ---
#         col1, col2 = st.columns(2)
#         with col1:
#             news_articles = get_google_news_for_session()
#             news_html = "<h3>📰 Personalized Market News</h3><ul>"
#             if news_articles:
#                 for article in news_articles:
#                     title = html.escape(article.get("title", "No Title"))
#                     link = html.escape(article.get("link", "#"))
#                     news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
#             else:
#                 news_html += "<li>No personalized news found.</li>"
#             news_html += "</ul>"
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         with col2:
#             llm_summary_text = get_financial_summary() 

#             summary_content = f"""
#                 <h3>💡 AI Summary</h3>
#                 <p>{llm_summary_text}</p>
#             """
           
#             st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)

#             # --- Generate and download the financial summary PDF ---
#             pdf_file = pdf_financial_summary()  # Call the pdf_financial_summary function here
#             with open(pdf_file, "rb") as f:
#                 st.download_button(
#                     label="📥 Download Financial Summary as PDF",
#                     data=f,
#                     file_name="Financial_Summary.pdf",
#                     mime="application/pdf"
#                 )

#         # --- Chatbot ---
#         st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                 gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                 response = get_vertex_response(gemini_prompt)
#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("login.py", label="🔙 Return to Login") 
#     st.stop()
# else:
#     main()



# ##################################################  6th Version#######################################################
# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html
# from modules.summary_client import get_financial_summary

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# # from modules.news_client import get_indian_stock_market_news
# from modules.news_client import get_google_news_for_session


# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 2px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             .info-box { background-color: #152320; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#                /* --- NEW: Gradient Divider Style --- */
#             .gradient-divider {
#                 height: 2px; /* Controls the thickness of the line */
#                 width: 100%;
#                 background-image: linear-gradient(to right, #081411, #00b6a1, #081411);
#                 border: none; /* Removes any default border */
#                 margin: 2rem 0; /* Adds vertical space, similar to st.divider() */
#             }
#             [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# from modules.pdf_writer import generate_summary_pdf #, generate_chat_summary_pdf

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("login.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         st.write("")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.write("")

#         # --- News and Summary Boxes ---
#         col1, col2 = st.columns(2)
#         with col1:
#             news_articles = get_google_news_for_session()
#             news_html = "<h3>📰 Personalized Market News</h3><ul>"
#             if news_articles:
#                 for article in news_articles:
#                     title = html.escape(article.get("title", "No Title"))
#                     link = html.escape(article.get("link", "#"))
#                     news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
#             else:
#                 news_html += "<li>No personalized news found.</li>"
#             news_html += "</ul>"
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         with col2:
#             llm_summary_text = get_financial_summary() 

#             summary_content = f"""
#                 <h3>💡 AI Summary</h3>
#                 <p>{llm_summary_text}</p>
#             """
           
#             st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)

#             # Generate and download the financial summary PDF
#             pdf_file = generate_summary_pdf(llm_summary_text)
#             with open(pdf_file, "rb") as f:
#                 st.download_button(
#                     label="📥 Download Financial Summary as PDF",
#                     data=f,
#                     file_name="Financial_Summary.pdf",
#                     mime="application/pdf"
#                 )

#         # --- Chatbot ---
#         st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                 gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                 response = get_vertex_response(gemini_prompt)
#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("login.py", label="🔙 Return to Login") 
#     st.stop()
# else:
#     main()




# # ##################################################  5th Version Karthik #######################################################
# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html
# from modules.summary_client import get_financial_summary

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# # from modules.news_client import get_indian_stock_market_news
# from modules.news_client import get_google_news_for_session


# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 2px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             .info-box { background-color: #152320; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#                /* --- NEW: Gradient Divider Style --- */
#             .gradient-divider {
#                 height: 2px; /* Controls the thickness of the line */
#                 width: 100%;
#                 background-image: linear-gradient(to right, #081411, #00b6a1, #081411);
#                 border: none; /* Removes any default border */
#                 margin: 2rem 0; /* Adds vertical space, similar to st.divider() */
#             }
#             [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("login.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         st.write("")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.write("")

#         # --- News and Summary Boxes ---
#         col1, col2 = st.columns(2)
#         with col1:
#             news_articles = get_google_news_for_session()
#             # news_articles = get_indian_stock_market_news()
#             news_html = "<h3>📰 Personalized Market News</h3><ul>"
#             if news_articles:
#                 for article in news_articles:
#                     title = html.escape(article.get("title", "No Title"))
#                     link = html.escape(article.get("link", "#"))
#                     news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
#             else:
#                 news_html += "<li>No personalized news found.</li>"
#             news_html += "</ul>"
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         with col2:
#             llm_summary_text = get_financial_summary() 

#             summary_content = f"""
#                 <h3>💡 AI Summary</h3>
#                 <p>{llm_summary_text}</p>
#             """
   
#             st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)

#         # --- Chatbot ---
#         # st.divider()
#         st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                 gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                 response = get_vertex_response(gemini_prompt)
#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("login.py", label="🔙 Return to Login")
#     st.stop()
# else:
#     main()






















#  # ##################################################  Fourth VERSION (Updated with News)-PDF integration  #######################################################
# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# from modules.news_client import get_google_news_for_session
# from modules.summary_client import get_financial_summary
# from modules.pdf_writer import generate_summary_pdf, generate_chat_summary_pdf
# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             .info-box { background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#             [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     if not session_id:
#         st.error("Session ID missing. Please login again to continue.")
#         st.page_link("Home.py", label="🔙 Return to Login")
#         st.stop()

#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         st.markdown("### Your AI-Recommended Insights")
#         st.write("")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.write("")

#         col1, col2 = st.columns(2)
#         with col1:
#             news_articles = get_google_news_for_session()
#             if len(news_articles) == 1 and news_articles[0]["title"].startswith("⚠️"):
#                 st.warning("Personalized news could not be generated. Please ensure you are logged in and portfolio data is available.")
#                 st.stop()

#             news_html = "<h3>📰 Personalized Market News</h3><ul>"
#             for article in news_articles:
#                 title = html.escape(article.get("title", "No Title"))
#                 link = html.escape(article.get("link", "#"))
#                 news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
#             news_html += "</ul>"
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         with col2:
#             summary_text = get_financial_summary()
#             st.markdown(f"""
#                 <div class="info-box">
#                     <h3>💡 AI Summary</h3>
#                     <p>{summary_text}</p>
#                 </div>
#             """, unsafe_allow_html=True)
#         pdf_file = generate_summary_pdf(summary_text)
#         with open(pdf_file, "rb") as f:
#             st.download_button(
#                 label="📥 Download Summary as PDF",
#                 data=f,
#                 file_name="Financial_Summary.pdf",
#                 mime="application/pdf"
#             )

#         st.divider()
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})

#             if prompt.lower().strip() in ["give me into pdf", "export to pdf", "save chat as pdf"]:
#                 chat_pdf = generate_chat_summary_pdf(st.session_state.messages)
#                 with open(chat_pdf, "rb") as f:
#                     st.download_button(
#                         label="📄 Click to Download Your Chat PDF",
#                         data=f,
#                         file_name="Chat_Summary.pdf",
#                         mime="application/pdf",
#                         key="chat_pdf_dl_btn"
#                     )
#             else:
#                 try:
#                     context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                     gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                     response = get_vertex_response(gemini_prompt)
#                 except Exception as e:
#                     response = f"⚠️ Error: {e}"
#                 st.session_state.messages.append({"role": "assistant", "content": response})
#                 st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("Home.py", label="🔙 Return to Login")
#     st.stop()
# else:
#     main()

##################################################  Fourth VERSION (Updated with News)  #######################################################
# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# # from modules.news_client import get_indian_stock_market_news
# from modules.news_client import get_google_news_for_session
# from modules.summary_client import get_financial_summary
# from modules.pdf_writer import generate_summary_pdf

# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             .info-box { background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#             [data-testid="stButton"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid="stButton"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         st.write("")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.write("")

#         # --- News and Summary Boxes ---
#         col1, col2 = st.columns(2)
#         with col1:
#             news_articles = get_google_news_for_session()
#             # news_articles = get_indian_stock_market_news()
#             news_html = "<h3>📰 Personalized Market News</h3><ul>"
#             if news_articles:
#                 for article in news_articles:
#                     title = html.escape(article.get("title", "No Title"))
#                     link = html.escape(article.get("link", "#"))
#                     news_html += f'<li><strong>{title}</strong><br><a href="{link}" target="_blank">Read more</a></li>'
#             else:
#                 news_html += "<li>No personalized news found.</li>"
#             news_html += "</ul>"
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         # with col2:
#         #     summary_content = """
#         #         <h3>💡 AI Summary</h3>
#         #         <p>Placeholder for AI-generated summary based on portfolio health.</p>
#         #     """
#         #     st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)
#         with col2:
#             summary_text = get_financial_summary()
#             st.markdown(f"""
#                 <div class="info-box">
#                     <h3>💡 AI Summary</h3>
#                     <p>{summary_text}</p>
#                 </div>
#             """, unsafe_allow_html=True)
#         # Generate PDF and offer download
#         pdf_file = generate_summary_pdf(summary_text)
#         # pdf_file = generate_summary_pdf(summary_text, news_articles)
#         with open(pdf_file, "rb") as f:
#             st.download_button(
#                 label="📥 Download Summary as PDF",
#                 data=f,
#                 file_name="Financial_Summary.pdf",
#                 mime="application/pdf"
#             )


#         # --- Chatbot ---
#         st.divider()
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                 gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                 response = get_vertex_response(gemini_prompt)
#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("Home.py", label="🔙 Return to Login")
#     st.stop()
# else:
#     main()












# ##################################################  Fourth VERSION  #######################################################
# import streamlit as st
# import sys
# import os
# import json
# import uuid
# import html

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# from vertex_chat import get_vertex_response

# from modules.news_client import get_indian_stock_market_news

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid=\"stSidebar\"], [data-testid=\"stToolbar\"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid=\"stHeader\"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid=\"stAppViewContainer\"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             .info-box { background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 1.5rem; height: 250px; overflow-y: auto; }
#             [data-testid=\"stButton\"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid=\"stButton\"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         st.write("")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.write("")

#         # --- News and Summary Boxes ---
#         col1, col2 = st.columns(2)
#         with col1:
#             news_html = """
#                 <h3>📰 Latest News</h3>
#                 <ul>
#                     <li><strong>Market Update:</strong> Tech stocks see a slight dip after recent rally.</li>
#                     <li><strong>Your Holdings:</strong> Company XYZ announces record earnings.</li>
#                 </ul>
#             """
#             st.markdown(f'<div class="info-box">{news_html}</div>', unsafe_allow_html=True)

#         with col2:
#             summary_content = """
#                 <h3>💡 AI Summary</h3>
#                 <p>Placeholder for AI-generated summary.</p>
#             """
#             st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)

#         # --- Chatbot ---
#         st.divider()
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             escaped_content = html.escape(msg['content'])
#             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                 gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                 response = get_vertex_response(gemini_prompt)
#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("Home.py", label="🔙 Return to Login")
#     st.stop()
# else:
#     main()

# ##################################################  THIRD VERSION  #######################################################
# import streamlit as st
# import sys
# import os
# import json
# import uuid

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from modules.mcp_tools import load_all_tools
# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid=\"stSidebar\"], [data-testid=\"stToolbar\"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid=\"stHeader\"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid=\"stAppViewContainer\"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             [data-testid=\"stButton\"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid=\"stButton\"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     load_all_tools(session_id, base_url)

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.divider()
#         st.markdown("### Chat with DashAI")

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             message_html += f"<div class='message-container {msg['role']}-message'>{msg['content']}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})

#             try:
#                 context = json.dumps(st.session_state.get("fetched_data", {}), indent=2)
#                 gemini_prompt = f"""
# You are a finance assistant. Use the following data to answer the user's question.

# User Question:
# {prompt}

# Financial Data:
# {context}
# """
#                 response = get_vertex_response(gemini_prompt)
#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("Home.py", label="🔙 Return to Login")
#     st.stop()
# else:
#     main()




################################################### SECOND VERSION ##########################################################
# import streamlit as st
# import sys
# import os
# import requests
# import json
# import uuid

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid=\"stSidebar\"], [data-testid=\"stToolbar\"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid=\"stHeader\"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid=\"stAppViewContainer\"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             [data-testid=\"stButton\"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid=\"stButton\"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     # --- SESSION SETUP ---
#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.divider()
#         st.markdown("### Chat with DashAI")

#         # --- CHAT LOG ---
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             message_html += f"<div class='message-container {msg['role']}-message'>{msg['content']}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         # --- CHAT INPUT ---
#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 tool_url = f"{base_url}/mcp/stream"
#                 params = {"toolName": "fetch_net_worth", "sessionId": session_id}
#                 resp = requests.get(tool_url, params=params)

#                 # --- PARSE RESPONSE ---
#                 if "application/json" in resp.headers.get("Content-Type", ""):
#                     tool_result = resp.json()
#                 else:
#                     try:
#                         tool_result = json.loads(resp.text)
#                     except:
#                         tool_result = None

#                 # --- SUMMARIZE W/ GEMINI ---
#                 if tool_result:
#                     tool_text = json.dumps(tool_result, indent=2)
#                     gemini_prompt = f"""
# You are a finance assistant. Summarize the following net worth information in simple language:

# {tool_text}
# """
#                     response = get_vertex_response(gemini_prompt)
#                 else:
#                     login_url = f"{base_url}/mockWebPage?sessionId={session_id}"
#                     response = (
#                         "⚠️ Unable to access net worth. "
#                         f"Please [authenticate with Fi MCP]({login_url}) and try again."
#                     )

#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- ACCESS GUARD ---
# if not st.session_state.get('user_id') or not st.session_state.get('session_id'):
#     st.error("Session missing or expired. Please login again.")
#     st.page_link("Home.py", label="🔙 Return to Login")
#     st.stop()
# else:
#     main()

############################################## VERSION 2 #########################################################################
# import streamlit as st
# import sys
# import os
# import requests
# import json
# import uuid

# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit
# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Layout Styling ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid=\"stSidebar\"], [data-testid=\"stToolbar\"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid=\"stHeader\"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid=\"stAppViewContainer\"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             [data-testid=\"stButton\"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid=\"stButton\"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     # --- SESSION ID Setup ---
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = str(uuid.uuid4())  # Or use "2222222222" for testing
#     session_id = st.session_state.session_id
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     login_url = f"{base_url}/mockWebPage?sessionId={session_id}"

#     # --- LOGIN CHECK ---
#     if not st.session_state.get("login_confirmed"):
#         st.warning("🔐 Please login to access your financial data.")
#         st.markdown(f"[Click here to login securely]({login_url})", unsafe_allow_html=True)
#         if st.button("✅ I have logged in"):
#             st.session_state.login_confirmed = True
#             st.success("✅ You're logged in! Ask questions or view insights.")
#             st.rerun()
#         st.stop()

#     # --- HEADER ---
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     # --- MAIN CONTENT ---
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # --- KPIs ---
#         st.markdown("### Your AI-Recommended Insights")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.divider()
#         st.markdown("### Chat with DashAI")

#         # --- CHAT LOG ---
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             message_html += f"<div class='message-container {msg['role']}-message'>{msg['content']}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         # --- CHAT INPUT ---
#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 tool_url = f"{base_url}/mcp/stream"
#                 params = {"toolName": "fetch_net_worth", "sessionId": session_id}
#                 resp = requests.get(tool_url, params=params)

#                 # --- PARSE RESPONSE ---
#                 if "application/json" in resp.headers.get("Content-Type", ""):
#                     tool_result = resp.json()
#                 else:
#                     try:
#                         tool_result = json.loads(resp.text)
#                     except:
#                         tool_result = None

#                 # --- SUMMARIZE W/ GEMINI ---
#                 if tool_result:
#                     tool_text = json.dumps(tool_result, indent=2)
#                     gemini_prompt = f"""
# You are a finance assistant. Summarize the following net worth information in simple language:

# {tool_text}
# """
#                     response = get_vertex_response(gemini_prompt)
#                 else:
#                     response = (
#                         "⚠️ Unable to access net worth. "
#                         f"Please [authenticate with Fi MCP]({login_url}) and try again."
#                     )

#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # --- LOGIN CHECK FOR PAGE ACCESS ---
# if not st.session_state.get('user_id'):
#     st.error("Please login first.")
#     st.page_link("Home.py", label="Go to Login", icon="🏠")
#     st.stop()
# else:
#     main()

##############################################################################################################################################
# # pages/1_Dashboard.py

# import streamlit as st
# import sys
# import os
# import requests
# import json
# import uuid

# ##########################################
# # --- Pathing Logic ---
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# if project_root not in sys.path:
#     sys.path.append(project_root)

# # --- Module Imports ---
# from modules import ai_selector, ui_components
# from modules.kpi_definitions import investments, net_worth, banking, credit

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from vertex_chat import get_vertex_response

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Dashboard",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Minimal CSS for Layout and Hiding Default UI ---
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             [data-testid=\"stSidebar\"], [data-testid=\"stToolbar\"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid=\"stHeader\"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
#             div[data-testid=\"stAppViewContainer\"] > .main > div:first-child > div:first-child {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85);
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#             }
#             .header-logo { color: #FFFFFF !important; font-weight: 700; font-size: 24px; text-decoration: none !important; }
#             .welcome-msg { color: #C9D1D9; font-weight: 400; font-size: 16px; text-align: right; padding-top: 8px; }
#             .main-content { padding-top: 100px; }
#             .chat-log-container { max-height: 400px; overflow-y: auto; padding: 1rem; border: 1px solid #30363D; border-radius: 12px; margin-bottom: 1rem; display: flex; flex-direction: column-reverse; }
#             .message-container { width: 100%; margin-bottom: 0.5rem; }
#             .user-message { text-align: right; color: #E0E0E0; }
#             .assistant-message { text-align: left; color: #A0AEC0; }
#             [data-testid=\"stButton\"] > button { border: 1px solid #30363D; background-color: transparent; color: #C9D1D9; }
#             [data-testid=\"stButton\"] > button:hover { border-color: #F2CB5A; color: #F2CB5A; }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     # Sticky Header
#     header = st.container()
#     with header:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
#         with col2:
#             sub_col1, sub_col2 = st.columns([3, 1])
#             with sub_col1:
#                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
#                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
#             with sub_col2:
#                 if st.button("Logout", use_container_width=True):
#                     for key in list(st.session_state.keys()):
#                         del st.session_state[key]
#                     st.switch_page("Home.py")

#     # Main Content
#     main_content = st.container()
#     with main_content:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)

#         # KPIs
#         st.markdown("### Your AI-Recommended Insights")
#         kpi_columns = st.columns(4)
#         kpi_map = {
#             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
#             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
#             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
#             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
#         }
#         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
#         for i, kpi_name in enumerate(recommended_kpis):
#             if kpi_name in kpi_map:
#                 with kpi_columns[i]:
#                     data = kpi_map[kpi_name]['function']()
#                     ui_components.render_kpi_card(
#                         title=kpi_map[kpi_name]['title'], value=data['value'],
#                         unit=kpi_map[kpi_name]['unit'], change=data['change'], icon=kpi_map[kpi_name]['icon']
#                     )

#         st.divider()
#         st.markdown("### Chat with DashAI")

#         # Initialize chat history
#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # Display chat log
#         message_html = ""
#         for msg in reversed(st.session_state.messages):
#             message_html += f"<div class='message-container {msg['role']}-message'>{msg['content']}</div>"
#         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

#         # Chat input and logic
#         if prompt := st.chat_input("Ask DashAI about your finances..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             try:
#                 # Ensure session_id exists
#                 session_id = st.session_state.get("session_id")
#                 if not session_id:
#                     session_id = str(uuid.uuid4())
#                     st.session_state["session_id"] = session_id

#                 # Call MCP tool
#                 base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#                 tool_url = f"{base_url}/mcp/stream"
#                 params = {"toolName": "fetch_net_worth", "sessionId": session_id}
#                 resp = requests.get(tool_url, params=params)

#                 # Parse tool result
#                 if "application/json" in resp.headers.get("Content-Type", ""):
#                     tool_result = resp.json()
#                 else:
#                     try:
#                         tool_result = json.loads(resp.text)
#                     except:
#                         tool_result = None

#                 # If data available, summarize with Gemini
#                 if tool_result:
#                     tool_text = json.dumps(tool_result, indent=2)
#                     gemini_prompt = f"""
# You are a finance assistant. Summarize the following net worth information in simple language:

# {tool_text}
# """
#                     response = get_vertex_response(gemini_prompt)
#                 else:
#                     login_url = f"{base_url}/mockWebPage?sessionId={session_id}"
#                     response = (
#                         "⚠️ Unable to access net worth. "
#                         f"Please [authenticate with Fi MCP]({login_url}) and try again."
#                     )

#             except Exception as e:
#                 response = f"⚠️ Error: {e}"

#             st.session_state.messages.append({"role": "assistant", "content": response})
#             st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

# # Authentication check
# if not st.session_state.get('user_id'):
#     st.error("Please login first.")
#     st.page_link("Home.py", label="Go to Login", icon="🏠")
#     st.stop()
# else:
#     main()

# # # # -----------------------------------------------------------------
# # # #   
# # # # -----------------------------------------------------------------
# # # pages/1_Dashboard.py

# # import streamlit as st
# # import sys
# # import os
# # import requests
# # import json
# # import uuid

# # # --- Pathing Logic ---
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # project_root = os.path.dirname(current_dir)
# # if project_root not in sys.path:
# #     sys.path.append(project_root)

# # # --- Module Imports ---
# # from modules import ai_selector, ui_components
# # from modules.kpi_definitions import investments, net_worth, banking, credit

# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# # from vertex_chat import get_vertex_response

# # # --- Page Configuration ---
# # st.set_page_config(
# #     page_title="DashAI - Dashboard",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )

# # # --- Minimal CSS for Layout and Hiding Default UI ---
# # def apply_layout_styling():
# #     st.markdown("""
# #         <style>
# #             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
# #                 display: none;
# #             }
# #             header[data-testid="stHeader"] {
# #                 display: none !important;
# #                 visibility: hidden !important;
# #             }
# #             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
# #                 position: fixed;
# #                 top: 0;
# #                 left: 0;
# #                 right: 0;
# #                 width: 100%;
# #                 background: rgba(10, 10, 10, 0.85);
# #                 backdrop-filter: blur(12px);
# #                 -webkit-backdrop-filter: blur(12px);
# #                 padding: 1rem 2.5rem;
# #                 z-index: 1000;
# #                 border-bottom: 1px solid #30363D;
# #             }
# #             .header-logo {
# #                 color: #FFFFFF !important;
# #                 font-weight: 700;
# #                 font-size: 24px;
# #                 text-decoration: none !important;
# #             }
# #             .welcome-msg {
# #                 color: #C9D1D9;
# #                 font-weight: 400;
# #                 font-size: 16px;
# #                 text-align: right;
# #                 padding-top: 8px;
# #             }
# #             .main-content {
# #                 padding-top: 100px;
# #             }
# #             .chat-log-container {
# #                 max-height: 400px;
# #                 overflow-y: auto;
# #                 padding: 1rem;
# #                 border: 1px solid #30363D;
# #                 border-radius: 12px;
# #                 margin-bottom: 1rem;
# #                 display: flex;
# #                 flex-direction: column-reverse;
# #             }
# #             .message-container {
# #                 width: 100%;
# #                 margin-bottom: 0.5rem;
# #             }
# #             .user-message {
# #                 text-align: right;
# #                 color: #E0E0E0;
# #             }
# #             .assistant-message {
# #                 text-align: left;
# #                 color: #A0AEC0;
# #             }
# #             [data-testid="stButton"] > button {
# #                 border: 1px solid #30363D;
# #                 background-color: transparent;
# #                 color: #C9D1D9;
# #             }
# #             [data-testid="stButton"] > button:hover {
# #                 border-color: #F2CB5A;
# #                 color: #F2CB5A;
# #             }
# #         </style>
# #     """, unsafe_allow_html=True)

# # def main():
# #     apply_layout_styling()

# #     header = st.container()
# #     with header:
# #         col1, col2 = st.columns([2, 1])
# #         with col1:
# #             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
# #         with col2:
# #             sub_col1, sub_col2 = st.columns([3, 1])
# #             with sub_col1:
# #                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
# #                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
# #             with sub_col2:
# #                 if st.button("Logout", use_container_width=True):
# #                     for key in st.session_state.keys():
# #                         del st.session_state[key]
# #                     st.switch_page("Home.py")

# #     main_content = st.container()
# #     with main_content:
# #         st.markdown('<div class="main-content">', unsafe_allow_html=True)

# #         st.markdown("### Your AI-Recommended Insights")
# #         st.write("")
# #         kpi_columns = st.columns(4)
# #         kpi_map = {
# #             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
# #             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
# #             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
# #             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
# #         }
# #         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
# #         for i, kpi_name in enumerate(recommended_kpis):
# #             if kpi_name in kpi_map:
# #                 with kpi_columns[i]:
# #                     kpi_data = kpi_map[kpi_name]['function']()
# #                     ui_components.render_kpi_card(
# #                         title=kpi_map[kpi_name]['title'], value=kpi_data['value'],
# #                         unit=kpi_map[kpi_name]['unit'], change=kpi_data['change'],
# #                         icon=kpi_map[kpi_name]['icon']
# #                     )

# #         st.divider()
# #         st.markdown("### Chat with DashAI")

# #         if "messages" not in st.session_state:
# #             st.session_state.messages = []

# #         message_html = ""
# #         for msg in reversed(st.session_state.messages):
# #             message_html += f"<div class='message-container {msg['role']}-message'>{msg['content']}</div>"
# #         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

# #         # --- Chat Input with MCP and Gemini integration ---
# #         if prompt := st.chat_input("Ask DashAI about your finances..."):
# #             st.session_state.messages.append({"role": "user", "content": prompt})
# #             try:
# #                 session_id = st.session_state.get("session_id")
# #                 if not session_id:
# #                     session_id = str(uuid.uuid4())
# #                     st.session_state["session_id"] = session_id

# #                 tool_url = "https://fi-mcp-mock-292450254722.us-central1.run.app/mcp/stream"
# #                 params = {"toolName": "fetch_net_worth", "sessionId": session_id}
# #                 resp = requests.get(tool_url, params=params)

# #                 if "application/json" in resp.headers.get("Content-Type", ""):
# #                     tool_result = resp.json()
# #                 elif "text" in resp.headers.get("Content-Type", ""):
# #                     try:
# #                         tool_result = json.loads(resp.text)
# #                     except:
# #                         tool_result = None
# #                 else:
# #                     tool_result = None

# #                 if tool_result:
# #                     tool_text = json.dumps(tool_result, indent=2)
# #                     gemini_prompt = f"""
# # You are a finance assistant. Summarize the following net worth information in simple language:

# # {tool_text}
# # """
# #                     response = get_vertex_response(gemini_prompt)
# #                 else:
# #                     login_url = f"https://fi-mcp-mock-292450254722.us-central1.run.app/mockWebPage?sessionId={session_id}"
# #                     response = f"Okay, it looks like I can't access your net worth information right now. Please [click here to login with Fi MCP]({login_url}) and then come back."

# #             except Exception as e:
# #                 response = f"⚠️ Error: {e}"

# #             st.session_state.messages.append({"role": "assistant", "content": response})
# #             st.rerun()

# #         st.markdown('</div>', unsafe_allow_html=True)

# # if 'user_id' not in st.session_state or not st.session_state.get('user_id'):
# #     st.error("Please login first.")
# #     st.page_link("Home.py", label="Go to Login Page", icon="🏠")
# #     st.stop()
# # else:
# #     main()




# # # -----------------------------------------------------------------
# # #  LLM Vertex AI simple 
# # # -----------------------------------------------------------------
# # # pages/1_Dashboard.py

# # import streamlit as st
# # import sys
# # import os

# # # --- Pathing Logic ---
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # project_root = os.path.dirname(current_dir)
# # if project_root not in sys.path:
# #     sys.path.append(project_root)

# # # --- Module Imports ---
# # from modules import ai_selector, ui_components
# # from modules.kpi_definitions import investments, net_worth, banking, credit
# # # from src.UI.vertex_chat import get_vertex_response  # ✅ Vertex AI import
# # # from src.UI.vertex_chat import get_vertex_response  # if using streamlit run Home.py

# # import sys, os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# # from vertex_chat import get_vertex_response



# # # --- Page Configuration ---
# # st.set_page_config(
# #     page_title="DashAI - Dashboard",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )

# # # --- Minimal CSS for Layout and Hiding Default UI ---
# # def apply_layout_styling():
# #     st.markdown("""
# #         <style>
# #             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
# #                 display: none;
# #             }
# #             header[data-testid="stHeader"] {
# #                 display: none !important;
# #                 visibility: hidden !important;
# #             }
# #             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
# #                 position: fixed;
# #                 top: 0;
# #                 left: 0;
# #                 right: 0;
# #                 width: 100%;
# #                 background: rgba(10, 10, 10, 0.85);
# #                 backdrop-filter: blur(12px);
# #                 -webkit-backdrop-filter: blur(12px);
# #                 padding: 1rem 2.5rem;
# #                 z-index: 1000;
# #                 border-bottom: 1px solid #30363D;
# #             }
# #             .header-logo {
# #                 color: #FFFFFF !important;
# #                 font-weight: 700;
# #                 font-size: 24px;
# #                 text-decoration: none !important;
# #             }
# #             .welcome-msg {
# #                 color: #C9D1D9;
# #                 font-weight: 400;
# #                 font-size: 16px;
# #                 text-align: right;
# #                 padding-top: 8px;
# #             }
# #             .main-content {
# #                 padding-top: 100px;
# #             }
# #             .chat-log-container {
# #                 max-height: 400px;
# #                 overflow-y: auto;
# #                 padding: 1rem;
# #                 border: 1px solid #30363D;
# #                 border-radius: 12px;
# #                 margin-bottom: 1rem;
# #                 display: flex;
# #                 flex-direction: column-reverse;
# #             }
# #             .message-container {
# #                 width: 100%;
# #                 margin-bottom: 0.5rem;
# #             }
# #             .user-message {
# #                 text-align: right;
# #                 color: #E0E0E0;
# #             }
# #             .assistant-message {
# #                 text-align: left;
# #                 color: #A0AEC0;
# #             }
# #             [data-testid="stButton"] > button {
# #                 border: 1px solid #30363D;
# #                 background-color: transparent;
# #                 color: #C9D1D9;
# #             }
# #             [data-testid="stButton"] > button:hover {
# #                 border-color: #F2CB5A;
# #                 color: #F2CB5A;
# #             }
# #         </style>
# #     """, unsafe_allow_html=True)

# # def main():
# #     apply_layout_styling()

# #     # --- Sticky Header ---
# #     header = st.container()
# #     with header:
# #         col1, col2 = st.columns([2, 1])
# #         with col1:
# #             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
        
# #         with col2:
# #             sub_col1, sub_col2 = st.columns([3, 1])
# #             with sub_col1:
# #                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
# #                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
# #             with sub_col2:
# #                 if st.button("Logout", use_container_width=True):
# #                     for key in st.session_state.keys():
# #                         del st.session_state[key]
# #                     st.switch_page("Home.py")

# #     # --- Main Content Area ---
# #     main_content = st.container()
# #     with main_content:
# #         st.markdown('<div class="main-content">', unsafe_allow_html=True)

# #         # --- AI-Recommended Insights ---
# #         st.markdown("### Your AI-Recommended Insights")
# #         st.write("")
# #         kpi_columns = st.columns(4)
# #         kpi_map = {
# #             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
# #             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
# #             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
# #             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
# #         }
# #         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
# #         for i, kpi_name in enumerate(recommended_kpis):
# #             if kpi_name in kpi_map:
# #                 with kpi_columns[i]:
# #                     kpi_data = kpi_map[kpi_name]['function']()
# #                     ui_components.render_kpi_card(
# #                         title=kpi_map[kpi_name]['title'], value=kpi_data['value'],
# #                         unit=kpi_map[kpi_name]['unit'], change=kpi_data['change'],
# #                         icon=kpi_map[kpi_name]['icon']
# #                     )

# #         # --- Chatbot Section ---
# #         st.divider()
# #         st.markdown("### Chat with DashAI")

# #         if "messages" not in st.session_state:
# #             st.session_state.messages = []

# #         # Chat History Display
# #         message_html = ""
# #         for msg in reversed(st.session_state.messages):
# #             message_html += f"<div class='message-container {msg['role']}-message'>{msg['content']}</div>"
# #         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)

# #         # Chat Input + Vertex AI Response
# #         if prompt := st.chat_input("Ask DashAI about your finances..."):
# #             st.session_state.messages.append({"role": "user", "content": prompt})
# #             try:
# #                 response = get_vertex_response(prompt)
# #             except Exception as e:
# #                 response = f"⚠️ Error: {e}"
# #             st.session_state.messages.append({"role": "assistant", "content": response})
# #             st.rerun()

# #         st.markdown('</div>', unsafe_allow_html=True)

# # # --- Authentication Check ---
# # if 'user_id' not in st.session_state or not st.session_state.get('user_id'):
# #     st.error("Please login first.")
# #     st.page_link("Home.py", label="Go to Login Page", icon="🏠")
# #     st.stop()
# # else:
# #     main()

# # -----------------------------------------------------------------
# #  KARTHIK CODE BELOW
# # -----------------------------------------------------------------
# # pages/1_Dashboard.py ------------------------
# # The main dashboard page for the user, with a custom chat implementation.

# # import streamlit as st
# # import sys
# # import os
# # import html # Import the html library to escape characters

# # # --- Pathing Logic ---
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # project_root = os.path.dirname(current_dir)
# # if project_root not in sys.path:
# #     sys.path.append(project_root)

# # # --- Module Imports ---
# # from modules import ai_selector, ui_components
# # from modules.kpi_definitions import investments, net_worth, banking, credit

# # # --- Page Configuration ---
# # st.set_page_config(
# #     page_title="DashAI - Dashboard",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )

# # # --- Minimal CSS for Layout and Hiding Default UI ---
# # def apply_layout_styling():
# #     st.markdown("""
# #         <style>
# #             /* Hide Streamlit's default UI elements */
# #             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
# #                 display: none;
# #             }
# #             header[data-testid="stHeader"] {
# #                 display: none !important;
# #                 visibility: hidden !important;
# #             }
            
# #             /* Target the first container in the main view to act as our sticky header */
# #             div[data-testid="stAppViewContainer"] > .main > div:first-child > div:first-child {
# #                 position: fixed;
# #                 top: 0;
# #                 left: 0;
# #                 right: 0;
# #                 width: 100%;
# #                 background: rgba(10, 10, 10, 0.85); /* Matches theme bg */
# #                 backdrop-filter: blur(12px);
# #                 -webkit-backdrop-filter: blur(12px);
# #                 padding: 1rem 2.5rem;
# #                 z-index: 1000;
# #                 border-bottom: 1px solid #30363D;
# #             }
            
# #             .header-logo {
# #                 color: #FFFFFF !important;
# #                 font-weight: 700;
# #                 font-size: 24px;
# #                 text-decoration: none !important;
# #             }
            
# #             .welcome-msg {
# #                 color: #C9D1D9;
# #                 font-weight: 400;
# #                 font-size: 16px;
# #                 text-align: right;
# #                 padding-top: 8px; /* Align vertically with button */
# #             }

# #             /* Add padding to the top of the main content to prevent overlap with sticky header */
# #             .main-content {
# #                 padding-top: 100px; 
# #             }
            
# #             /* --- NEW: Style for News and Summary Boxes --- */
# #             .info-box {
# #                 background-color: #161B22; /* secondaryBackgroundColor */
# #                 border: 1px solid #30363D;
# #                 border-radius: 12px;
# #                 padding: 1.5rem;
# #                 height: 250px; /* Fixed height */
# #                 overflow-y: auto;
# #             }
            
# #             /* --- CUSTOM CHAT LOG STYLES --- */
# #             .chat-log-container {
# #                 max-height: 400px; /* Set a max height */
# #                 overflow-y: auto;  /* Make it scrollable */
# #                 padding: 1rem;
# #                 border: 1px solid #30363D;
# #                 border-radius: 12px;
# #                 margin-bottom: 1rem;
# #                 display: flex;
# #                 flex-direction: column-reverse; /* Newest messages at the bottom */
# #             }

# #             .message-container {
# #                 width: 100%;
# #                 margin-bottom: 0.5rem;
# #             }

# #             .user-message {
# #                 text-align: right;
# #                 color: #E0E0E0;
# #             }

# #             .assistant-message {
# #                 text-align: left;
# #                 color: #A0AEC0; /* Slightly different color for assistant */
# #             }
# #             /* --- END OF CHAT STYLES --- */
            
# #             /* Style for the logout button */
# #             [data-testid="stButton"] > button {
# #                 border: 1px solid #30363D;
# #                 background-color: transparent;
# #                 color: #C9D1D9;
# #             }
# #             [data-testid="stButton"] > button:hover {
# #                 border-color: #F2CB5A;
# #                 color: #F2CB5A;
# #             }

# #         </style>
# #     """, unsafe_allow_html=True)

# # def main():
# #     apply_layout_styling()

# #     # --- Sticky Header (Built with Streamlit widgets) ---
# #     header = st.container()
# #     with header:
# #         col1, col2 = st.columns([2, 1])
# #         with col1:
# #             st.markdown('<a href="#" class="header-logo">🪙 DashAI</a>', unsafe_allow_html=True)
        
# #         with col2:
# #             sub_col1, sub_col2 = st.columns([3, 1])
# #             with sub_col1:
# #                 user_name = "Alex" if st.session_state.user_id == "USER_ALEX" else "User"
# #                 st.markdown(f'<p class="welcome-msg">Welcome back, {user_name}!</p>', unsafe_allow_html=True)
# #             with sub_col2:
# #                 if st.button("Logout", use_container_width=True):
# #                     for key in st.session_state.keys():
# #                         del st.session_state[key]
# #                     st.switch_page("Home.py")

# #     # --- Main Content Area ---
# #     main_content = st.container()
# #     with main_content:
# #         st.markdown('<div class="main-content">', unsafe_allow_html=True)

# #         # --- AI-Recommended Insights Section ---
# #         st.markdown("### Your AI-Recommended Insights")
# #         st.write("") # Spacer

# #         kpi_columns = st.columns(4)
# #         kpi_map = {
# #             'NET_WORTH': {'function': net_worth.calculate_net_worth, 'title': "Net Worth", 'unit': '$', 'icon': '💰'},
# #             'PORTFOLIO_PERFORMANCE': {'function': investments.calculate_ytd_performance, 'title': "YTD Performance", 'unit': '%', 'icon': '📈'},
# #             'SAVINGS_RATE': {'function': banking.calculate_savings_rate, 'title': "Savings Rate", 'unit': '%', 'icon': '🏦'},
# #             'CREDIT_SCORE': {'function': credit.get_credit_score, 'title': "Credit Score", 'unit': '', 'icon': '💳'}
# #         }
# #         recommended_kpis = ai_selector.get_recommended_kpis(st.session_state.user_id)
# #         for i, kpi_name in enumerate(recommended_kpis):
# #             if kpi_name in kpi_map:
# #                 with kpi_columns[i]:
# #                     kpi_data = kpi_map[kpi_name]['function']()
# #                     ui_components.render_kpi_card(
# #                         title=kpi_map[kpi_name]['title'], value=kpi_data['value'],
# #                         unit=kpi_map[kpi_name]['unit'], change=kpi_data['change'],
# #                         icon=kpi_map[kpi_name]['icon']
# #                     )

# #         st.write("") # Add some space

# #         # --- News and Summary Section ---
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             # --- WHERE TO CHANGE NEWS CONTENT ---
# #             # Replace the placeholder strings below with your AI-generated news content.
# #             news_content = """
# #                 <h3>📰 Latest News</h3>
# #                 <p>Placeholder for AI-curated news articles relevant to your portfolio.</p>
# #                 <ul>
# #                     <li><strong>Market Update:</strong> Tech stocks see a slight dip after recent rally.</li>
# #                     <li><strong>Your Holdings:</strong> Company XYZ announces record earnings.</li>
# #                 </ul>
# #             """
# #             st.markdown(f'<div class="info-box">{news_content}</div>', unsafe_allow_html=True)
        
# #         with col2:
# #             # --- WHERE TO CHANGE SUMMARY CONTENT ---
# #             # Replace the placeholder string below with your AI-generated summary.
# #             summary_content = """
# #                 <h3>💡 AI Summary</h3>
# #                 <p>Placeholder for an AI-generated summary of your financial health.</p>
# #                 <p>Overall, your net worth is trending positively. Your savings rate is strong, but there may be opportunities to optimize your investment allocation based on recent market news.</p>
# #             """
# #             st.markdown(f'<div class="info-box">{summary_content}</div>', unsafe_allow_html=True)


# #         # --- Chatbot Section ---
# #         st.divider()
# #         st.markdown("### Chat with DashAI")

# #         if "messages" not in st.session_state:
# #             st.session_state.messages = []

# #         # --- Refactored Chat Log Display ---
# #         message_html = ""
# #         for msg in reversed(st.session_state.messages):
# #             # FIX: Escape the message content to prevent HTML injection
# #             escaped_content = html.escape(msg['content'])
# #             message_html += f"<div class='message-container {msg['role']}-message'>{escaped_content}</div>"
        
# #         st.markdown(f'<div class="chat-log-container">{message_html}</div>', unsafe_allow_html=True)


# #         # --- Chat Input ---
# #         if prompt := st.chat_input("Ask DashAI about your finances..."):
# #             st.session_state.messages.append({"role": "user", "content": prompt})
# #             assistant_response = f"You asked: '{prompt}'. The AI response functionality is under development."
# #             st.session_state.messages.append({"role": "assistant", "content": assistant_response})
# #             st.rerun()
        
# #         st.markdown('</div>', unsafe_allow_html=True)

# # # --- Authentication Check ---
# # if 'user_id' not in st.session_state or not st.session_state.get('user_id'):
# #     st.error("Please login first.")
# #     st.page_link("Home.py", label="Go to Login Page", icon="🏠")
# #     st.stop()
# # else:
# #     main()
