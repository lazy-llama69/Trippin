import requests
import os
import streamlit as st

def get_place_details(place_name):
    api_key = st.secrets["google"]["places_api_key"]
    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=place_id&key={api_key}"
    
    response = requests.get(search_url)
    print("Search Response:", response.json())  # Log the search response for debugging

    if response.status_code == 200:
        results = response.json().get('candidates', [])
        if results:
            place_id = results[0].get("place_id")
            details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_address,international_phone_number,website,opening_hours,rating,user_ratings_total,price_level,geometry,photos,types,place_id,reviews&key={api_key}"
            details_response = requests.get(details_url)
            print("Details Response:", details_response.json())  # Log the details response for debugging
            if details_response.status_code == 200:
                place_info = details_response.json().get('result', {})
                photo_reference = place_info.get("photos", [{}])[0].get("photo_reference")
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}" if photo_reference else None
                return {
                    "name": place_info.get("name"),
                    "address": place_info.get("formatted_address"),
                    "phone_number": place_info.get("international_phone_number"),
                    "website": place_info.get("website"),
                    "opening_hours": place_info.get("opening_hours", {}).get("weekday_text"),
                    "rating": place_info.get("rating"),
                    "user_ratings_total": place_info.get("user_ratings_total"),
                    "price_level": place_info.get("price_level"),
                    "geometry": place_info.get("geometry"),
                    "photo_url": photo_url,
                    "types": place_info.get("types"),
                    "place_id": place_info.get("place_id"),
                    "top_review": place_info.get("reviews", [{}])[0].get("text")
                }
    return None

def get_price_estimations(places):
    price_estimations = {}
    if places:
        place = places[0]  # Only use the first place
        details = get_place_details(place)
        print("Place Details:", details)  # Log the place details for debugging
        if details:
            price_estimations[place] = {
                "name": details.get("name", "Not available"),
                "address": details.get("address", "Not available"),
                "phone_number": details.get("phone_number", "Not available"),
                "website": details.get("website", "Not available"),
                "opening_hours": details.get("opening_hours", "Not available"),
                "rating": details.get("rating", "Not available"),
                "user_ratings_total": details.get("user_ratings_total", "Not available"),
                "price_level": details.get("price_level", "Not available"),
                "geometry": details.get("geometry", "Not available"),
                "photo_url": details.get("photo_url", "Not available"),
                "types": details.get("types", []),  # Ensure types is a list
                "place_id": details.get("place_id", "Not available"),
                "top_review": details.get("top_review", "Not available")
            }
        else:
            price_estimations[place] = {
                "name": "Not available",
                "address": "Not available",
                "phone_number": "Not available",
                "website": "Not available",
                "opening_hours": "Not available",
                "rating": "Not available",
                "user_ratings_total": "Not available",
                "price_level": "Not available",
                "geometry": "Not available",
                "photo_url": "Not available",
                "types": [],
                "place_id": "Not available",
                "top_review": "Not available"
            }
    return price_estimations