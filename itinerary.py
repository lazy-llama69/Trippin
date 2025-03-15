# Add your API key here for local testing (avoid committing this key in production!)
GOOGLE_MAPS_API_KEY = "AIzaSyDO-7AwP9kpPhLvXo848g7PKFgYPQXSkkA"

import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
from io import BytesIO
import streamlit.components.v1 as components


############################
# Utility functions
############################

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

def display_custom_map(places, api_key, center_lat=35.6895, center_lng=139.6917, zoom=12):
    """
    places: list of dict, each with 'title', 'lat', 'lng', and optionally 'description' and 'image_url'
    api_key: your Google Maps JavaScript API key
    center_lat, center_lng: map center
    zoom: initial zoom level
    """

    # Build JS for creating each marker
    markers_js = ""
    for p in places:
        # Escape quotes in description to avoid JS errors
        desc = p.get('description', '').replace('"', '\\"')
        img_url = p.get('image_url', '')
        title = p.get('title', '').replace('"', '\\"')

        markers_js += f"""
            var marker = new google.maps.Marker({{
                position: {{ lat: {p['lat']}, lng: {p['lng']} }},
                map: map,
                title: "{title}"
            }});

            var infowindow = new google.maps.InfoWindow({{
                content: `
                    <div style="min-width:200px">
                        <h4>{title}</h4>
                        {"<img src='" + img_url + "' style='max-width:200px;' />" if img_url else ""}
                        <p>{desc}</p>
                    </div>
                `
            }});

            marker.addListener('click', function() {{
                // Center and zoom on the marker
                map.setCenter(marker.getPosition());
                map.setZoom(15);
                infowindow.open(map, marker);
            }});
        """

    # Build the full HTML/JS
    html_code = f"""
    <html>
    <head>
      <style>
        #map {{
          height: 700px;
          width: 100%;
        }}
      </style>
    </head>
    <body>
      <div id="map"></div>
      <script>
        function initMap() {{
          var center = {{ lat: {center_lat}, lng: {center_lng} }};
          var map = new google.maps.Map(document.getElementById('map'), {{
            zoom: {zoom},
            center: center
          }});

          {markers_js}
        }}
      </script>
      <script async
        src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap">
      </script>
    </body>
    </html>
    """

    # Embed the custom map HTML in Streamlit
    components.html(html_code, height=700)

############################
# Main display function
############################

def display_itinerary():
    # Create a two-column layout: left for itinerary details, right for map
    col1, col2 = st.columns([3, 7])
    
    # Apply global CSS for a modern, clean look
    st.markdown(
    """
    <style>
    /* Global font and background */
    body {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", 
                      Roboto, Helvetica, Arial, sans-serif;
        background-color: #f5f5f7;
        color: #333;
    }

    /* Remove default Streamlit footer */
    footer { 
        display: none !important; 
    }

    /* Full-width container */
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 auto;
    }

    /* Make columns take full height */
    [data-testid="column"] {
        height: calc(100vh - 80px);
        overflow: auto;
    }

    /* Left column with card-like background */
    [data-testid="column"]:first-child {
        overflow-y: auto;
        background-color: #ffffff;
        padding: 2rem;
        border-right: 1px solid #e0e0e0;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }

    /* Right column for map */
    [data-testid="column"]:nth-child(2) {
        overflow: hidden;
        background-color: #f5f5f7;
        padding: 2rem;
    }

    /* Headings styling */
    h2 {
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        text-align: left;
        color: #222;
    }

    h1, h2, h3, h4 {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", 
                      Roboto, Helvetica, Arial, sans-serif;
    }

    /* Styling lists */
    ul, ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }

    li {
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }

    /* PDF Download button styling */
    .stDownloadButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        border: none;
        font-weight: 600;
        cursor: pointer;
    }
    .stDownloadButton > button:hover {
        background-color: #45a049;
    }

    /* Map container styling */
    #map {
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # LEFT COLUMN: Display AI-generated itinerary from session state
    with col1:
        st.markdown("<h2 style='text-align: center;'>Itinerary Details</h2>", unsafe_allow_html=True)
        
        if "itinerary" in st.session_state:
            real_itinerary = st.session_state["itinerary"]
            st.markdown(real_itinerary)
            
            # Optional: Allow PDF download of the itinerary
            pdf_ai = generate_pdf(real_itinerary)
            st.download_button(
                "Download AI Itinerary as PDF",
                data=pdf_ai,
                file_name="AI_itinerary.pdf",
                mime="application/pdf",
                type="primary"
            )
        else:
            st.markdown("No AI-generated itinerary found. Please generate one first.")

    # RIGHT COLUMN: Display map of the destination
    with col2:
        st.markdown("<h2 style='text-align: center;'>Map of Your Destination</h2>", unsafe_allow_html=True)
        
        # For demonstration purposes, we use a sample places list.
        # In a full implementation, you could extract place details from the AI itinerary.
        sample_places = [
            {
                "title": "Tsukiji Outer Market",
                "lat": 35.665498,
                "lng": 139.770642,
                "description": "A bustling market offering fresh seafood, local produce, and souvenirs.",
                "image_url": "https://example.com/tsukiji.jpg"
            },
            {
                "title": "Tokyo Skytree",
                "lat": 35.7100627,
                "lng": 139.8107004,
                "description": "Tokyo Skytree is the tallest structure in Japan, offering panoramic views.",
                "image_url": "https://example.com/skytree.jpg"
            }
        ]
        
        # Center the map (example uses Tokyo coordinates)
        display_custom_map(
            places=sample_places,
            api_key=GOOGLE_MAPS_API_KEY,
            center_lat=35.6895,
            center_lng=139.6917,
            zoom=12
        )

# Note: Do not call display_itinerary() here.
# It will be imported and called from streamlit_app.py based on the active tab.