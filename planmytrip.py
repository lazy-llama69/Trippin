import streamlit as st

def plan_my_trip():
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
            st.success("Your preferences have been saved! We will generate your itinerary shortly.")
