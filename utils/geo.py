# utils/geo.py
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def find_nearest_store(user_lat, user_lon, stores):
    """Find the nearest McDonald's store"""
    if not stores or user_lat is None or user_lon is None:
        return None, None
    
    min_dist = float("inf")
    nearest = None

    for store in stores:
        store_lat = store["coordinates"]["latitude"]
        store_lon = store["coordinates"]["longitude"]
        dist = geodesic((user_lat, user_lon), (store_lat, store_lon)).meters

        if dist < min_dist:
            min_dist = dist
            nearest = store

    return nearest, int(min_dist)

def geocode_location(address):
    """Convert address to coordinates"""
    geolocator = Nominatim(user_agent="mcdonalds_assistant")
    
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            # Fallback for common cities
            address_lower = address.lower()
            if "delhi" in address_lower:
                return 28.6139, 77.2090
            elif "mumbai" in address_lower:
                return 19.0760, 72.8777
            elif "bangalore" in address_lower:
                return 12.9716, 77.5946
            else:
                return 28.6139, 77.2090  # Default to Delhi
    except:
        return 28.6139, 77.2090  # Default on error