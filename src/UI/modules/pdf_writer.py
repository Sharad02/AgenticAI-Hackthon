# # import json
# # from fpdf import FPDF
# # import streamlit as st
# # from modules.summary_client import fetch_financial_data


# # def pdf_generate_summary_prompt(combined_data):
# #     """Generate the prompt for the LLM using the fetched financial data."""
# #     return f"""
# # You are a personal financial assistant.

# # Using the following structured financial data, write a short summary of the user's overall financial health in 5 bulletin points. Highlight key strengths (e.g., good net worth, positive investments), weaknesses (e.g., loans, credit score issues), and suggest actions (e.g., reduce EMI, increase savings).
# # **Formatting Instructions:**
# # - Use `<span style="color: #F2CB5A;">...</span>` to highlight **positive** numbers, strengths, and key terms.
# # - Use `<span style="color: #FF6B6B;">...</span>` to highlight **negative** numbers, weaknesses, or areas for improvement.
# # - Add `<br>` after each point.
# # - Do not include any other message like 'Here is your summary'.
# # - Maximum length should be 500 characters.
# # Financial Data:
# # {json.dumps(combined_data, indent=2)}
# # """


# # def generate_pdf_summary(combined_data, summary_text, file_name="financial_summary_report.pdf"):
# #     """
# #     Generate a PDF summary report of the user's financial wealth.

# #     Args:
# #         combined_data (dict): Dictionary containing the financial data.
# #         summary_text (str): A summary of the financial health generated from the LLM.
# #         file_name (str): The name of the PDF file to be saved.
    
# #     Returns:
# #         None
# #     """
# #     # Create instance of FPDF class
# #     pdf = FPDF()
# #     pdf.set_auto_page_break(auto=True, margin=15)
    
# #     # Add a page
# #     pdf.add_page()

# #     # Set title
# #     pdf.set_font('Arial', 'B', 16)
# #     pdf.cell(200, 10, txt="Financial Wealth Summary Report", ln=True, align='C')

# #     # Add line break
# #     pdf.ln(10)  

# #     # Set subheading for the financial health summary
# #     pdf.set_font('Arial', 'B', 12)
# #     pdf.cell(200, 10, txt="Financial Health Summary", ln=True, align='L')

# #     # Add the summary text from the LLM
# #     pdf.ln(5)
# #     pdf.set_font('Arial', '', 12)
# #     pdf.multi_cell(0, 10, txt=summary_text)

# #     # Add detailed financial data below the summary
# #     pdf.ln(10)
# #     pdf.set_font('Arial', 'B', 12)
# #     pdf.cell(200, 10, txt="Detailed Financial Data", ln=True, align='L')
    
# #     # Loop through the combined data to extract and display key financial data
# #     pdf.ln(5)
# #     pdf.set_font('Arial', '', 12)
# #     for tool, data in combined_data.items():
# #         pdf.cell(200, 10, txt=f"{tool.replace('_', ' ').title()}: ", ln=True)
        
# #         # Check if data is a dictionary (e.g., net worth or investments)
# #         if isinstance(data, dict):
# #             for key, value in data.items():
# #                 pdf.cell(200, 10, txt=f"  - {key.title()}: {value}", ln=True)
# #         else:
# #             pdf.cell(200, 10, txt=f"  - {data}", ln=True)

# #     # Save the PDF to file
# #     pdf.output(file_name)
# #     print(f"PDF report generated and saved as {file_name}")


# # def generate_financial_summary_pdf():
# #     """Fetch data from MCP tools, generate summary, and create a PDF report."""
# #     session_id = st.session_state.get("session_id")
# #     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
# #     tools = ["fetch_net_worth", "fetch_mf_transactions", "fetch_stock_transactions", "fetch_credit_report"]

# #     # Fetch the combined data from MCP tools
# #     combined_data = fetch_financial_data(tools, session_id, base_url)

# #     # Create summary prompt for LLM (for PDF generation)
# #     prompt = pdf_generate_summary_prompt(combined_data)

# #     try:
# #         # Get the summary from Gemini (Assume 'get_vertex_response' returns a summary)
# #         summary = get_vertex_response(prompt)

# #         # Generate the PDF report with the summary
# #         generate_pdf_summary(combined_data, summary.strip())

# #         return summary.strip()
# #     except Exception as e:
# #         return f"⚠️ Error generating PDF summary: {e}"


# # import json
# # from vertex_chat import get_vertex_response
# # # from modules.mcp_tools import call_mcp_tool
# # import streamlit as st
# # from fpdf import FPDF
# # from modules.summary_client import fetch_financial_data

# # # def fetch_financial_data(tools, session_id, base_url):
# # #     """Fetch data from multiple MCP tools and return a combined result."""
# # #     combined_data = {}
# # #     for tool in tools:
# # #         result = None
# # #         try:
# # #             result = call_mcp_tool(tool, session_id, base_url)
# # #             if isinstance(result, str):
# # #                 result = json.loads(result)
# # #         except Exception as e:
# # #             st.error(f"❌ Error fetching {tool}: {e}")
# # #         combined_data[tool] = result
# # #     return combined_data


# # # def generate_summary_prompt(combined_data, is_pdf=False):
# # #     """Generate the prompt for the LLM using the fetched financial data."""
# # #     prompt = f"""
# # #     You are a personal financial assistant.

# # #     Using the following structured financial data, write a short summary of the user's overall financial health in 5 bulletin points. Highlight key strengths (e.g., good net worth, positive investments), weaknesses (e.g., loans, credit score issues), and suggest actions (e.g., reduce EMI, increase savings).
# # #     **Formatting Instructions:**
# # #     - Use `<span style="color: #F2CB5A;">...</span>` to highlight **positive** numbers, strengths, and key terms.
# # #     - Use `<span style="color: #FF6B6B;">...</span>` to highlight **negative** numbers, weaknesses, or areas for improvement.
# # #     - Add `<br>` after each point.
# # #     - Do not include any other message like 'Here is your summary'.
# # #     - Maximum length should be 500 characters.
# # #     Financial Data:
# # #     {json.dumps(combined_data, indent=2)}
# # #     """
    
# #     # # Modify the prompt if it's for PDF generation (could add specific formatting instructions if needed)
# #     # if is_pdf:
# #     #     prompt = prompt.replace("Maximum length should be 500 characters.", "Provide detailed insights suitable for a PDF report.")

# #     # return prompt

# # def pdf_generate_summary_prompt(combined_data):
# #     """Generate the prompt for the LLM using the fetched financial data."""
# #     return f"""
# # You are a personal financial assistant.

# # Using the following structured financial data, write a short summary of the user's overall financial health in 5 bulletin points. Highlight key strengths (e.g., good net worth, positive investments), weaknesses (e.g., loans, credit score issues), and suggest actions (e.g., reduce EMI, increase savings).
# # **Formatting Instructions:**
# # - Use `<span style="color: #F2CB5A;">...</span>` to highlight **positive** numbers, strengths, and key terms.
# # - Use `<span style="color: #FF6B6B;">...</span>` to highlight **negative** numbers, weaknesses, or areas for improvement.
# # - Add `<br>` after each point.
# # - Do not include any other message like 'Here is your summary'.
# # - Maximum length should be 500 characters.
# # Financial Data:
# # {json.dumps(combined_data, indent=2)}
# # """


# # def generate_pdf_summary(combined_data, summary_text, file_name="financial_summary_report.pdf"):
# #     """
# #     Generate a PDF summary report of the user's financial wealth.

# #     Args:
# #         combined_data (dict): Dictionary containing the financial data.
# #         summary_text (str): A summary of the financial health generated from the LLM.
# #         file_name (str): The name of the PDF file to be saved.
    
# #     Returns:
# #         None
# #     """
# #     # Create instance of FPDF class
# #     pdf = FPDF()
# #     pdf.set_auto_page_break(auto=True, margin=15)
    
# #     # Add a page
# #     pdf.add_page()

# #     # Set title
# #     pdf.set_font('Arial', 'B', 16)
# #     pdf.cell(200, 10, txt="Financial Wealth Summary Report", ln=True, align='C')

# #     # Set subheading for the financial health summary
# #     pdf.ln(10)  # Line break
# #     pdf.set_font('Arial', 'B', 12)
# #     pdf.cell(200, 10, txt="Financial Health Summary", ln=True, align='L')

# #     # Add summary text from the LLM
# #     pdf.ln(5)
# #     pdf.set_font('Arial', '', 12)
# #     pdf.multi_cell(0, 10, txt=summary_text)

# #     # Add detailed financial data below the summary
# #     pdf.ln(10)
# #     pdf.set_font('Arial', 'B', 12)
# #     pdf.cell(200, 10, txt="Detailed Financial Data", ln=True, align='L')
    
# #     # Loop through the combined_data to extract and display key financial data
# #     pdf.ln(5)
# #     pdf.set_font('Arial', '', 12)
# #     for tool, data in combined_data.items():
# #         pdf.cell(200, 10, txt=f"{tool.replace('_', ' ').title()}: ", ln=True)
# #         # Check if data is a dictionary (e.g., net worth or investments)
# #         if isinstance(data, dict):
# #             for key, value in data.items():
# #                 pdf.cell(200, 10, txt=f"  - {key.title()}: {value}", ln=True)
# #         else:
# #             pdf.cell(200, 10, txt=f"  - {data}", ln=True)

# #     # Save the PDF to file
# #     pdf.output(file_name)
# #     print(f"PDF report generated and saved as {file_name}")


# # def get_financial_summary():
# #     """Fetch data from MCP tools and generate a financial health summary using Gemini."""
# #     session_id = st.session_state.get("session_id")
# #     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
# #     tools = ["fetch_net_worth", "fetch_mf_transactions", "fetch_stock_transactions", "fetch_credit_report"]
    
# #     # Fetch the combined data from MCP tools
# #     combined_data = fetch_financial_data(tools, session_id, base_url)

# #     # Create summary prompt for LLM
# #     prompt = generate_summary_prompt(combined_data)

# #     try:
# #         # Get the summary from Gemini
# #         summary = get_vertex_response(prompt)
# #         return summary.strip()
# #     except Exception as e:
# #         return f"⚠️ Error generating summary: {e}"


# def pdf_financial_summary():
#     """Fetch data from MCP tools and generate a PDF financial wealth report."""
#     session_id = st.session_state.get("session_id")
#     base_url = "https://fi-mcp-mock-292450254722.us-central1.run.app"
#     tools = ["fetch_net_worth", "fetch_mf_transactions", "fetch_stock_transactions", "fetch_credit_report"]

#     # Fetch the combined data from MCP tools
#     combined_data = fetch_financial_data(tools, session_id, base_url)

#     # Create summary prompt for LLM (for PDF generation)
#     prompt = pdf_generate_summary_prompt(combined_data, is_pdf=True)

#     try:
#         # Get the summary from Gemini
#         summary = get_vertex_response(prompt)

#         # Generate the PDF report with the summary
#         generate_pdf_summary(combined_data, summary.strip())

#         return summary.strip()
#     except Exception as e:
#         return f"⚠️ Error generating PDF summary: {e}"













############################### Fourth Version ###############
from fpdf import FPDF

def generate_summary_pdf(summary_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Load the DejaVuSans font from the correct path
    pdf.add_font('DejaVu', '','/app/modules/font/DejaVuSans.ttf', uni=True) 
    # pdf.add_font('DejaVu', '', '/workspaces/AgenticAI-Hackthon/src/UI/modules/font/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)
    
    # Set the width of the cell and wrap the text correctly
    width = 190  # Adjust the width as per your page layout
    
    # Use multi_cell to wrap text within the specified width
    pdf.multi_cell(width, 10, summary_text)
    
    # Save the PDF to a file
    file_name = "/tmp/financial_summary.pdf"
    pdf.output(file_name)
    
    return file_name


# ############################################## Third VERSION ##################################################
# from fpdf import FPDF
# from datetime import datetime
# import os

# class PDF(FPDF):
#     def __init__(self):
#         super().__init__()
#         self.set_auto_page_break(auto=True, margin=15)
#         self.add_page()
#         self._setup_fonts()

#     def _setup_fonts(self):
#         font_path = os.path.abspath(
#             os.path.join(os.path.dirname(__file__), "../.streamlit/font/DejaVuSans.ttf")
#         )
#         self.add_font("DejaVu", "", font_path, uni=True)
#         self.set_font("DejaVu", size=12)

#     def add_title(self, text):
#         self.set_font("DejaVu", size=16)
#         self.cell(0, 10, text, ln=True)
#         self.ln(2)

#     def add_date(self):
#         self.set_font("DejaVu", size=11)
#         self.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
#         self.ln(2)

#     def add_section_header(self, title):
#         self.set_font("DejaVu", size=13)
#         self.set_text_color(33, 33, 33)
#         self.cell(0, 10, title, ln=True)
#         self.ln(1)

#     def add_paragraph(self, text):
#         self.set_font("DejaVu", size=11)
#         self.set_text_color(0)
#         for line in text.strip().split("\n"):
#             self.multi_cell(0, 8, line)
#         self.ln(2)

#     def add_news_list(self, news_list):
#         self.add_section_header("📢 Related Market News:")
#         for item in news_list:
#             title = item.get("title", "No Title")
#             link = item.get("link", "#")
#             self.multi_cell(0, 7, f"• {title}\n{link}")
#             self.ln(1)


# def generate_summary_pdf(summary_text, news_list=None, filename="Financial_Summary.pdf"):
#     pdf = PDF()
#     pdf.add_title("AI-Generated Financial Health Report")
#     pdf.add_date()

#     pdf.add_section_header("Summary:")
#     pdf.add_paragraph(summary_text)

#     if news_list:
#         pdf.add_news_list(news_list)

#     pdf.output(filename)
#     return filename

# def generate_chat_summary_pdf(messages, filename="Chat_Summary.pdf"):
#     from fpdf import FPDF
#     from datetime import datetime
#     from pathlib import Path

#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     font_path = Path(__file__).resolve().parent.parent / "UI/.streamlit/font/DejaVuSans.ttf"
#     pdf.add_font("DejaVu", "", str(font_path), uni=True)
#     pdf.set_font("DejaVu", size=12)

#     pdf.set_font("DejaVu", "B", 16)
#     pdf.cell(0, 10, "Chat Summary", ln=True)
#     pdf.set_font("DejaVu", "", 12)
#     pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

#     pdf.set_font("DejaVu", "", 12)
#     for msg in messages:
#         role = "🧑 User" if msg["role"] == "user" else "🤖 Assistant"
#         content = msg["content"]
#         pdf.multi_cell(0, 10, f"{role}:\n{content}\n", border=0)

#     pdf.output(filename)
#     return filename


############################################## SECOND VERSION ##################################################
# modules/pdf_writer.py
# from fpdf import FPDF
# from datetime import datetime
# import os

# # Define absolute path to DejaVuSans.ttf
# FONT_PATH = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../modules/font/DejaVuSans.ttf")
# )
# # FONT_PATH = os.path.abspath(
# #     os.path.join(os.path.dirname(__file__), "../.streamlit/font/DejaVuSans.ttf")
# # )

# class PDF(FPDF):
#     pass

# def generate_summary_pdf(summary_text, news_list=None, filename="Financial_Summary.pdf"):
#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # Register Unicode font manually
#     pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
#     pdf.set_font("DejaVu", size=16)
#     pdf.cell(0, 10, "AI-Generated Financial Health Report", ln=True)

#     pdf.set_font("DejaVu", size=12)
#     pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

#     # Summary Section
#     pdf.set_font("DejaVu", size=14)
#     pdf.cell(0, 10, "Summary:", ln=True)

#     pdf.set_font("DejaVu", size=12)
#     for line in summary_text.split("\n"):
#         pdf.multi_cell(0, 10, line)

#     # News Section
#     if news_list:
#         pdf.set_font("DejaVu", size=14)
#         pdf.cell(0, 10, "Related Market News:", ln=True)

#         pdf.set_font("DejaVu", size=12)
#         for item in news_list:
#             pdf.multi_cell(0, 10, f"• {item['title']}\n{item['link']}")

#     pdf.output(filename)
#     return filename









####################################################### FIRST VERSION ####################################################
# from fpdf import FPDF
# from datetime import datetime
# import os

# # Dynamically find the DejaVuSans.ttf path
# FONT_PATH = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), "../.streamlit/font/DejaVuSans.ttf")
# )

# def generate_summary_pdf(summary_text, news_list=None, filename="Financial_Summary.pdf"):
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # ✅ Register and use Unicode-safe font
#     pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
#     pdf.set_font("DejaVu", size=16)
#     pdf.cell(0, 10, "🤖 AI-Generated Financial Health Report", ln=True)

#     # Date
#     pdf.set_font("DejaVu", size=12)
#     pdf.cell(0, 10, f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

#     # Summary
#     pdf.set_font("DejaVu", style="B", size=14)
#     pdf.cell(0, 10, "💡 Summary:", ln=True)
#     pdf.set_font("DejaVu", size=12)
#     for line in summary_text.split("\n"):
#         pdf.multi_cell(0, 10, line)

#     # News
#     if news_list:
#         pdf.set_font("DejaVu", style="B", size=14)
#         pdf.cell(0, 10, "📰 Related Market News:", ln=True)
#         pdf.set_font("DejaVu", size=12)
#         for item in news_list:
#             pdf.multi_cell(0, 10, f"• {item['title']}\n{item['link']}")
#             pdf.ln(1)

#     pdf.output(filename)
#     return filename
