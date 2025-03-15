import requests
import os

def get_place_details(place_name):
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=name,price_level&key={api_key}"
    
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get('candidates', [])
        if results:
            place_info = results[0]
            return {
                "name": place_info.get("name"),
                "price_level": place_info.get("price_level")
            }
    return None

def get_price_estimations(places):
    price_estimations = {}
    for place in places:
        details = get_place_details(place)
        if details:
            price_estimations[place] = details['price_level']
        else:
            price_estimations[place] = "Not available"
    return price_estimations