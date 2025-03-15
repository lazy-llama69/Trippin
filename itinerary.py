import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
from io import BytesIO

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
    # Add a back button
    if st.button("Back"):
        st.session_state["active_tab"] = "Plan My Trip"
        st.rerun()
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
    left_col, right_col = st.columns([1, 1])  # 2:1 ratio
    

    def convert_markdown_to_html(text):
        """
        Convert markdown-style text (e.g., **bold**, ### header) to HTML-like formatting
        """
        # Convert **bold** to <b>bold</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Convert ### to <h3> header
        text = re.sub(r'###(.*?)\n', r'<h3>\1</h3>\n', text)
        
        # Convert ## to <h2> header
        text = re.sub(r'##(.*?)\n', r'<h2>\1</h2>\n', text)
        
        # Convert # to <h1> header
        text = re.sub(r'#(.*?)\n', r'<h1>\1</h1>\n', text)
        
        return text

    def generate_pdf(itinerary_content):
        buffer = BytesIO()
        # Set up the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        style_normal = styles['Normal']
        style_normal.fontName = 'Helvetica'
        style_normal.fontSize = 12
        style_normal.leading = 14 

        # Create a Paragraph with the itinerary content
        # Replace newlines with HTML-like line breaks
        itinerary_paragraph = Paragraph(itinerary_content.replace("\n", "<br />"), style_normal)

        # Build the PDF
        doc.build([itinerary_paragraph])

        canvas = doc.canv

        # Add custom text at the bottom of the page
        canvas.setFont("Helvetica-Oblique", 10)
        canvas.drawString(40, 40, "Generated by Trippin")  # Text at the bottom-left of the page

        buffer.seek(0)
        return buffer

    with left_col:
        st.header("Itinerary Details")
        itinerary_text = st.session_state.get("itinerary", "No itinerary available.")
        st.write(itinerary_text)
        formatted_itinerary = convert_markdown_to_html(itinerary_text)
        pdf = generate_pdf(formatted_itinerary)
        st.download_button("Download Itinerary as PDF", data=pdf, file_name="itinerary.pdf", mime="application/pdf")
        # Add the ratings section
        st.markdown("### Ratings")
        map_locations = st.session_state.get("map_locations", {})
        for place, details in map_locations.items():
            if details:
                st.write(f"**{place}**")
                st.write(f"Types: {', '.join(details.get('types', [])) if details.get('types') else 'Not available'}")
                st.write(f"Rating: {details.get('rating', 'Not available')}")
                st.write(f"Price Level: {details.get('price_level', 'Not available')}")
                st.write(f"Opening Hours: {details.get('opening_hours', 'Not available')}")
                st.write(f"Website: {details.get('website', 'Not available')}")
                st.write(f"Top Review: {details.get('top_review', 'Not available')}")
                st.write("---")
                st.write(f"**{place}**")
                st.write(f"Types: {', '.join(details.get('types', [])) if details.get('types') else 'Not available'}")
                st.write(f"Rating: {details.get('rating', 'Not available')}")
                st.write(f"Price Level: {details.get('price_level', 'Not available')}")
                st.write(f"Opening Hours: {details.get('opening_hours', 'Not available')}")
                st.write(f"Website: {details.get('website', 'Not available')}")
                st.write(f"Top Review: {details.get('top_review', 'Not available')}")
                st.write("---")
            else:
                st.write(f"{place}: Rating - Not available, Price Level - Not available")

        
        st.write("")
        st.download_button("Download Itinerary as PDF", data=pdf, file_name="itinerary.pdf", mime="application/pdf",type="primary")

        if st.button("Back", type="primary"):
            st.session_state["active_tab"] = "Plan My Trip"
            st.rerun()

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