import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

def get_coordinates(location):
    """Convert a location name to latitude and longitude coordinates."""
    geolocator = Nominatim(user_agent="trippin_app")
    try:
        location = geolocator.geocode(location)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return None

def display_itinerary():
    # Remove padding and margins from the main container
    st.markdown(
        """
        <style>
            .block-container {
                padding: 0rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Your Custom Itinerary")
    # Create two columns: left for itinerary, right for map
    left_col, right_col = st.columns([2, 1])  # 2:1 ratio

    with left_col:
        st.header("Itinerary Details")
        itinerary_text = st.session_state.get("itinerary", "No itinerary available.")
        st.write(itinerary_text)

    with right_col:
        st.header("Map of Your Destination")
        destination = st.session_state.get("destination", "Unknown")
        coordinates = get_coordinates(destination)
        if coordinates:
            # Create a Folium map centered on the destination
            m = folium.Map(location=coordinates, zoom_start=11)
            # Add a marker for the destination
            folium.Marker(
                location=coordinates,
                popup=destination,
                tooltip=destination
            ).add_to(m)
            # Render the map with full width and increased height
            st_folium(m, width=None, height=600)
        else:
            st.write("Could not find coordinates for the destination.")