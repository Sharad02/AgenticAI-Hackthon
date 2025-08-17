import streamlit as st
import uuid
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="DashAI - Login",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Base URL for the mock authentication service
MCP_BASE = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# --- Styling ---
def apply_layout_styling():
    st.markdown("""
        <style>
            /* Hide default Streamlit UI elements */
            [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
                display: none;
            }
            header[data-testid="stHeader"] {
                display: none !important;
                visibility: hidden !important;
            }
            /* Custom sticky header */
            .sticky-header {
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
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .header-logo {
                color: #FFFFFF !important;
                font-weight: 700;
                font-size: 24px;
                text-decoration: none !important;
            }
            .nav-menu { display: flex; gap: 2.5rem; }
            .nav-item {
                color: #FFFFFF !important;
                text-decoration: none !important;
                font-weight: 600;
                font-size: 14px;
                text-transform: uppercase;
                transition: color 0.2s;
            }
            .nav-item:hover {
                color: #F2CB5A !important;
            }
            /* Centered headline wrapper */
            .headline-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding-top: 20vh;
                width: 100%;
                max-width: 550px;
                margin: 0 auto;
            }
            .main-headline {
                font-size: 3.5rem;
                font-weight: 800;
                text-align: center;
                line-height: 1.1;
                margin-bottom: 1rem;
            }
            .main-headline span { color: #F2CB5A; }
            .version-text {
                color: #8B949E;
                font-size: 16px;
                text-align: center;
                margin-bottom: 2rem;
            }
            .instruction-text {
                color: #CCCCCC;
                text-align: center;
                margin-top: 2rem;
                font-size: 14px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Authentication Function ---
def is_authenticated(session_id: str) -> bool:
    """
    Calls the MCP server and checks the JSON response to determine
    if the user is properly authenticated.
    """
    try:
        url = f"{MCP_BASE}/mcp/stream"
        params = {"toolName": "fetch_net_worth", "sessionId": session_id}
        resp = requests.get(url, params=params, timeout=10)

        if resp.status_code != 200:
            return False

        # The server response reveals the true status.
        # A successful login has a "status" of "success".
        data = resp.json()
        if data.get("status") == "success":
            # As a bonus, we can store the retrieved financial data for the next page
            st.session_state['financial_data'] = data.get('result')
            return True
        else:
            # Any other status (like "login_required") means authentication is not complete.
            return False
        
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        st.error(f"An error occurred while validating the session: {e}")
        return False

# --- Main Application Logic ---
def main():
    apply_layout_styling()

    # --- UI Elements: Header and Headline ---
    nav_html = "".join([f'<a href="#" class="nav-item">{item}</a>' for item in ['About', 'Team', 'Tech Used', 'Analysis']])
    st.markdown(f"""
        <div class="sticky-header">
            <a href="#" class="header-logo">🪙 DashAI</a>
            <div class="nav-menu">{nav_html}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
    st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
    st.markdown("<p class='version-text'>Prototype v1.0.0</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Session and Authentication Logic ---
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    
    session_id = st.session_state["session_id"]
    login_url = f"{MCP_BASE}/mockWebPage?sessionId={session_id}"

    # Use columns to center the login elements
    _ , col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown(f"""
            <a href="{login_url}" target="_blank" style="text-decoration: none;">
                <button style='padding: 12px 30px; font-size: 16px; border-radius: 8px;
                               background-color: #4CAF50; color: white; border: none; width: 100%; margin-bottom: 10px;'>
                    🔐 Login with Fi MCP
                </button>
            </a>
        """, unsafe_allow_html=True)

        if st.button("Check Login Status", use_container_width=True):
            with st.spinner("Verifying authentication..."):
                if is_authenticated(session_id):
                    st.success("✅ Authentication successful! Redirecting...")
                    st.session_state["user_id"] = "USER_MCP"
                    # Use a short delay before switching pages to allow the user to see the message
                    import time
                    time.sleep(1)
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("Authentication incomplete. Please complete the login on the other tab and try again.")

    st.markdown("""
        <div class="instruction-text">
            Step 1: Click “Login with Fi MCP” and complete the login in the new tab.<br>
            Step 2: Return here and click “Check Login Status”.
        </div>
    """, unsafe_allow_html=True)

# --- Main Execution ---
if __name__ == "__main__":
    # If the user is already logged in from a previous session, redirect them.
    if st.session_state.get("user_id"):
        st.switch_page("pages/1_Dashboard.py")
    else:
        main()



# ############################################################################### HOME PY Version
# import streamlit as st
# import uuid

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Login",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Styling ---
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
#             .sticky-header {
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
#                 display: flex;
#                 align-items: center;
#                 justify-content: space-between;
#             }
#             .header-logo {
#                 color: #FFFFFF !important;
#                 font-weight: 700;
#                 font-size: 24px;
#                 text-decoration: none !important;
#             }
#             .nav-menu { display: flex; gap: 2.5rem; }
#             .nav-item {
#                 color: #FFFFFF !important;
#                 text-decoration: none !important;
#                 font-weight: 600;
#                 font-size: 14px;
#                 text-transform: uppercase;
#                 transition: color 0.2s;
#             }
#             .nav-item:hover {
#                 color: #F2CB5A !important;
#             }
#             .headline-wrapper {
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 justify-content: center;
#                 padding-top: 20vh;
#                 width: 100%;
#                 max-width: 550px;
#                 margin: 0 auto;
#             }
#             .main-headline {
#                 font-size: 3.5rem;
#                 font-weight: 800;
#                 text-align: center;
#                 line-height: 1.1;
#                 margin-bottom: 1rem;
#             }
#             .main-headline span { color: #F2CB5A; }
#             .version-text {
#                 color: #8B949E;
#                 font-size: 16px;
#                 text-align: center;
#                 margin-bottom: 2rem;
#             }
#             .instruction-text {
#                 color: #CCCCCC;
#                 text-align: center;
#                 margin-top: 2rem;
#                 font-size: 14px;
#             }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     apply_layout_styling()

#     # Sticky Header
#     nav_html = "".join([f'<a href="#" class="nav-item">{item}</a>' for item in ['About', 'Team', 'Tech Used', 'Analysis']])
#     st.markdown(f"""
#         <div class="sticky-header">
#             <a href="#" class="header-logo">🪙 DashAI</a>
#             <div class="nav-menu">{nav_html}</div>
#         </div>
#     """, unsafe_allow_html=True)

#     # Headline
#     st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
#     st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
#     st.markdown("<p class='version-text'>Prototype v1.0.0</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # --- Session Setup ---
#     if "session_id" not in st.session_state:
#         st.session_state["session_id"] = str(uuid.uuid4())

#     session_id = st.session_state["session_id"]
#     login_url = f"https://fi-mcp-mock-292450254722.us-central1.run.app/mockWebPage?sessionId={session_id}"

#     # Centered Buttons
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         # Login Button
#         st.markdown(f"""
#             <a href="{login_url}" target="_blank">
#                 <button style='padding: 12px 30px; font-size: 16px; border-radius: 8px;
#                                 background-color: #4CAF50; color: white; border: none; width: 100%;'>
#                     🔐 Login with Fi MCP
#                 </button>
#             </a>
#         """, unsafe_allow_html=True)

#         # Proceed Button
#         if st.button("➡️ Proceed to Dashboard", use_container_width=True):
#             st.session_state["user_id"] = "USER_MCP"
#             st.switch_page("pages/1_Dashboard.py")

#     # Instruction
#     st.markdown("""
#         <div class="instruction-text">
#             Step 1: Click “Login with Fi MCP” and complete login in the new tab.<br>
#             Step 2: Return here and click “Proceed to Dashboard”.
#         </div>
#     """, unsafe_allow_html=True)

# # --- Redirect if already logged in ---
# if st.session_state.get("user_id") and st.session_state.get("session_id"):
#     st.switch_page("pages/1_Dashboard.py")
# else:
#     main()

# print(str(uuid.uuid4()))



# #############################################################DOCKER
# # Home.py
# # This is the landing page of the DashAI application.
# # It now uses the central theme defined in .streamlit/config.toml
# # -----------------------------------------------------------------
# #  LLM BASED BELOW
# # -----------------------------------------------------------------
# import streamlit as st
# import re

# # --- Page Configuration ---
# # The theme will be automatically picked up from the config.toml file.
# st.set_page_config(
#     page_title="DashAI - Login",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Minimal CSS for Layout and Hiding Default UI ---
# # All color and font styling is now handled by the theme.
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             /* Hide Streamlit's default UI elements */
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
            
#             /* Custom Sticky Header Layout */
#             .sticky-header {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85); /* Matches theme bg */
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#                 display: flex;
#                 align-items: center;
#                 justify-content: space-between;
#             }
            
#             /* Logo text is now white */
#             .header-logo {
#                 color: #FFFFFF !important; 
#                 font-weight: 700;
#                 font-size: 24px;
#                 text-decoration: none !important;
#             }
            
#             .nav-menu { display: flex; gap: 2.5rem; }
#             /* Nav menu text is white */
#             .nav-item {
#                 color: #FFFFFF !important;
#                 text-decoration: none !important;
#                 font-weight: 600;
#                 font-size: 14px;
#                 text-transform: uppercase;
#                 transition: color 0.2s;
#             }
#             .nav-item:hover {
#                 color: #F2CB5A !important; /* Hover color is yellow */
#             }

#             /* Wrapper to center the headline text */
#             .headline-wrapper {
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 justify-content: center;
#                 padding-top: 15vh;
#                 width: 100%;
#                 max-width: 550px;
#                 margin: 0 auto;
#             }

#             /* Main headline styling */
#             .main-headline {
#                 font-size: 4rem;
#                 font-weight: 800;
#                 text-align: center;
#                 line-height: 1.1;
#                 margin-bottom: 1rem;
#             }
            
#             .main-headline span {
#                 color: #F2CB5A; /* Primary color from theme */
#             }

#             .version-text {
#                 color: #8B949E;
#                 font-size: 16px;
#                 text-align: center;
#                 margin-bottom: 2.5rem;
#             }

#         </style>
#     """, unsafe_allow_html=True)

# def validate_mobile_number(mobile):
#     """A simple validator for mobile numbers."""
#     if re.match(r"^\d{10}$", mobile):
#         return True
#     return False

# def main():
#     APP_VERSION = "v1.0.0"
#     apply_layout_styling()

#     # --- Sticky Header ---
#     menu_items = ['About', 'Team', 'Tech Used', 'Analysis']
#     nav_html = "".join([f'<a href="#" class="nav-item">{item}</a>' for item in menu_items])
    
#     st.markdown(f"""
#         <div class="sticky-header">
#             <a href="#" class="header-logo">🪙 DashAI</a>
#             <div class="nav-menu">
#                 {nav_html}
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

#     # --- Main Login Headline ---
#     st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
#     st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
#     st.markdown(f"<p class='version-text'>Prototype {APP_VERSION}</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # --- Centered Login Form ---
#     # Use columns to create a centered form with a reduced, controlled width.
#     col1, col2, col3 = st.columns([1, 1, 1])

#     with col2:
#         mobile_number = st.text_input(
#             "Mobile Number",
#             placeholder="Enter your 10-digit mobile number to begin",
#             key="mobile_number_input",
#             label_visibility="collapsed",
#             max_chars=10
#         )

#         # The button will fill the width of the column, appearing centered on the page.
#         if st.button("Proceed", use_container_width=True):
#             if validate_mobile_number(mobile_number):
#                 st.session_state['user_id'] = "USER_ALEX"
#                 st.session_state['mobile_number'] = mobile_number
#                 st.switch_page("pages/1_Dashboard.py")
#             else:
#                 st.error("Please enter a valid 10-digit mobile number.")


# if __name__ == "__main__":
#     if 'user_id' in st.session_state and st.session_state.get('user_id'):
#         st.switch_page("pages/1_Dashboard.py")
#     else:
#         main()


## VERSION 2.01################
# import streamlit as st
# import uuid
# import requests
# import time

# st.set_page_config(page_title="DashAI - Login", layout="wide", initial_sidebar_state="collapsed")

# MCP_BASE = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# def is_authenticated(session_id):
#     try:
#         url = f"{MCP_BASE}/mcp/stream"
#         resp = requests.get(url, params={"toolName": "fetch_net_worth", "sessionId": session_id}, timeout=5)
#         return resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("application")
#     except Exception:
#         return False

# def apply_styling():
#     st.markdown("""
#     <style>
#         [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#             display: none;
#         }
#         header[data-testid="stHeader"] {
#             display: none !important;
#             visibility: hidden !important;
#         }
#         .headline-wrapper {
#             display: flex; flex-direction: column; align-items: center; justify-content: center;
#             padding-top: 20vh; width: 100%; max-width: 550px; margin: 0 auto;
#         }
#         .main-headline {
#             font-size: 3.5rem; font-weight: 800; text-align: center; line-height: 1.1; margin-bottom: 1rem;
#         }
#         .main-headline span { color: #F2CB5A; }
#         .version-text { color: #8B949E; font-size: 16px; text-align: center; margin-bottom: 2rem; }
#     </style>
#     """, unsafe_allow_html=True)

# def main():
#     apply_styling()
#     st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
#     st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
#     st.markdown("<p class='version-text'>Prototype v1.0.0</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # --- Session ID ---
#     if "session_id" not in st.session_state:
#         st.session_state["session_id"] = str(uuid.uuid4())

#     session_id = st.session_state["session_id"]
#     login_url = f"{MCP_BASE}/mockWebPage?sessionId={session_id}"

#     # --- Login Button ---
#     st.markdown(f"""
#         <a href="{login_url}" target="_blank">
#             <button style='padding: 12px 30px; font-size: 16px; border-radius: 8px;
#                             background-color: #4CAF50; color: white; border: none; width: 100%;'>
#                 🔐 Login with Fi MCP
#             </button>
#         </a>
#     """, unsafe_allow_html=True)

#     # --- Auto-Check for Login Completion ---
#     st.info("Waiting for login... (this will auto-continue once you're authenticated)")

#     with st.spinner("Checking login status..."):
#         for i in range(30):  # up to ~15 seconds
#             if is_authenticated(session_id):
#                 st.success("✅ Logged in successfully! Redirecting...")
#                 st.session_state["user_id"] = "USER_MCP"
#                 time.sleep(1)
#                 st.switch_page("pages/1_Dashboard.py")
#                 break
#             time.sleep(0.5)
#         else:
#             st.warning("Still not logged in. Please complete login in the other tab and refresh this page.")

# # --- Run App ---
# if __name__ == "__main__":
#     if st.session_state.get("user_id"):
#         st.switch_page("pages/1_Dashboard.py")
#     else:
#         main()


# # Home.py – Smart Login with Streamlit-controlled sessionId

# import streamlit as st
# import uuid

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="DashAI - Login",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Styling ---
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
#             .sticky-header {
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
#                 display: flex;
#                 align-items: center;
#                 justify-content: space-between;
#             }
#             .header-logo {
#                 color: #FFFFFF !important; 
#                 font-weight: 700;
#                 font-size: 24px;
#                 text-decoration: none !important;
#             }
#             .nav-menu { display: flex; gap: 2.5rem; }
#             .nav-item {
#                 color: #FFFFFF !important;
#                 text-decoration: none !important;
#                 font-weight: 600;
#                 font-size: 14px;
#                 text-transform: uppercase;
#                 transition: color 0.2s;
#             }
#             .nav-item:hover {
#                 color: #F2CB5A !important;
#             }
#             .headline-wrapper {
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 justify-content: center;
#                 padding-top: 15vh;
#                 width: 100%;
#                 max-width: 550px;
#                 margin: 0 auto;
#             }
#             .main-headline {
#                 font-size: 4rem;
#                 font-weight: 800;
#                 text-align: center;
#                 line-height: 1.1;
#                 margin-bottom: 1rem;
#             }
#             .main-headline span {
#                 color: #F2CB5A;
#             }
#             .version-text {
#                 color: #8B949E;
#                 font-size: 16px;
#                 text-align: center;
#                 margin-bottom: 2.5rem;
#             }
#         </style>
#     """, unsafe_allow_html=True)

# # --- Main Function ---
# def main():
#     APP_VERSION = "v1.0.0"
#     apply_layout_styling()

#     # Sticky Header
#     menu_items = ['About', 'Team', 'Tech Used', 'Analysis']
#     nav_html = "".join([f'<a href="#" class="nav-item">{item}</a>' for item in menu_items])
#     st.markdown(f"""
#         <div class="sticky-header">
#             <a href="#" class="header-logo">🪙 DashAI</a>
#             <div class="nav-menu">{nav_html}</div>
#         </div>
#     """, unsafe_allow_html=True)

#     # Headline Text
#     st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
#     st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
#     st.markdown(f"<p class='version-text'>Prototype {APP_VERSION}</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # --- Session Generation ---
#     if "session_id" not in st.session_state:
#         st.session_state["session_id"] = str(uuid.uuid4())

#     session_id = st.session_state["session_id"]
#     login_url = f"https://fi-mcp-mock-292450254722.us-central1.run.app/mockWebPage?sessionId={session_id}"

#     # --- Login and Proceed Buttons ---
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         st.markdown(f"""
#             <a href="{login_url}" target="_blank">
#                 <button style='padding: 12px 30px; font-size: 16px; border-radius: 8px;
#                                 background-color: #4CAF50; color: white; border: none; width: 100%;'>
#                     🔐 Login with Fi MCP
#                 </button>
#             </a>
#         """, unsafe_allow_html=True)

#         if st.button("➡️ Proceed to Dashboard", use_container_width=True):
#             st.session_state["user_id"] = "USER_MCP"
#             st.switch_page("pages/1_Dashboard.py")

# # --- Run ---
# if __name__ == "__main__":
#     if st.session_state.get("user_id"):
#         st.switch_page("pages/1_Dashboard.py")
#     else:
#         main()

##############################################################DOCKER
# # Home.py
# # This is the landing page of the DashAI application.
# # It now uses the central theme defined in .streamlit/config.toml
# # -----------------------------------------------------------------
# #  LLM BASED BELOW
# # -----------------------------------------------------------------
# import streamlit as st
# import re

# # --- Page Configuration ---
# # The theme will be automatically picked up from the config.toml file.
# st.set_page_config(
#     page_title="DashAI - Login",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # --- Minimal CSS for Layout and Hiding Default UI ---
# # All color and font styling is now handled by the theme.
# def apply_layout_styling():
#     st.markdown("""
#         <style>
#             /* Hide Streamlit's default UI elements */
#             [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#                 display: none;
#             }
#             header[data-testid="stHeader"] {
#                 display: none !important;
#                 visibility: hidden !important;
#             }
            
#             /* Custom Sticky Header Layout */
#             .sticky-header {
#                 position: fixed;
#                 top: 0;
#                 left: 0;
#                 right: 0;
#                 width: 100%;
#                 background: rgba(10, 10, 10, 0.85); /* Matches theme bg */
#                 backdrop-filter: blur(12px);
#                 -webkit-backdrop-filter: blur(12px);
#                 padding: 1rem 2.5rem;
#                 z-index: 1000;
#                 border-bottom: 1px solid #30363D;
#                 display: flex;
#                 align-items: center;
#                 justify-content: space-between;
#             }
            
#             /* Logo text is now white */
#             .header-logo {
#                 color: #FFFFFF !important; 
#                 font-weight: 700;
#                 font-size: 24px;
#                 text-decoration: none !important;
#             }
            
#             .nav-menu { display: flex; gap: 2.5rem; }
#             /* Nav menu text is white */
#             .nav-item {
#                 color: #FFFFFF !important;
#                 text-decoration: none !important;
#                 font-weight: 600;
#                 font-size: 14px;
#                 text-transform: uppercase;
#                 transition: color 0.2s;
#             }
#             .nav-item:hover {
#                 color: #F2CB5A !important; /* Hover color is yellow */
#             }

#             /* Wrapper to center the headline text */
#             .headline-wrapper {
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 justify-content: center;
#                 padding-top: 15vh;
#                 width: 100%;
#                 max-width: 550px;
#                 margin: 0 auto;
#             }

#             /* Main headline styling */
#             .main-headline {
#                 font-size: 4rem;
#                 font-weight: 800;
#                 text-align: center;
#                 line-height: 1.1;
#                 margin-bottom: 1rem;
#             }
            
#             .main-headline span {
#                 color: #F2CB5A; /* Primary color from theme */
#             }

#             .version-text {
#                 color: #8B949E;
#                 font-size: 16px;
#                 text-align: center;
#                 margin-bottom: 2.5rem;
#             }

#         </style>
#     """, unsafe_allow_html=True)

# def validate_mobile_number(mobile):
#     """A simple validator for mobile numbers."""
#     if re.match(r"^\d{10}$", mobile):
#         return True
#     return False

# def main():
#     APP_VERSION = "v1.0.0"
#     apply_layout_styling()

#     # --- Sticky Header ---
#     menu_items = ['About', 'Team', 'Tech Used', 'Analysis']
#     nav_html = "".join([f'<a href="#" class="nav-item">{item}</a>' for item in menu_items])
    
#     st.markdown(f"""
#         <div class="sticky-header">
#             <a href="#" class="header-logo">🪙 DashAI</a>
#             <div class="nav-menu">
#                 {nav_html}
#             </div>
#         </div>
#     """, unsafe_allow_html=True)

#     # --- Main Login Headline ---
#     st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
#     st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
#     st.markdown(f"<p class='version-text'>Prototype {APP_VERSION}</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # --- Centered Login Form ---
#     # Use columns to create a centered form with a reduced, controlled width.
#     col1, col2, col3 = st.columns([1, 1, 1])

#     with col2:
#         mobile_number = st.text_input(
#             "Mobile Number",
#             placeholder="Enter your 10-digit mobile number to begin",
#             key="mobile_number_input",
#             label_visibility="collapsed",
#             max_chars=10
#         )

#         # The button will fill the width of the column, appearing centered on the page.
#         if st.button("Proceed", use_container_width=True):
#             if validate_mobile_number(mobile_number):
#                 st.session_state['user_id'] = "USER_ALEX"
#                 st.session_state['mobile_number'] = mobile_number
#                 st.switch_page("pages/1_Dashboard.py")
#             else:
#                 st.error("Please enter a valid 10-digit mobile number.")


# if __name__ == "__main__":
#     if 'user_id' in st.session_state and st.session_state.get('user_id'):
#         st.switch_page("pages/1_Dashboard.py")
#     else:
#         main()

##################################################################################################
# import streamlit as st
# import uuid
# import requests
# import time

# # --- Page Config ---
# st.set_page_config(page_title="DashAI - Login", layout="wide", initial_sidebar_state="collapsed")

# MCP_BASE = "https://fi-mcp-mock-292450254722.us-central1.run.app"

# # --- Styling ---
# def apply_styling():
#     st.markdown("""
#     <style>
#         [data-testid="stSidebar"], [data-testid="stToolbar"], #MainMenu, footer {
#             display: none;
#         }
#         header[data-testid="stHeader"] {
#             display: none !important;
#             visibility: hidden !important;
#         }
#         .sticky-header {
#             position: fixed;
#             top: 0;
#             left: 0;
#             right: 0;
#             width: 100%;
#             background: rgba(10, 10, 10, 0.85);
#             backdrop-filter: blur(12px);
#             -webkit-backdrop-filter: blur(12px);
#             padding: 1rem 2.5rem;
#             z-index: 1000;
#             border-bottom: 1px solid #30363D;
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#         }
#         .header-logo {
#             color: #FFFFFF !important;
#             font-weight: 700;
#             font-size: 24px;
#             text-decoration: none !important;
#         }
#         .nav-menu { display: flex; gap: 2.5rem; }
#         .nav-item {
#             color: #FFFFFF !important;
#             text-decoration: none !important;
#             font-weight: 600;
#             font-size: 14px;
#             text-transform: uppercase;
#             transition: color 0.2s;
#         }
#         .nav-item:hover {
#             color: #F2CB5A !important;
#         }
#         .headline-wrapper {
#             display: flex; flex-direction: column; align-items: center; justify-content: center;
#             padding-top: 20vh; width: 100%; max-width: 550px; margin: 0 auto;
#         }
#         .main-headline {
#             font-size: 3.5rem; font-weight: 800; text-align: center; line-height: 1.1; margin-bottom: 1rem;
#         }
#         .main-headline span { color: #F2CB5A; }
#         .version-text { color: #8B949E; font-size: 16px; text-align: center; margin-bottom: 2rem; }
#         .instruction-text {
#             color: #CCCCCC;
#             text-align: center;
#             margin-top: 2rem;
#             font-size: 14px;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # --- Auth Check with MCP ---
# def is_authenticated(session_id):
#     try:
#         url = f"{MCP_BASE}/mcp/stream"
#         resp = requests.get(url, params={"toolName": "fetch_net_worth", "sessionId": session_id}, timeout=5)
#         return resp.status_code == 200 and resp.headers.get("Content-Type", "").startswith("application")
#     except Exception:
#         return False

# # --- Main App ---
# def main():
#     apply_styling()

#     # Sticky header
#     menu_items = ['About', 'Team', 'Tech Used', 'Analysis']
#     nav_html = "".join([f'<a href="#" class="nav-item">{item}</a>' for item in menu_items])
#     st.markdown(f"""
#         <div class="sticky-header">
#             <a href="#" class="header-logo">🪙 DashAI</a>
#             <div class="nav-menu">{nav_html}</div>
#         </div>
#     """, unsafe_allow_html=True)

#     # Headline
#     st.markdown('<div class="headline-wrapper">', unsafe_allow_html=True)
#     st.markdown("<h1 class='main-headline'>One AI for all your <span>finances.</span></h1>", unsafe_allow_html=True)
#     st.markdown("<p class='version-text'>Prototype v1.0.0</p>", unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Generate session ID if not already set
#     if "session_id" not in st.session_state:
#         st.session_state["session_id"] = str(uuid.uuid4())

#     session_id = st.session_state["session_id"]
#     login_url = f"{MCP_BASE}/mockWebPage?sessionId={session_id}"

#     # Centered button alignment
#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         # Login Button
#         st.markdown(f"""
#             <a href="{login_url}" target="_blank">
#                 <button style='padding: 12px 30px; font-size: 16px; border-radius: 8px;
#                                 background-color: #4CAF50; color: white; border: none; width: 100%;'>
#                     🔐 Login with Fi MCP
#                 </button>
#             </a>
#         """, unsafe_allow_html=True)

#         # Start polling
#         st.info("Waiting for login... (auto-redirects after successful login)")
#         with st.spinner("Checking login status..."):
#             for i in range(30):  # ~15 seconds
#                 if is_authenticated(session_id):
#                     st.success("✅ Logged in successfully! Redirecting...")
#                     st.session_state["user_id"] = "USER_MCP"
#                     time.sleep(1)
#                     st.switch_page("pages/1_Dashboard.py")
#                     break
#                 time.sleep(0.5)
#             else:
#                 st.warning("Still not logged in. Complete login in the new tab, then refresh this page.")

#     # Instruction at bottom
#     st.markdown("""
#         <div class="instruction-text">
#             Step 1: Click “Login with Fi MCP” to open the login page<br>
#             Step 2: Log in with your number<br>
#             Step 3: Return to this tab — you'll be auto-redirected
#         </div>
#     """, unsafe_allow_html=True)

# # --- Auto-Redirect if Already Logged In ---
# if st.session_state.get("user_id") and st.session_state.get("session_id"):
#     st.switch_page("pages/1_Dashboard.py")
# else:
#     main()

