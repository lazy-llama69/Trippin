import streamlit as st
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key="")

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
col1, col2, col3 = st.columns([8, 1, 1])  # Push buttons to the right
with col3:
    if st.button("Chat", key="chat_tab"):
        switch_tab("Chat")
with col2:
    if st.button("Plan My Trip", key="trip_tab"):
        switch_tab("Plan My Trip")
with col1:
    if st.button("Trippin", key="home_tab"):
        switch_tab("Home")

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
    st.markdown("<h2 style='text-align: center;'>Tell us your travel preferences</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Just provide some basic information, and our trip planner will generate a customized itinerary based on your preferences.</p>", unsafe_allow_html=True)

    # Create layout with empty space on both sides
    left_space, form, right_space = st.columns([1, 4, 1])

    with form:
        # Destination input
        st.markdown("### What is your destination of choice?")
        destination = st.text_input("What is your destination of choice?", placeholder="Enter your destination", label_visibility="collapsed")

        st.markdown("---")  # Horizontal separator

        # Travel date input
        st.markdown("### When are you planning to travel?")
        travel_date = st.date_input("When are you planning to travel?", format="YYYY-MM-DD", label_visibility="collapsed")

        st.markdown("---")  # Horizontal separator

        # Number of travel days
        st.markdown("### How many days are you planning to travel?")
        num_days = st.number_input("How many days are you planning to travel?", min_value=1, max_value=60, value=7, label_visibility="collapsed")

        st.markdown("---")  # Horizontal separator

        # Budget selection
        st.markdown("### What is Your Budget?")
        budget = st.radio("What is Your Budget?", ["Low (0 - 1000 USD)", "Medium (1000 - 2500 USD)", "High (2500+ USD)"], horizontal=True, label_visibility="collapsed")

        st.markdown("---")  # Horizontal separator

        # Travel companions selection
        st.markdown("### Who do you plan on traveling with on your next adventure?")
        companions = st.multiselect("Who do you plan on traveling with on your next adventure?", ["👤 Solo", "👫 Couple", "👨‍👩‍👧 Family", "👬 Friends"], label_visibility="collapsed")

        st.markdown("---")  # Horizontal separator

        # Activity selection
        st.markdown("### Which activities are you interested in?")
        activities = st.multiselect(
            "Which activities are you interested in?",
            [
                "Beaches", "City Sightseeing", "Outdoor Adventures", "Festivals/Events",
                "Food Exploration", "Nightlife", "Shopping", "Spa Wellness"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")  # Horizontal separator

        # Dietary preferences
        st.markdown("### Would you like to have these options?")
        dietary_options = st.multiselect(" Would you like to have these options?", ["Halal", "Vegetarian"],label_visibility="collapsed")

        st.markdown("---")  # Horizontal separator

        # Additional requirements section
        st.markdown("### Any additional requirements?")
        additional_requirements = st.text_area(
            "Enter any specific locations, allergens, or preferences:",
            placeholder="E.g., I want to visit the Eiffel Tower, avoid peanuts, need wheelchair accessibility...",
            label_visibility="collapsed"
        )

        st.markdown("---")  # Horizontal separator

        # Submit button
        submit = st.button("Submit", key="submit_preferences", help="Generate your custom itinerary")

        if submit:
            # Collect all inputs
            user_preferences = {
                "destination": destination,
                "travel_date": travel_date.strftime("%Y-%m-%d"),
                "num_days": num_days,
                "budget": budget,
                "companions": companions,
                "activities": activities,
                "dietary_options": dietary_options,
                "additional_requirements": additional_requirements
            }

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful travel assistant."},
                    {"role": "user", "content": f"Generate a custom travel itinerary based on the following preferences: {user_preferences}"}
                ],
                max_tokens=500
            )

            # Display the generated itinerary
            st.markdown("### Your Custom Itinerary")
            st.write(response.choices[0].message.content)

elif st.session_state["active_tab"] == "Chat":
    st.header("Chat with AI")
    st.write("Ask travel-related questions and get instant recommendations.")