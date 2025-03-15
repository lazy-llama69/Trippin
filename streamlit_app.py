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

# Custom CSS for aligning navigation buttons to the right & styling the "Get Started" button
st.markdown(
    """
    <style>
        /* Styling for the Trippin button text */
        # div[data-testid="stButton"] > button {
        #     font-size: 24px !important;  /* Larger font */
        #     font-weight: bold !important;
        #     color: #FF7F9F !important;  /* Pink text */
        #     background: none !important;
        #     border: none !important;
        #     cursor: pointer;
        # }

        # div[data-testid="stButton"] > button:hover {
        #     text-decoration: underline;
        # }

        button[kind="primary"] {
            background-color: #FF7F9F;
            border: none;
        }

        button[kind="primary"]:hover {
            background-color: #ff5c8a;  
            cursor: pointer;  
        }

        button[kind="secondary"] {
            background-color: none;
            border: none;
            color: #FF7F9F
        }

        button[kind="secondary"]:hover {
            color: white;  
            background-color: #FF7F9F;  
            cursor: pointer;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Navigation Bar (properly aligned to the right)
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6= st.columns([8, 1, 1.4, 1.9, 1.5, 1])  # Push buttons to the right

st.markdown(
    """
    <style>
        /* Hide the enlarge icon beside images */
        .css-1lcbm11 {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
with col1:
    st.image("assets/trippin_logo.png", width=220)
with col2:
    if st.button("Home", key="home_tab",type="secondary"):
        switch_tab("Home")
with col3:
    if st.button("Plan My Trip", key="trip_tab"):
        switch_tab("Plan My Trip")
with col4:
    if st.button("Currency Converter", key="convert_tab"):
        switch_tab("Convert")
with col5:
    if st.button("Glow Up", key="glowup_tab"):
        switch_tab("Glow Up")
with col6:
    if st.button("Chat", key="chat_tab"):
        switch_tab("Chat")
st.markdown('</div>', unsafe_allow_html=True)

# Render content based on the active tab
if st.session_state["active_tab"] == "Home":
    st.markdown(
    """
    <h1 style="text-align: center;">
        Say Goodbye to Travel Hassles, Hello to <span style="color: #FF7F9F;">Trippin AI!</span>
    </h1>
    <p style="text-align: center; font-size:18px;">We create customized itineraries, provide currency conversion, and answer all your travel questions. Need help? Just ask our chatbot!</p>
    """,
    unsafe_allow_html=True
)
    st.write("")

    
    col1, col2, col3 = st.columns([5.2, 2, 5])

    with col2:  # Center column
        if st.button("Get started Now", key="get_started", type="primary"):
            switch_tab("Plan My Trip")  # Redirect to "Plan My Trip" tab

    st.write("")
    st.write("")
    st.markdown("<h2 style='text-align: center;'>🌟 Tourist Recommendations 🌟</h2>", unsafe_allow_html=True)

    trip_col1, trip_col2, trip_col3 = st.columns(3)

    if "selected_trip" not in st.session_state:
        st.session_state.selected_trip = None

    # Recommended Trip 1
    with trip_col1:
        st.image("assets/bali.jpg", use_column_width=True)
        st.markdown("### Bali, Indonesia")
        st.write("Experience breathtaking beaches, lush jungles, and vibrant culture.")
        if st.button("View", key="bali", type="primary"):
            st.session_state.selected_trip = "Bali"

    # Recommended Trip 2
    with trip_col2:
        st.image("assets/paris.webp", use_column_width=True)
        st.markdown("### Paris, France")
        st.write("Visit the City of Love and explore its iconic landmarks and cafes.")
        if st.button("View", key="paris",type="primary"):
            st.session_state.selected_trip = "Paris"

    # Recommended Trip 3
    with trip_col3:
        st.image("assets/tokyo.webp", use_column_width=True)
        st.markdown("### Tokyo, Japan")
        st.write("Discover a mix of futuristic cityscapes and traditional temples.")
        if st.button("View", key="tokyo", type="primary"):
            st.session_state.selected_trip = "Tokyo"

    st.markdown("<hr>", unsafe_allow_html=True)  # Add a separator

    travel_guide = {
        "Bali": {
            "days": "7-10 days",
            "best_season": "Dry season (April - October)",
            "cheapest_month": "February",
            "attractions": [
                "Uluwatu Temple – Stunning cliffside views.",
                "Tegallalang Rice Terraces – Breathtaking landscapes.",
                "Seminyak Beach – Perfect for sunset lovers.",
                "Mount Batur – Sunrise trek for adventure seekers.",
                "Nusa Penida – Spectacular cliffs and beaches."
            ],
            "activities": [
                "Surfing at Kuta Beach.",
                "Snorkeling or diving in Nusa Lembongan.",
                "Balinese cooking class.",
                "Traditional spa and wellness retreat.",
                "Exploring Ubud’s Monkey Forest."
            ],
            "restaurants": [
                "Locavore – Award-winning fine dining.",
                "Naughty Nuri’s – Famous for ribs and cocktails.",
                "Bambu – Authentic Indonesian cuisine.",
                "Sardine – Great seafood with rice paddy views."
            ],
            "festivals": [
                "Nyepi (March) – Balinese New Year, a day of silence.",
                "Galungan & Kuningan – Celebrations of good over evil.",
                "Bali Arts Festival (June - July) – Traditional performances."
            ]
        },
        "Paris": {
            "days": "5-7 days",
            "best_season": "Spring (April - June) & Fall (September - November)",
            "cheapest_month": "January",
            "attractions": [
                "Eiffel Tower – A must-see iconic landmark.",
                "Louvre Museum – Home of the Mona Lisa.",
                "Champs-Élysées – Perfect for shopping and cafes.",
                "Seine River Cruise – Romantic boat tour.",
                "Sacré-Cœur – Stunning views from Montmartre."
            ],
            "activities": [
                "Visit art museums like Musée d'Orsay.",
                "Enjoy a picnic at Jardin du Luxembourg.",
                "Take a day trip to the Palace of Versailles.",
                "Explore Parisian cafés and bakeries.",
                "Watch a cabaret show at Moulin Rouge."
            ],
            "restaurants": [
                "Le Meurice – Michelin-starred luxury dining.",
                "Le Petit Cambodge – Amazing local food.",
                "L’Ambroisie – A 3-star Michelin experience.",
                "Bouillon Pigalle – Affordable and delicious French cuisine."
            ],
            "festivals": [
                "Bastille Day (July 14) – Fireworks & celebrations.",
                "Paris Fashion Week (March & September).",
                "Nuit Blanche (October) – All-night art festival."
            ]
        },
        "Tokyo": {
            "days": "7-10 days",
            "best_season": "Spring (March - May) & Fall (September - November)",
            "cheapest_month": "February",
            "attractions": [
                "Shibuya Crossing – The world’s busiest intersection.",
                "Senso-ji Temple – Tokyo’s most famous temple.",
                "Akihabara – A paradise for anime and gaming lovers.",
                "Shinjuku Gyoen – Beautiful park, great for cherry blossoms.",
                "Tsukiji Outer Market – Fresh sushi experience."
            ],
            "activities": [
                "Explore teamLab Planets Tokyo (digital art museum).",
                "Watch a sumo wrestling match.",
                "Shop for tech and anime merchandise in Akihabara.",
                "Visit a themed café (Pokemon Café, Robot Restaurant, etc.).",
                "Experience a traditional tea ceremony."
            ],
            "restaurants": [
                "Sukiyabashi Jiro – World-famous sushi restaurant.",
                "Ichiran Ramen – Best solo ramen experience.",
                "Gonpachi – Known as 'The Kill Bill' restaurant.",
                "Narisawa – Innovative fine dining experience."
            ],
            "festivals": [
                "Sakura Festivals (March - April) – Cherry blossom season.",
                "Sumidagawa Fireworks Festival (July).",
                "Tokyo Game Show (September) – A must for gamers.",
                "Shichi-Go-San (November) – Celebration for children."
            ]
        }
    }

    if st.session_state.selected_trip:
        st.subheader(f"🌍 {st.session_state.selected_trip} Travel Guide")
        
        st.markdown(f"**🗓️ Ideal Trip Duration:** {travel_guide[st.session_state.selected_trip]['days']}")
        st.markdown(f"**🌤️ Best Season to Visit:** {travel_guide[st.session_state.selected_trip]['best_season']}")
        st.markdown(f"**✈️ Cheapest Month for Flights:** {travel_guide[st.session_state.selected_trip]['cheapest_month']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🏛️ Top Attractions:")
            for attraction in travel_guide[st.session_state.selected_trip]["attractions"]:
                st.write(f"- {attraction}")
            
            st.markdown("### 🎭 Best Activities:")
            for activity in travel_guide[st.session_state.selected_trip]["activities"]:
                st.write(f"- {activity}")

        with col2:
            st.markdown("### 🍽️ Must-Try Restaurants:")
            for restaurant in travel_guide[st.session_state.selected_trip]["restaurants"]:
                st.write(f"- {restaurant}")
            
            st.markdown("### 🎉 Festivals & Events:")
            for festival in travel_guide[st.session_state.selected_trip]["festivals"]:
                st.write(f"- {festival}")

        st.markdown("Safe travels! 🌍✨")
        st.markdown("<hr>", unsafe_allow_html=True)  # Add a separator

    st.markdown("<h2 style='text-align: center;'>💡 Travel FAQs 💡</h2>", unsafe_allow_html=True)

    st.write("Find answers to common travel questions below! Click on any category to expand.")

    # Visa & Passport FAQs
    with st.expander("🛂 Visa & Passport FAQs"):
        st.write("**Q: How do I check if I need a visa for my destination?**")
        st.write("👉 You can check visa requirements on official embassy websites or use [iVisa](https://www.ivisa.com/) for quick reference.")

        st.write("**Q: How long should my passport be valid for travel?**")
        st.write("👉 Many countries require at least **6 months of validity** beyond your departure date.")

        st.write("**Q: Do I need a transit visa if I have a layover?**")
        st.write("👉 Some countries require transit visas if you **leave the airport**, so check with the airline or embassy.")

    # Money & Currency FAQs
    with st.expander("💰 Budget & Currency FAQs"):
        st.write("**Q: Should I exchange money before traveling?**")
        st.write("👉 It’s usually cheaper to **withdraw cash from ATMs** at your destination rather than exchange money at airports.")

        st.write("**Q: What is the best way to avoid foreign transaction fees?**")
        st.write("👉 Use a **no-fee travel credit card** or **withdraw larger amounts from ATMs** to reduce fees.")

    # Flight & Airport FAQs
    with st.expander("✈️ Flight & Airport FAQs"):
        st.write("**Q: When is the best time to book a cheap flight?**")
        st.write("👉 **Tuesdays and Wednesdays** tend to have the cheapest fares, and booking **2-3 months in advance** is ideal.")

        st.write("**Q: What items are restricted in carry-on luggage?**")
        st.write("👉 No liquids over **100ml**, sharp objects, aerosols, or batteries exceeding airline limits.")

    # Accommodation FAQs
    with st.expander("🏨 Accommodation FAQs"):
        st.write("**Q: Should I book hotels in advance or last-minute?**")
        st.write("👉 For peak seasons, book early. Last-minute deals can be cheaper, but availability is risky.")

        st.write("**Q: Are Airbnb rentals better than hotels?**")
        st.write("👉 **Hotels** offer **security & services**, while **Airbnb** provides **local experiences & lower costs** for groups.")

    # Tech & Connectivity FAQs
    with st.expander("📱 Tech & Connectivity FAQs"):
        st.write("**Q: What’s the best way to get internet while traveling?**")
        st.write("👉 Buy a **local SIM card, eSIM, or use portable WiFi**.")

        st.write("**Q: Can I use my phone abroad?**")
        st.write("👉 Check if your carrier offers **international roaming**, or **unlock your phone** for a local SIM.")

    # Health & Safety FAQs
    with st.expander("🚑 Health & Safety FAQs"):
        st.write("**Q: Do I need travel insurance?**")
        st.write("👉 Yes! Travel insurance covers **medical emergencies, cancellations, and lost luggage**.")

        st.write("**Q: Can I drink tap water abroad?**")
        st.write("👉 **Research first!** In some countries, only bottled or filtered water is safe.")

    # Sightseeing & Activities FAQs
    with st.expander("🗺️ Sightseeing & Activities FAQs"):
        st.write("**Q: Should I book tours in advance or on arrival?**")
        st.write("👉 **Popular tours (museums, safaris, adventure activities)** should be booked early to avoid missing out.")

        st.write("**Q: What’s the best way to avoid crowds at attractions?**")
        st.write("👉 **Visit early in the morning** or right before closing time.")

    st.write("🔍 Need more help? Ask our chatbot for personalized travel advice!")  

elif st.session_state["active_tab"] == "Plan My Trip":
    plan_my_trip()

elif st.session_state["active_tab"] == "Chat":
    st.title("Chat with AI")
    st.write("Ask travel-related questions and get instant recommendations.")
    generate_chat_response()

# streamlit_app.py (excerpt)
elif st.session_state["active_tab"] == "Itinerary":
    from itinerary import display_itinerary  # Import the function
    display_itinerary()  # Call it to render the layout

elif st.session_state["active_tab"] == "Convert":
    get_conversion()