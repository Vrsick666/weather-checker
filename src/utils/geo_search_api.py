from geopy.geocoders import Nominatim


# Function to get locations cords from name
def get_coordinates(location: str) -> tuple:
    geolocator = Nominatim(user_agent='Chrome/51.0.2704.103')
    location = geolocator.geocode(location)
    if location is None:
        raise ValueError("Location not found.")
    return location.latitude, location.longitude


# Example of usage:
#     location = "Red Square, Moscow, Russia"
#     latitude, longitude = get_coordinates(location)
#     print(f"Latitude: {latitude}, Longitude: {longitude}")