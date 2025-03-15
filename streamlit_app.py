import streamlit as st
import openai
from dotenv import load_dotenv
import os
from chatbot import generate_chat_response  
from planmytrip import plan_my_trip
from conversion import get_conversion

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration
st.set_page_config(page_title="Trippin", layout="wide")

# Initialize session state for active tab
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Home"  # Default tab

# Function to switch tabs
def switch_tab(tab_name):
    st.session_state["active_tab"] = tab_name
    st.rerun()  # Refresh UI to reflect change

# Custom CSS for aligning navigation buttons to the right & styling the "Get Started" button
st.markdown(
    """
    <style>
        /* Align navigation buttons to the right */
        .nav-container {
            display: flex;
            justify-content: flex-end;
            align-items: ;
            padding: 10px 40px;
            gap: 25px;
        }

        /* Navigation button styling */
        .stButton > button {
            background: none;
            border: none;
            color: black;
            font-size: 18px;
            cursor: pointer;
            font-weight: bold;
        }

        /* Hover effect for navigation buttons */
        .stButton > button:hover {
            text-decoration: underline;
        }

        /* Style for the 'Get Started' button */
        .get-started-container {
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }
        .get-started {
            background-color: #FF7F9F;
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 12px 24px;
            border: 2px solid #ff5c8a;
            border-radius: 8px;
            cursor: pointer;    
            text-align: center;
        }
        .get-started-button:hover {
            background-color: #ff5c8a;
            border-color: #ff3d6e;
        }

        /* Styling for the Trippin button text */
        div[data-testid="stButton"] > button {
            font-size: 24px !important;  /* Larger font */
            font-weight: bold !important;
            color: #FF7F9F !important;  /* Pink text */
            background: none !important;
            border: none !important;
            cursor: pointer;
        }
        div[data-testid="stButton"] > button:hover {
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation Bar (properly aligned to the right)
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([8, 1, 1.5, 0.6])  # Push buttons to the right

with col1:
    if st.button("Trippin", key="home_tab"):
        switch_tab("Home")
with col2:
    if st.button("Plan My Trip", key="trip_tab"):
        switch_tab("Plan My Trip")
with col3:
    if st.button("Currency Converter", key="convert_tab"):
        switch_tab("Convert")
with col4:
    if st.button("Chat", key="chat_tab"):
        switch_tab("Chat")
st.markdown('</div>', unsafe_allow_html=True)

# Render content based on the active tab
if st.session_state["active_tab"] == "Home":
    st.markdown(
    """
    <h1 style="text-align: center;">Craft Unforgettable Itineraries with AI Trip Planner</h1>
    <p style="text-align: center; font-size:18px;">Your personal trip planner and travel curator, creating custom itineraries tailored to your interests and budget.</p>
    """,
    unsafe_allow_html=True
)
    
    col1, col2, col3 = st.columns([5, 2, 5])

    with col2:  # Center column
        if st.button("Get started—it's free", key="get_started"):
            switch_tab("Plan My Trip")  # Redirect to "Plan My Trip" tab

elif st.session_state["active_tab"] == "Plan My Trip":
    plan_my_trip()

elif st.session_state["active_tab"] == "Chat":
    st.header("Chat with AI")
    st.write("Ask travel-related questions and get instant recommendations.")
    generate_chat_response()

elif st.session_state["active_tab"] == "Convert":
    get_conversion()
