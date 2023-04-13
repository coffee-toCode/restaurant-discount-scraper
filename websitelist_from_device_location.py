# Import the necessary libraries for using the Google Places API
import googlemaps
import geocoder
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("PLACES_API_KEY")

# Create a Google Places API client
gmaps = googlemaps.Client(key=API_KEY)

# Generate the LOCATION variable from the user's device IP address.
# This is used to get the location of the user's device.

g = geocoder.ip('me')
if g.ok:
    lat, lng = g.latlng
    location = f"{lat},{lng}"

# Define a function to retrieve website URLs based on device location
def get_website_urls(location):
    # Use the Google Places API to search for nearby restaurants based on device location
    restaurants = gmaps.places_nearby(location=location, radius=5000, type='restaurant')

    # Iterate through the list of restaurants and retrieve their website URLs using getDetails
    website_urls = []
    for restaurant in restaurants['results']:
        # Retrieve the place_id of the restaurant
        place_id = restaurant['place_id']
        
        # Use getDetails to retrieve details of the restaurant, including its website URL
        details = gmaps.place(place_id=place_id, fields=['website'])
        
        # Check if the restaurant has a website URL and append it to the list if available
        if 'website' in details['result']:
            website_urls.append(details['result']['website'])
    
    # Return the list of website URLs
    return website_urls

# Call the function with the device location as the parameter
device_location = (location)  # Replace with actual GPS coordinates of device
website_urls = get_website_urls(device_location)

# Print the retrieved website URLs
print(website_urls)