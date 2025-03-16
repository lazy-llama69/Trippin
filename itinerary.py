import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import re
from io import BytesIO
import streamlit.components.v1 as components
import json
import requests
import os

GOOGLE_MAPS_API_KEY = st.secrets["google"]["maps_api_key"]

def convert_markdown_to_html(text):
    """
    Convert markdown-style text to ReportLab-compatible HTML-like formatting.
    """
    text = re.sub(r'# (.*?)\n', r'<font size="18"><b>\1</b></font><br />\n', text)
    text = re.sub(r'## (.*?)\n', r'<font size="16"><b>\1</b></font><br />\n', text)
    text = re.sub(r'### (.*?)\n', r'<font size="14"><b>\1</b></font><br />\n', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = text.replace('\n', '<br />\n')
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

    itinerary_paragraph = Paragraph(itinerary_content, style_normal)
    doc.build([itinerary_paragraph])
    buffer.seek(0)
    return buffer

def get_coordinates(location):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK' and data['results']:
            loc = data['results'][0]['geometry']['location']
            return (loc['lat'], loc['lng'])
    return None

def display_custom_map(places, api_key, center_lat=35.6895, center_lng=139.6917, zoom=12):
    """
    places: list of dicts with keys 'title', 'lat', 'lng', and optionally 'description' and 'image_url'
    api_key: your Google Maps JavaScript API key
    center_lat, center_lng: map center coordinates (used if no places)
    zoom: initial zoom level (used if no places)
    """
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
    if places:  # If there are markers, generate JavaScript to fit bounds
        markers_js = """
        var bounds = new google.maps.LatLngBounds();
        """
        for p in places:
            desc = p.get('description', '').replace('"', '\\"')
            img_url = p.get('image_url', '')
            title = p.get('title', '').replace('"', '\\"')
            markers_js += f"""
            var marker = new google.maps.Marker({{
                position: {{ lat: {p['lat']}, lng: {p['lng']} }},
                map: map,
                title: "{title}"
            }});
            bounds.extend(marker.getPosition());
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
                map.setCenter(marker.getPosition());
                map.setZoom(15);
                infowindow.open(map, marker);
            }});
            """
        markers_js += "map.fitBounds(bounds);"
    else:  # No markers, so no additional JavaScript needed
        markers_js = ""

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
      <script async src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap"></script>
    </body>
    </html>
    """
    components.html(html_code, height=700)

def display_itinerary():
    # col1, col2 = st.columns([3, 7])


    st.markdown(
        """
        <style>
        body {
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
                          Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f5f7;
            color: #333;
        }
        # footer { display: none !important; }

        [data-testid="column"] {
            height: calc(100vh - 80px);
            overflow: auto;
        }
        [data-testid="column"]:first-child {
            overflow-y: auto;
            background-color: #ffffff;
            padding: 2rem;
            border-right: 1px solid #e0e0e0;
            box-shadow: 2px 0 5px rgba(0,0,0,0.05);
        }
        [data-testid="column"]:nth-child(2) {
            overflow: hidden;
            background-color: #f5f5f7;
            padding: 2rem;
        }
        h2 {
            font-weight: 600;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
            text-align: left;
            color: #222;
        }

        .block-container {
             padding-top: 1rem !important; /* Adjust the top padding */
             padding-left: 6rem;
             padding-right: 6rem;
        }

        #map {
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h1 style='text-align: center;'>Here's Your Personalised Itinerary</h1>", unsafe_allow_html=True)
    left_margin, col1, col2, right_margin = st.columns([0.1, 1.6, 1.4, 0.1])
    # Left Column: Itinerary Details
    with col1:
        st.markdown("<h2 style='text-align: center;'>Itinerary Details</h2>", unsafe_allow_html=True)
        if "itinerary" in st.session_state:
            real_itinerary = st.session_state["itinerary"]
            st.markdown(real_itinerary)
            formatted_itinerary = convert_markdown_to_html(real_itinerary)
            pdf_ai = generate_pdf(formatted_itinerary)
            st.download_button(
                "Download AI Itinerary as PDF",
                data=pdf_ai,
                file_name="AI_itinerary.pdf",
                mime="application/pdf",
                type="primary"
            )
            if st.button("Back", type="primary"):
                st.session_state["active_tab"] = "Plan My Trip"
                st.rerun()
        else:
            st.markdown("No AI-generated itinerary found. Please generate one first.")

    # Right Column: Map Display
    with col2:
        st.markdown("<h2 style='text-align: center;'>Map of Your Destination</h2>", unsafe_allow_html=True)
        addresses = []
        if "addresses_data" in st.session_state:
            raw_addresses = st.session_state["addresses_data"]
            # Debug expander commented out
            # with st.expander("Debug: Raw Addresses Data"):
            #   st.write(raw_addresses)
            # st.write(f'addresses{raw_addresses}')
            start = raw_addresses.find('[')
            end = raw_addresses.rfind(']') + 1
            json_str = raw_addresses[start:end] if start != -1 and end != -1 else "[]"
            try:
                addresses = json.loads(json_str)
                markers = []
                destination = st.session_state["destination"].strip().lower()
                if ',' in destination:
                    destination_parts = [part.strip().lower() for part in destination.split(',')]
                else:
                    destination_parts = [destination]
                for place in addresses:
                    if not isinstance(place, dict):
                        continue
                    # Check if all parts of the destination are in the address
                    if all(part in place.get('address', '').lower() for part in destination_parts):
                        query = place.get('address') or place.get('name')
                        if not query:
                            continue
                        coords = get_coordinates(query)
                        if coords:
                            markers.append({
                                "title": place.get('name', query),
                                "lat": coords[0],
                                "lng": coords[1],
                                "description": place.get('shortDescription', '')
                            })
                        else:
                            pass

                if markers:
                    display_custom_map(markers, GOOGLE_MAPS_API_KEY)
                    return
                else:
                    st.write("Sorry we could not place markers :(")
                    destination = st.session_state.get("destination", "Tokyo")
                    coords = get_coordinates(destination)
                    if coords:
                        st.write(f"Showing map centered on {destination}.")
                        display_custom_map(
                            places=[],
                            api_key=GOOGLE_MAPS_API_KEY,
                            center_lat=coords[0],
                            center_lng=coords[1],
                            zoom=12
                        )

            except json.JSONDecodeError as e:
                addresses = []
            
        if not addresses:
            st.write("Sorry we could not extract structured address from itinerary :(")
            destination = st.session_state.get("destination", "Tokyo")
            coords = get_coordinates(destination)
            if coords:
                st.write(f"Showing map centered on {destination}.")
                display_custom_map(
                    places=[],
                    api_key=GOOGLE_MAPS_API_KEY,
                    center_lat=coords[0],
                    center_lng=coords[1],
                    zoom=12
                )
            else:
                st.write("Unable to geocode destination. Displaying default map.")
                sample_places = [
                    {"title": "Tsukiji Outer Market", "lat": 35.665498, "lng": 139.770642, "description": "A bustling market offering fresh seafood."},
                    {"title": "Tokyo Skytree", "lat": 35.7100627, "lng": 139.8107004, "description": "Tallest structure in Japan with panoramic views."}
                ]
                display_custom_map(
                    places=sample_places,
                    api_key=GOOGLE_MAPS_API_KEY,
                    center_lat=35.6895,
                    center_lng=139.6917,
                    zoom=12
                )