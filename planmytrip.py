import streamlit as st
import openai
from dotenv import load_dotenv
import os
import re
from streamlit_extras.switch_page_button import switch_page

openai.api_key = st.secrets["openai"]["api_key"]

def plan_my_trip():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1rem !important; /* Adjust the top padding */
                padding-left: 6rem;
                padding-right: 6rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center;'>Tell us your travel preferences</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Just provide some basic information, and our trip planner will generate a customized itinerary based on your preferences.</p>", unsafe_allow_html=True)

    left_space, form, right_space = st.columns([1, 4, 1])

    with form:
        destination = st.text_input("What is your destination of choice?", placeholder="Enter your destination", key="destination_input")
        st.markdown("---")
        travel_date = st.date_input("When are you planning to travel?", format="YYYY-MM-DD", key="travel_date_input")
        st.markdown("---")
        num_days = st.number_input("How many days are you planning to travel?", min_value=1, max_value=60, value=5, key="num_days_input")
        st.markdown("---")
        budget = st.radio("What is Your Budget?", ["Low (0 - 1000 USD)", "Medium (1000 - 2500 USD)", "High (2500+ USD)"], horizontal=True, key="budget_input")
        st.markdown("---")
        companions = st.multiselect("Who do you plan on traveling with on your next adventure?", ["👤 Solo", "👫 Couple", "👨‍👩‍👧 Family", "👬 Friends"], key="companions_input")
        st.markdown("---")
        activities = st.multiselect(
            "Which activities are you interested in?",
            ["Beaches", "City Sightseeing", "Outdoor Adventures", "Festivals/Events", "Food Exploration", "Nightlife", "Shopping", "Spa Wellness"],
            key="activities_input"
        )
        st.markdown("---")
        dietary_options = st.multiselect("Would you like to have these options?", ["Halal", "Vegetarian"], key="dietary_options_input")
        st.markdown("---")
        additional_requirements = st.text_area("Enter any specific locations, allergens, or preferences:", placeholder="E.g., I want to visit the Eiffel Tower, avoid peanuts...", key="additional_requirements_input")
        st.markdown("---")

        submit = st.button("Submit", key="submit_preferences", help="Generate your custom itinerary", type="primary")

        if submit:
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

            # 1) Generate the itinerary (first GPT call)
            itinerary = generate_itinerary(user_preferences)
            st.session_state["itinerary"] = itinerary

            # 2) Extract places (second GPT call)
            places_json = extract_places_gpt(itinerary)

            # Basic validation before storing
            if not places_json.strip().startswith('['):
                st.error("Failed to extract valid places data")
                places_json = "[]"  # Fallback empty array

            st.session_state["addresses_data"] = places_json

            # 3) Extract location (regex-based function)
            st.session_state["destination"] = extract_location(itinerary)

            # 4) Switch to the itinerary tab and rerun
            st.session_state["active_tab"] = "Itinerary"
            st.rerun()

def generate_itinerary(user_preferences):
    with st.spinner("Generating your personalized itinerary..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant that generates fun and customized travel itineraries."},
                {"role": "user", "content": f"""
                    Generate a custom travel itinerary based on the following preferences:
                    
                    Location: {user_preferences['destination']}
                    Travel Date: {user_preferences['travel_date']}
                    Number of Days: {user_preferences['num_days']}
                    Budget: {user_preferences['budget']}
                    Companions: {user_preferences['companions']}
                    Activities: {', '.join(user_preferences['activities'])}
                    Dietary Options: {', '.join(user_preferences['dietary_options'])}
                    Additional Requirements: {user_preferences['additional_requirements']}
                    
                    Please strictly follow the instructions below:
                    
                    1. **Travel Name**: Generate a catchy, funny, and engaging name for the trip, like "Journey to {user_preferences['destination']}, make it ".
                    2. For each day of the itinerary, use headers with the day number and a short description.
                    3. For each day's activities, DO NOT use **bullet points**.
                    4. Make **important keywords bold**: 
                        - **Restaurants**, e.g., **The Eiffel Tower Restaurant**
                        - **Tourist Attractions**, e.g., **Louvre Museum**
                        - **Landmarks**, e.g., **Notre-Dame Cathedral**
                    5. Keep the tone fun, engaging, and descriptive.
                    6. Be detailed and have an estimated time for each activity 
                    7. Include the preferences separated by new line below the travel name.
                    8. Be specific with the names of the places to dine and the tourist attractions.
                    11. If location is empty, please put a specific place to go. 
                    12. If additional requirements is empty, keep additonal requirements none, do not generate a prompt for additional requirements
                    14. Try to make it a full day experience from 8:00 till 22:00 unless stated otherwise in additional requirements
                    15. Use this | symbol to separate the time and the activity for each day and then ALWAYS INCLUDE line break after each activity
                    16. After the final day in the itinerary, include additional suggestions that would be useful and beneficial for the tourist during the trip regarding (public transport, culture rules, etc.)
                    
                    Must include:
                    - Line break after each activity in a day
                    - The itinerary duration is equal to the number of days in preferences

                    Example Format:
                    
                    **Travel Name**: "Journey to Paris: A Culinary Adventure"
                    
                    'preferences'

                    Day 1: Arrival in Paris \n
                    10:00-11:00 | Visit the **Eiffel Tower** \n
                    11:00-11:30 | Enjoy a meal at **Le Cinq** (Michelin Star restaurant) \n
                    11:30-12:00 | Relax at **Tuileries Gardens** \n
                """},
            ],
            max_tokens=2500
        )
    return response.choices[0].message.content

def extract_places_gpt(itinerary_text):
    """
    Use a second GPT call to extract distinct places from the itinerary.
    Returns the structured information as JSON text.
    """
    prompt = f"""
        Extract distinct major landmarks and well-known places from this itinerary:
        {itinerary_text}

        Return JSON array with these keys for each entry:
        - "name": Exact place name (e.g., "Eiffel Tower")
        - "category": Type (Landmark, Museum, Restaurant)
        - "shortDescription": Brief 5-7 word description
        - "address": Full address if mentioned, else empty

        Rules:
        1. Only include internationally recognized places
        2. Exclude generic/local businesses
        3. Return ONLY valid JSON (no text/formatting outside the array)
        4. Ensure proper JSON syntax with double quotes
        5. Response must start with '[' and end with ']'
        6. Do not include backticks, comments, or any text before/after the JSON

        Example:
        [
        {{
            "name": "Tokyo Disneyland",
            "category": "Theme Park",
            "shortDescription": "Famous Disney theme park in Japan",
            "address": "1-1 Maihama, Urayasu, Chiba 279-0031, Japan"
        }}
        ]
    """
    with st.spinner("Extracting places from the itinerary..."):
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured place information from text."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0
        )
    return response.choices[0].message.content

def extract_location(itinerary):
    # Regex pattern to match text between 'Location:' and the next newline
    pattern = r'Location:\s+([A-Za-z\s,]+)\n'
    match = re.search(pattern, itinerary)
    return match.group(1).strip() if match else None