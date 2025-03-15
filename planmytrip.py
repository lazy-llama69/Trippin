import streamlit as st
import openai
from dotenv import load_dotenv
import os
import re
# from google_places import get_price_estimations
from streamlit_extras.switch_page_button import switch_page

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        num_days = st.number_input("How many days are you planning to travel?", min_value=1, max_value=60, value=7, key="num_days_input")
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

        submit = st.button("Submit", key="submit_preferences", help="Generate your custom itinerary")

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
                        
                        Please follow the format below:
                        
                        1. **Travel Name**: Generate a catchy, funny, and engaging name for the trip, like "Journey to {destination}, make it ".
                        2. For each day of the itinerary, use **headers** with the day number and a short description.
                        3. For each day's activities, DO NOT use **bullet points**.
                        4. Make **important keywords bold**: 
                            - **Restaurants**, e.g., **The Eiffel Tower Restaurant**
                            - **Tourist Attractions**, e.g., **Louvre Museum**
                            - **Landmarks**, e.g., **Notre-Dame Cathedral**
                        5. Keep the tone fun, engaging, and descriptive.
                        6. Be detailed and have an estimated time for each activity 
                        7. Include the preferences separated by new line below the travel name.
                        8. Be specific with the names of the places to dine and the tourist attractions.
                        9. Ensure the itinerary accomadates the additional requirements strictly 
                        10. Make the travel name font size big so it stands out
                        11. If location is empty, please put a specific place to go. 
                        12. If additional requirements is empty, keep additonal requirements none, do not generate a prompt for additional requirements
                        13. Have a total time next to each of the short description for each day
                        14. Try to make it a full day experience from 8:00 till 22:00 unless stated otherwise in additional requirements
                        15. Use this | symbol to separate the time and the activity for each day
                        16. After the final day in the itinerary, include additional suggestions that would be useful and beneficial for the tourist during the trip regarding (public transport, culture rules, etc.)
                        17. Ensure that each activity is in a newline 

                        Example Format:
                        
                        **Travel Name**: "Journey to Paris: A Culinary Adventure"
                        
                        'preferences'

                        #Day 1: Arrival in Paris 
                        10:00-11:00 | Visit the **Eiffel Tower** 
                        11:00-11:30 | Enjoy a meal at **Le Cinq** (Michelin Star restaurant) 
                        11:30-12:00 | Relax at **Tuileries Gardens** 
                        
                        
                        #Day 2: Exploring Marrakech 
                        10:00-12:00 | Visit the iconic **Jardin Majorelle** 
                        12:00-13:30 | Discover the historic **Bahia Palace** 
                        13:30-15:30 | Explore the bustling **Jemaa el-Fnaa** square 
                        15:30-16:30 | Try tasty street food at Food Stalls in **Jemaa el-Fnaa** 
                        
                        #Additional Suggestions:
                        bullet point: Buy Myki card for the Australian public transport
                        bullet point: Take off your shoes when entering people's homes. 
                    """},
                ],
                max_tokens=2000
            )


            itinerary = response.choices[0].message.content
            st.session_state["itinerary"] = itinerary
            st.session_state["destination"] = extract_location(itinerary)  
            st.session_state["active_tab"] = "Itinerary"
            st.rerun()
            # places = extract_places(itinerary)

            # Get price estimations for each place
            # price_estimations = get_price_estimations(places)

            # Display the generated itinerary with price estimations
            # st.markdown("### Your Custom Itinerary")
            # st.write(itinerary)
            # st.markdown("### Price Estimations")
            # st.write(price_estimations)

def extract_location(itinerary):
    # Regex pattern to match text between 'for' and the colon
    pattern = r'Location:\s+([A-Za-z\s,]+)\n'
    
    # Search for the location using regex
    match = re.search(pattern, itinerary)
    
    # If a match is found, return the location
    if match:
        return match.group(1).strip()
    else:
        return None
        
def extract_places(itinerary):
    # Implement a function to extract place names from the itinerary text
    # This is a placeholder implementation and should be replaced with actual logic
    return ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"]
         
