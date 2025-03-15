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
col1, col2, col3, col4, col5 = st.columns([7, 1, 1.5, 1.8, 1.5])  # Push buttons to the right

with col1:
    st.image("assets/logo.png", width=300)
with col2:
    if st.button("Home", key="home_tab"):
        switch_tab("Home")
with col3:
    if st.button("Plan My Trip", key="trip_tab"):
        switch_tab("Plan My Trip")
with col4:
    if st.button("Currency Converter", key="convert_tab"):
        switch_tab("Convert")
with col5:
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

    st.markdown("<h2 style='text-align: center;'>🌟 Tourist Recommendations 🌟</h2>", unsafe_allow_html=True)

    trip_col1, trip_col2, trip_col3 = st.columns(3)

    if "selected_trip" not in st.session_state:
        st.session_state.selected_trip = None

    # Recommended Trip 1
    with trip_col1:
        st.image("assets/bali.jpg", use_column_width=True)
        st.markdown("### Bali, Indonesia")
        st.write("Experience breathtaking beaches, lush jungles, and vibrant culture.")
        if st.button("View", key="bali"):
            st.session_state.selected_trip = "Bali"

    # Recommended Trip 2
    with trip_col2:
        st.image("assets/paris.webp", use_column_width=True)
        st.markdown("### Paris, France")
        st.write("Visit the City of Love and explore its iconic landmarks and cafes.")
        if st.button("View", key="paris"):
            st.session_state.selected_trip = "Paris"

    # Recommended Trip 3
    with trip_col3:
        st.image("assets/tokyo.webp", use_column_width=True)
        st.markdown("### Tokyo, Japan")
        st.write("Discover a mix of futuristic cityscapes and traditional temples.")
        if st.button("View", key="tokyo"):
            st.session_state.selected_trip = "Tokyo"

    st.markdown("<hr>", unsafe_allow_html=True)  # Add a separator


    if st.session_state.selected_trip == "Bali":
        st.markdown("### 🌴 Best Places to Visit in Bali:")
        st.write("- **Uluwatu Temple** – Stunning cliffside views.")
        st.write("- **Tegallalang Rice Terraces** – Breathtaking landscapes.")
        st.write("- **Seminyak Beach** – Perfect for sunset lovers.")

        st.markdown("### 🍽️ Top Restaurants in Bali:")
        st.write("- **Locavore** – Award-winning fine dining.")
        st.write("- **Naughty Nuri’s** – Famous for ribs and cocktails.")

    elif st.session_state.selected_trip == "Paris":
        st.markdown("### 🗼 Best Places to Visit in Paris:")
        st.write("- **Eiffel Tower** – A must-see iconic landmark.")
        st.write("- **Louvre Museum** – Home of the Mona Lisa.")
        st.write("- **Champs-Élysées** – Perfect for shopping and cafes.")

        st.markdown("### 🍽️ Top Restaurants in Paris:")
        st.write("- **Le Meurice** – Michelin-starred luxury dining.")
        st.write("- **Le Petit Cambodge** – Amazing local food.")

    elif st.session_state.selected_trip == "Tokyo":
        st.markdown("### 🎌 Best Places to Visit in Tokyo:")
        st.write("- **Shibuya Crossing** – The world’s busiest intersection.")
        st.write("- **Senso-ji Temple** – Tokyo’s most famous temple.")
        st.write("- **Akihabara** – A paradise for anime and gaming lovers.")

        st.markdown("### 🍣 Top Restaurants in Tokyo:")
        st.write("- **Sukiyabashi Jiro** – World-famous sushi restaurant.")
        st.write("- **Ichiran Ramen** – Best solo ramen experience.")




elif st.session_state["active_tab"] == "Plan My Trip":
    plan_my_trip()

elif st.session_state["active_tab"] == "Chat":
    st.header("Chat with AI")
    st.write("Ask travel-related questions and get instant recommendations.")
    generate_chat_response()

# streamlit_app.py (excerpt)
elif st.session_state["active_tab"] == "Itinerary":
    from itinerary import display_itinerary  # Import the function
    display_itinerary()  # Call it to render the layout

elif st.session_state["active_tab"] == "Convert":
    get_conversion()


