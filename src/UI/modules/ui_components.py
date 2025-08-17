import streamlit as st
import re # Import regex for advanced string parsing

def render_kpi_card(title: str, value, unit: str, change, icon: str, benchmark: str = None):
    """
    Renders a single KPI card with a title, value, change metric, and an optional benchmark,
    styled to match the fi.money theme.
    Enhanced to color change text red for negative values and green for positive values,
    even when the change string includes descriptive text (e.g., '▼ 4,089 from 2025-06').

    Args:
        title (str): The title of the KPI.
        value: The main value of the KPI.
        unit (str): The unit for the value (e.g., '$', '%', '₹').
        change: The change value (can be float, str like '4.2%', or None).
        icon (str): An emoji icon for the KPI.
        benchmark (str, optional): Text indicating a benchmark comparison (e.g., "Average ➡️", "Poor ❌"). Defaults to None.
    """
    st.markdown("""
    <style>
    .kpi-card-themed {
        background-color: #152320; /* Consistent background */
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 24px;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s ease-in-out;
        text-align: center; /* Center align main content like title and value */
    }
    .kpi-card-themed:hover {
        border-color: #F2CB5A;
    }
    .kpi-title-container {
        display: flex;
        align-items: center; /* Align icon and title vertically */
        justify-content: center; /* Center align items horizontally */
        flex-wrap: wrap; /* Allow wrapping if text is too long */
        margin-bottom: 8px; /* Space below title container */
    }
    .kpi-icon-display {
        font-size: 14px;
        color: #8B949E;
        margin-right: 4px;
    }
    .kpi-title-text {
        font-size: 16px;
        color: #8B949E;
    }
    .kpi-benchmark-good {
        color: #3FB950; /* Green for good */
    }
    .kpi-benchmark-average {
        color: #F2CB5A; /* Yellow/Orange for average */
    }
    .kpi-benchmark-poor {
        color: #F85149; /* Red for poor/critical alerts */
    }
    .kpi-value-themed {
        font-size: 38px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .kpi-value-unit {
        font-size: 38px;
        font-weight: 700;
        color: #FFFFFF; /* Ensure unit color is white for consistency with value */
        margin-left: 4px;
    }
    /* For Rupee symbol, remove margin-left as it will be prepended */
    .kpi-value-unit.prefixed {
        margin-left: 0;
        margin-right: 4px; /* Small space between symbol and value */
    }

    .kpi-change-positive-themed {
        font-size: 14px;
        color: #3FB950;
        font-weight: 600;
    }
    .kpi-change-negative-themed {
        font-size: 14px;
        color: #F85149;
        font-weight: 600;
    }
    .kpi-details-themed {
        font-size: 12px;
        color: #8B949E;
        margin-top: 0; /* Remove default paragraph margin */
        margin-bottom: 0;
        text-align: right; /* Ensure 'More Details' is right-aligned */
    }
    .kpi-value-wrapper {
        margin-top: 8px; /* Keep the top margin as specified */
        margin-bottom: 0; /* Explicitly remove default bottom margin */
        padding: 0; /* Remove any default padding */
    }

    .kpi-footer {
        display: flex;
        justify-content: space-between; /* Pushes items to ends */
        align-items: center; /* Vertically centers items */
        width: 100%;
        padding: 0 10px; /* Some horizontal padding for internal spacing */
        box-sizing: border-box; /* Include padding in width calculation */
        min-height: 20px; /* Ensure some height even if content is small */
    }
    .kpi-alert-text { /* For the left-aligned alert/change text */
        font-size: 14px;
        font-weight: 600;
        text-align: left; /* Explicitly left-align */
        flex-grow: 1; /* Allows it to take up available space */
        line-height: 1.2; /* Better vertical alignment */
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        # --- Format the value display ---
        display_value_html = ""
        formatted_value_str = ""
        try:
            numeric_value = float(value)
            formatted_value_str = f"{numeric_value:,.0f}"
        except (ValueError, TypeError):
            formatted_value_str = str(value)

        if isinstance(value, (int, float)):
            if value < 0 and not formatted_value_str.startswith('-'):
                formatted_value_str = '-' + formatted_value_str
        elif isinstance(value, str) and value.strip().startswith('-') and not formatted_value_str.startswith('-'):
            formatted_value_str = '-' + formatted_value_str

        if unit == '$':
            display_value_html = f"<span class='kpi-value-themed'>${formatted_value_str}</span>"
        elif unit == '₹':
            # Rupee symbol in front, with specific styling
            display_value_html = f"<span class='kpi-value-unit prefixed'>₹</span><span class='kpi-value-themed'>{formatted_value_str}</span>"
        elif unit == '%':
            display_value_html = f"<span class='kpi-value-themed'>{formatted_value_str}</span><span class='kpi-value-unit'>%</span>"
        else:
            # General case for other units or no unit
            display_value_html = f"<span class='kpi-value-themed'>{formatted_value_str}</span><span class='kpi-value-unit'>{unit}</span>" if unit else f"<span class='kpi-value-themed'>{formatted_value_str}</span>"

        # --- Determine alert/change text and color for the footer ---
        alert_text_display = "NA" # Default if no specific change or alert
        alert_color_class = "kpi-details-themed" # Neutral default

        # Priority 1: Check for explicit "alert" keywords in 'change' or 'benchmark'
        if isinstance(change, str) and ("⚠️" in change or "High risk" in change or "❗" in change or "🔴" in change or "Poor" in change or "Missed" in change):
            alert_text_display = change
            alert_color_class = "kpi-benchmark-poor"
        elif benchmark and ("poor" in benchmark.lower() or "red" in benchmark.lower() or "critical" in benchmark.lower() or "🔻" in benchmark.lower() or "high risk" in benchmark.lower()):
            alert_text_display = benchmark
            alert_color_class = "kpi-benchmark-poor"
        # NEW CHECK: If change is exactly '-', display "NA"
        elif isinstance(change, str) and change.strip() == '-':
            alert_text_display = "NA"
            alert_color_class = "kpi-details-themed" # Neutral color for NA
        # Priority 2: If no explicit alert, attempt to parse numeric change or detect keywords
        elif change is not None and change != '':
            alert_text_display = str(change) # Default to original change string

            # Attempt to extract a numeric value from the change string
            numeric_change = None
            # Regex to find a number, optionally preceded by + or - or ▼/▲, and including commas/decimals
            # It tries to find the first numerical sequence that could represent a change.
            cleaned_change_for_num = str(change).replace('▼', '-').replace('▲', '').replace(',', '')
            match = re.search(r'([-+]?\d+(\.\d+)?)', cleaned_change_for_num)
            if match:
                try:
                    numeric_change = float(match.group(1))
                except ValueError:
                    pass # Keep numeric_change as None if conversion fails

            if numeric_change is not None:
                # If a numeric change is found, use its sign for coloring
                alert_color_class = "kpi-change-positive-themed" if numeric_change >= 0 else "kpi-change-negative-themed"
            else:
                # If no clear numeric change, fall back to keyword detection for coloring
                negative_keywords = ['▼', '-', 'down', 'loss', 'poor', 'critical', 'missed', 'below']
                positive_keywords = ['▲', '+', 'up', 'gain', 'good', 'above', 'acceptable'] # Added acceptable as per previous logic

                is_negative = any(keyword in alert_text_display.lower() for keyword in negative_keywords)
                is_positive = any(keyword in alert_text_display.lower() for keyword in positive_keywords)

                if is_negative and not is_positive:
                    alert_color_class = "kpi-change-negative-themed"
                elif is_positive and not is_negative:
                    alert_color_class = "kpi-change-positive-themed"
                elif "Average" in alert_text_display or "➡️" in alert_text_display:
                    alert_color_class = "kpi-benchmark-average"
                else:
                    alert_color_class = "kpi-details-themed" # Neutral for other descriptive texts
        # If all above fail, alert_text_display remains "NA" and color is neutral

        # The footer detail HTML (always "More Details")
        footer_detail_html = "<p class='kpi-details-themed'>More Details &gt;</p>"

        # --- Render the card ---
        st.markdown(f"""
        <div class="kpi-card-themed">
            <div>
                <div class="kpi-title-container">
                  <span class="kpi-icon-display">{icon}</span>
                  <span class="kpi-title-text">{title}</span>
                </div>
            <p class="kpi-value-wrapper">{display_value_html}</p>
            </div>
            <div class="kpi-footer">
                <span class="kpi-alert-text {alert_color_class}">{alert_text_display}</span>
                {footer_detail_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

# import streamlit as st


# def render_kpi_card(title: str, value, unit: str, change, icon: str, benchmark: str = None):
#     """
#     Renders a single KPI card with a title, value, change metric, and an optional benchmark,
#     styled to match the fi.money theme.

#     Args:
#         title (str): The title of the KPI.
#         value: The main value of the KPI.
#         unit (str): The unit for the value (e.g., '$', '%', '₹').
#         change: The change value (can be float, str like '4.2%', or None).
#         icon (str): An emoji icon for the KPI.
#         benchmark (str, optional): Text indicating a benchmark comparison (e.g., "Average ➡️", "Poor ❌"). Defaults to None.
#     """
#     st.markdown("""
#     <style>
#     .kpi-card-themed {
#         background-color: #152320; /* Consistent background */
#         border: 1px solid #30363D;
#         border-radius: 12px;
#         padding: 24px;
#         height: 200px;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#         transition: all 0.2s ease-in-out;
#         text-align: center; /* Center align main content like title and value */
#     }
#     .kpi-card-themed:hover {
#         border-color: #F2CB5A;
#     }
#     .kpi-title-container {
#         display: flex;
#         align-items: center; /* Align icon and title vertically */
#         justify-content: center; /* Center align items horizontally */
#         flex-wrap: wrap; /* Allow wrapping if text is too long */
#         margin-bottom: 8px; /* Space below title container */
#     }
#     .kpi-icon-display {
#         font-size: 14px;
#         color: #8B949E;
#         margin-right: 4px;
#     }
#     .kpi-title-text {
#         font-size: 16px;
#         color: #8B949E;
#     }
#     .kpi-benchmark-good {
#         color: #3FB950; /* Green for good */
#     }
#     .kpi-benchmark-average {
#         color: #F2CB5A; /* Yellow/Orange for average */
#     }
#     .kpi-benchmark-poor {
#         color: #F85149; /* Red for poor/critical alerts */
#     }
#     .kpi-value-themed {
#         font-size: 38px;
#         font-weight: 700;
#         color: #FFFFFF;
#         line-height: 1.2;
#     }
#     .kpi-value-unit {
#         font-size: 38px;
#         font-weight: 700;
#         color: #FFFFFF; /* Ensure unit color is white for consistency with value */
#         margin-left: 4px;
#     }
#     /* For Rupee symbol, remove margin-left as it will be prepended */
#     .kpi-value-unit.prefixed {
#         margin-left: 0;
#         margin-right: 4px; /* Small space between symbol and value */
#     }

#     .kpi-change-positive-themed {
#         font-size: 14px;
#         color: #3FB950;
#         font-weight: 600;
#     }
#     .kpi-change-negative-themed {
#         font-size: 14px;
#         color: #F85149;
#         font-weight: 600;
#     }
#     .kpi-details-themed {
#         font-size: 12px;
#         color: #8B949E;
#         margin-top: 0; /* Remove default paragraph margin */
#         margin-bottom: 0;
#         text-align: right; /* Ensure 'More Details' is right-aligned */
#     }
#     .kpi-value-wrapper {
#     margin-top: 8px; /* Keep the top margin as specified */
#     margin-bottom: 0; /* Explicitly remove default bottom margin */
#     padding: 0; /* Remove any default padding */
#     }
                
#     .kpi-footer {
#         display: flex;
#         justify-content: space-between; /* Pushes items to ends */
#         align-items: center; /* Vertically centers items */
#         width: 100%;
#         padding: 0 10px; /* Some horizontal padding for internal spacing */
#         box-sizing: border-box; /* Include padding in width calculation */
#         min-height: 20px; /* Ensure some height even if content is small */
#     }
#     .kpi-alert-text { /* For the left-aligned alert/change text */
#         font-size: 14px;
#         font-weight: 600;
#         text-align: left; /* Explicitly left-align */
#         flex-grow: 1; /* Allows it to take up available space */
#         line-height: 1.2; /* Better vertical alignment */
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     with st.container():
#         # --- Format the value display ---
#         display_value_html = ""
#         if unit == '$':
#             display_value_html = f"<span class='kpi-value-themed'>${value:,.0f}</span>"
#         elif unit == '₹':
#             # Rupee symbol in front, with specific styling
#             display_value_html = f"<span class='kpi-value-unit prefixed'>₹</span><span class='kpi-value-themed'>{value:,.0f}</span>"
#         elif unit == '%':
#             display_value_html = f"<span class='kpi-value-themed'>{str(value)}</span><span class='kpi-value-unit'>%</span>"
#         else:
#             # General case for other units or no unit
#             display_value_html = f"<span class='kpi-value-themed'>{value:,.0f}</span><span class='kpi-value-unit'>{unit}</span>" if unit else f"<span class='kpi-value-themed'>{value:,.0f}</span>"

#         # --- Determine alert/change text and color for the footer ---
#         alert_text_display = "–" # Default if no specific change or alert
#         alert_color_class = "kpi-details-themed" # Neutral default

#         # Priority 1: Check for explicit "alert" keywords in 'change' or 'benchmark'
#         if isinstance(change, str) and ("⚠️" in change or "High risk" in change or "❗" in change or "🔴" in change or "Poor" in change or "Missed" in change):
#             alert_text_display = change
#             alert_color_class = "kpi-benchmark-poor"
#         elif benchmark and ("poor" in benchmark.lower() or "red" in benchmark.lower() or "critical" in benchmark.lower() or "🔻" in benchmark.lower() or "high risk" in benchmark.lower()):
#             alert_text_display = benchmark
#             alert_color_class = "kpi-benchmark-poor"
#         # Priority 2: If no explicit alert, check for numeric change
#         elif change is not None and change != '':
#             try:
#                 numeric_change = float(str(change).replace('%', '').strip())
#                 change_indicator = "▲" if numeric_change >= 0 else "▼"
#                 alert_color_class = "kpi-change-positive-themed" if numeric_change >= 0 else "kpi-change-negative-themed"
#                 change_unit = '%' if '%' in str(change) or unit == '%' or title.lower().__contains__('rate') else ''
#                 alert_text_display = f"{change_indicator} {abs(numeric_change):.1f}{change_unit} vs last period"
#             except (ValueError, TypeError):
#                 # Priority 3: If not numeric, and not an explicit alert, display as general descriptive text
#                 alert_text_display = str(change)
#                 if "Acceptable" in str(change) or "Good" in str(change) or "✅" in str(change) or "🟢" in str(change):
#                     alert_color_class = "kpi-change-positive-themed"
#                 elif "Average" in str(change) or "➡️" in str(change):
#                     alert_color_class = "kpi-benchmark-average"
#                 else:
#                     alert_color_class = "kpi-details-themed" # Neutral for other descriptive texts
#         # If all above fail, alert_text_display remains "–" and color is neutral

#         # The footer detail HTML (always "More Details")
#         footer_detail_html = "<p class='kpi-details-themed'>More Details &gt;</p>"

#         # --- Render the card ---
#         st.markdown(f"""
#         <div class="kpi-card-themed">
#             <div>
#                 <div class="kpi-title-container">
#                   <span class="kpi-icon-display">{icon}</span>
#                   <span class="kpi-title-text">{title}</span>
#                 </div>
#             <p class="kpi-value-wrapper">{display_value_html}</p>
#             </div>
#             <div class="kpi-footer">
#                 <span class="kpi-alert-text {alert_color_class}">{alert_text_display}</span>
#                 {footer_detail_html}
#             </div>
#         </div>
#         """, unsafe_allow_html=True)















################################### KARTHIK #####################################
#  # modules/ui_components.py
# # Contains functions for rendering specific UI components.

# import streamlit as st

# def render_kpi_card(title: str, value, unit: str, change: float, icon: str,benchmark: str=None):
#     """
#     Renders a single KPI card with a title, value, and change metric,
#     styled to match the fi.money theme.

#     Args:
#         title (str): The title of the KPI.
#         value: The main value of the KPI.
#         unit (str): The unit for the value (e.g., '$', '%').
#         change (float): The change value (positive or negative).
#         icon (str): An emoji icon for the KPI.
#     """
#     # This CSS is scoped to the KPI card component.
#     # The main page styles are applied in the page scripts.
#     st.markdown("""
#     <style>
#     .kpi-card-themed {
#         background-color: #152320;
#         border: 1px solid #30363D;
#         border-radius: 12px;
#         padding: 24px;
#         height: 200px; /* Fixed height for alignment */
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#         transition: all 0.2s ease-in-out;
#     }
#     .kpi-card-themed:hover {
#         border-color: #F2CB5A;
#     }
#     .kpi-title-themed {
#         font-size: 16px;
#         color: #8B949E; /* Light gray */
#     }
#     .kpi-value-themed {
#         font-size: 38px;
#         font-weight: 700;
#         color: #FFFFFF; /* White for main value */
#         line-height: 1.2;
#     }
#     .kpi-value-unit {
#         font-size: 30px;
#         font-weight: 600;
#         color: #8B949E; /* Muted color for the unit */
#         margin-left: 4px;
#     }
#     .kpi-change-positive-themed {
#         font-size: 14px;
#         color: #3FB950; /* Green */
#         font-weight: 600;
#     }
#     .kpi-change-negative-themed {
#         font-size: 14px;
#         color: #F85149; /* Red */
#         font-weight: 600;
#     }
#     .kpi-details-themed {
#         font-size: 12px;
#         color: #8B949E;
#         text-align: right;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     with st.container():
#         # Formatting value based on unit
#         if unit == '$':
#             formatted_value = f"${value:,.0f}"
#             display_value_html = f"<span class='kpi-value-themed'>{formatted_value}</span>"
#         elif unit == '%':
#             formatted_value = f"{value}"
#             display_value_html = f"<span class='kpi-value-themed'>{formatted_value}</span><span class='kpi-value-unit'>%</span>"
#         else:
#             formatted_value = f"{value}"
#             display_value_html = f"<span class='kpi-value-themed'>{formatted_value}</span>"


#         # Formatting change indicator
#         change_indicator = "▲" if change >= 0 else "▼"
#         change_color_class = "kpi-change-positive-themed" if change >= 0 else "kpi-change-negative-themed"
#         change_unit = '%' if '%' in title or title == "Savings Rate" else ''
#         change_text = f"{change_indicator} {abs(change):.1f}{change_unit}"

#         st.markdown(f"""
#         <div class="kpi-card-themed">
#             <div>
#                 <span class="kpi-title-themed">{icon} {title}</span>
#                 <p style="margin-top: 8px;">{display_value_html}</p>
#             </div>
#             <div>
#                 <span class="{change_color_class}">{change_text} vs last period</span>
#                 <p class="kpi-details-themed">More Details &gt;</p>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)