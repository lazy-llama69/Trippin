# Add your API key here for local testing (avoid committing this key in production!)
GOOGLE_MAPS_API_KEY = ""

import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
from io import BytesIO

# Optional: Use wide mode to maximize available width
st.set_page_config(layout="wide")

############################
# 1) Define placeholder variables
############################

# Example of user inputs
location_input = "Jakarta"  # e.g. from user: "Location: Jakarta"
travel_date_input = "2025-03-15"  # e.g. from user: "Travel Date: 2025-03-15"
number_of_days_input = 5  # e.g. from user: "Number of Days: 5"
budget_input = "Low (0 - 1000 USD)"  # e.g. from user: "Budget: Low (0 - 1000 USD)"
companions_input = ["Solo", "Couple"]  # e.g. from user: "Companions: [Solo, Couple]"
activities_input = []  # e.g. from user: "Activities: ..."
dietary_options_input = ""  # e.g. from user: "Dietary Options: ..."
additional_requirements_input = ""  # e.g. from user: "Additional Requirements: None"

# Overview & General Info placeholders
trip_title = f"{number_of_days_input} days trip in {location_input}"  
travel_dates = "22 Mar, 2025 - 24 Mar, 2025"
description_content = (
    "Tokyo is the capital city of Japan, famous for its vibrant blend of traditional "
    "and modern culture. It is a bustling metropolis with a population of over 14 million people..."
)
history_content = (
    "Tokyo has a rich history that dates back centuries. It was originally a small fishing village "
    "known as Edo, in 1603..."
)

# Lodging Recommendations placeholders
lodging_recommendations = [
    {
        "name": "MIMARU Tokyo Ikebukuro",
        "rating": "8.7",
        "price_per_night": "$288.75",
        "link": "http://example.com",
    },
    {
        "name": "Hotel JAL City Haneda Tokyo",
        "rating": "8.4",
        "price_per_night": "$144.57",
        "link": "http://example.com",
    },
    {
        "name": "Comfort Hotel ERA Tokyo",
        "rating": "8.7",
        "price_per_night": "$137.32",
        "link": "http://example.com",
    }
    # ... more hotels if needed
]

# Itinerary placeholders (day by day)
itinerary_details = [
    {
        "day": 1,
        "activities": [
            {
                "title": "Find a place to stay",
                "duration": "",
                "location": "",
                "description": "",
            },
            {
                "title": "Tsukiji Outer Market",
                "duration": "120 min",
                "location": "Tokyo",
                "description": "A bustling market offering fresh seafood, local produce, and souvenirs.",
            },
            {
                "title": "Tokyo Skytree",
                "duration": "120 min",
                "location": "Tokyo",
                "description": "Tokyo Skytree is the tallest structure in Japan, offering panoramic views of the city.",
            },
            {
                "title": "Dinner in Asakusa (Monjayaki)",
                "duration": "60 min",
                "location": "Tokyo",
                "description": "Witness the ancient Japanese sport of Sumo wrestling at the Ryogoku Kokugikan, a historic arena.",
            },
            {
                "title": "Evening stroll along Sumida River",
                "duration": "60 min",
                "location": "Tokyo",
                "description": "A scenic route along the Sumida River, offering views of Tokyo’s iconic landmarks.",
            },
        ],
    },
    # You can add more days with similar structure
]

# Estimated Cost placeholders
# This can be structured in many ways; here is just one example
estimated_costs = {
    "Accommodation": {
        "Hostel": 20,
        "Budget Hotel": 70,
        "Mid-Range Hotel": 150,
        "Airbnb (Private Room)": 80,
        "Capsule Hotel": 40,
    },
    "Transportation": {
        "Suica/Pasmo Card (Rechargeable Transit Card)": "10/day",
        "JR Pass (For Longer Trips Outside Tokyo)": 250,
        "Taxi": "15/ride",
        "Local Trains/Subways": 2,
        "Walking/Cycling": 0,
    },
    "Food": {
        "Street Food": "5-15",
        "Ramen Shops": "10-20",
        "Izakaya (Japanese Pubs)": "20-40",
        "Upscale Restaurants": "50+",
        "Convenience Stores (7-Eleven, FamilyMart)": "2-10",
    },
    "Activities": {
        "Ghibli Museum (Requires Advance Booking)": 10,
        "Tokyo National Museum": 5,
        "Hiking Mt. Takao": 0,
        "Shibuya Crossing Observation": 0,
        "Sensō-ji Temple Visit": 0,
    },
}

############################
# 2) Utility functions
############################

def get_coordinates(location):
    """Convert a location name to latitude and longitude coordinates."""
    geolocator = Nominatim(user_agent="trippin_app")
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return None

def convert_markdown_to_html(text):
    """Convert markdown-style text (e.g., **bold**, ### header) to HTML-like formatting."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'###(.*?)\n', r'<h3>\1</h3>\n', text)
    text = re.sub(r'##(.*?)\n', r'<h2>\1</h2>\n', text)
    text = re.sub(r'#(.*?)\n', r'<h1>\1</h1>\n', text)
    return text

def generate_pdf(itinerary_content):
    """Generate a PDF from the itinerary content."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_normal.fontName = 'Helvetica'
    style_normal.fontSize = 12
    style_normal.leading = 14

    itinerary_paragraph = Paragraph(itinerary_content.replace("\n", "<br />"), style_normal)
    doc.build([itinerary_paragraph])
    
    buffer.seek(0)
    return buffer

def build_itinerary_markdown():
    """
    Build a markdown string that includes all the placeholders:
    - Trip title, dates, overview, history
    - Lodging recommendations
    - Day-by-day itinerary
    - Estimated costs
    """
    md = []
    
    # Overview
    md.append(f"## Overview")
    md.append(f"**Trip Title:** {trip_title}")
    md.append(f"**Dates:** {travel_dates}")
    md.append(description_content)
    
    # General Information
    md.append(f"## General Information")
    md.append(history_content)
    
    # Lodging Recommendations
    md.append("## Lodging Recommendation")
    md.append("Below are some hotels based on your interests:")
    for hotel in lodging_recommendations:
        md.append(f"- **{hotel['name']}** (Rating: {hotel['rating']}, Price: {hotel['price_per_night']}/night) [Link]({hotel['link']})")
    
    # Itinerary
    md.append("## Itinerary")
    for day_info in itinerary_details:
        day_num = day_info["day"]
        md.append(f"### Day {day_num}")
        for act in day_info["activities"]:
            md.append(
                f"- **{act['title']}** \n"
                f"  - Duration: {act['duration']} \n"
                f"  - Location: {act['location']} \n"
                f"  - Description: {act['description']}"
            )
    
    # Estimated Cost
    md.append("## Estimated Cost (USD)")
    for category, items in estimated_costs.items():
        md.append(f"### {category}")
        if isinstance(items, dict):
            for k, v in items.items():
                md.append(f"- **{k}:** {v}")
        else:
            md.append(f"- {items}")
    
    # Combine everything
    return "\n\n".join(md)

############################
# 3) Main display function
############################

def display_itinerary():
    # Create a two-column layout
    col1, col2 = st.columns([3, 7])  # 30% for details, 70% for map
    
    # Apply CSS to make the layout more robust
    st.markdown(
        """
        <style>
        /* Make columns take full height */
        [data-testid="column"] {
            height: calc(100vh - 80px); /* Adjust if needed */
            overflow: auto;
        }
        
        /* Left column scrollable */
        [data-testid="column"]:first-child {
            overflow-y: auto;
            background-color: #f9f9f9;
            padding: 10px;
            border-right: 1px solid #e0e0e0;
            box-shadow: 2px 0 5px rgba(0,0,0,0.05);
        }
        
        /* Map container shouldn't scroll */
        [data-testid="column"]:nth-child(2) {
            overflow: hidden;
        }
        
        /* Full-width container */
        .block-container {
            max-width: 100% !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* Hide default streamlit footer */
        footer {display: none !important;}
        
        /* Make sure map takes full height */
        .folium-map {
            height: calc(100vh - 130px) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # LEFT COLUMN: Itinerary details
    with col1:
        st.markdown("<h2 style='text-align: center;'>Itinerary Details</h2>", unsafe_allow_html=True)
        
        # Build the itinerary markdown from placeholders
        itinerary_markdown = build_itinerary_markdown()
        st.markdown(itinerary_markdown)
        
        # Generate and offer PDF download
        formatted_itinerary = convert_markdown_to_html(itinerary_markdown)
        pdf = generate_pdf(formatted_itinerary)
        st.download_button(
            "Download Itinerary as PDF",
            data=pdf,
            file_name="itinerary.pdf",
            mime="application/pdf",
            type="primary"
        )

    # RIGHT COLUMN: Map
    with col2:
        st.markdown("<h2 style='text-align: center;'>Map of Your Destination</h2>", unsafe_allow_html=True)
        
        # Use the placeholder user input location for the map
        destination = location_input  # e.g. "Jakarta"
        coordinates = get_coordinates(destination)
        if coordinates:
            lat, lng = coordinates
            google_maps_url = (
                f"https://www.google.com/maps/embed/v1/view?"
                f"key={GOOGLE_MAPS_API_KEY}&center={lat},{lng}&zoom=12"
            )
            st.markdown(f"""
                <iframe
                width="100%"
                height="700"
                frameborder="0" style="border:0"
                src="{google_maps_url}" allowfullscreen>
                </iframe>
            """, unsafe_allow_html=True)
        else:
            st.write("Could not find coordinates for the destination.")



############################
# 4) Run the app
############################

if __name__ == "__main__":
    display_itinerary()
