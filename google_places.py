import requests
import os

def get_place_details(place_name):
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=name,formatted_address,international_phone_number,website,opening_hours,rating,user_ratings_total,price_level,geometry,photos,types,place_id,reviews&key={api_key}"
    
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get('candidates', [])
        if results:
            place_info = results[0]  # Only process the first place
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
                "photos": place_info.get("photos"),
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
        if details:
            price_estimations[place] = {
                "name": details.get("name", "Not available"),
                "website": details.get("website", "Not available"),
                "opening_hours": details.get("opening_hours", "Not available"),
                "rating": details.get("rating", "Not available"),
                "photos": details.get("photos", "Not available"),
                "types": details.get("types", "Not available"),
                "top_review": details.get("top_review", "Not available")
            }
        else:
            price_estimations[place] = {
                "name": "Not available",
                "website": "Not available",
                "opening_hours": "Not available",
                "rating": "Not available",
                "photos": "Not available",
                "types": "Not available",
                "top_review": "Not available"
            }
    return price_estimations