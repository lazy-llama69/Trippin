import requests
import os

def get_place_id(place_name):
    # Get the API key from environment variables
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_PLACES_API_KEY environment variable.")
    
    # Construct the autocomplete URL for the place
    autocomplete_url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={place_name}&key={api_key}"
    
    # Make the API request
    response = requests.get(autocomplete_url)
    if response.status_code == 200:
        predictions = response.json().get('predictions', [])
        if predictions:
            place_id = predictions[0].get("place_id")
            return place_id
        else:
            return None
    else:
        raise Exception(f"Error fetching place ID for {place_name}, Status code: {response.status_code}")

def get_place_details(place_id):
    # Get the API key from environment variables
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_PLACES_API_KEY environment variable.")
    
    # Construct the details URL for the place
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    
    # Make the API request
    response = requests.get(details_url)
    if response.status_code == 200:
        result = response.json().get('result', {})
        price_level = result.get("price_level", "Price level not available")
        rating = result.get("rating", "Rating not available")
        return price_level, rating
    else:
        raise Exception(f"Error fetching details for place ID {place_id}, Status code: {response.status_code}")

def get_price_estimations(places):
    price_estimations = {}
    for place in places:
        place_id = get_place_id(place)
        if place_id:
            price_level, rating = get_place_details(place_id)
            price_estimations[place] = {
                "price_level": price_level,
                "rating": rating
            }
        else:
            price_estimations[place] = {
                "price_level": "Not available",
                "rating": "Not available"
            }
    return price_estimations