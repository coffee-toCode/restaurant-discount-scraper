import os
import time
import pandas as pd
from pandas import json_normalize, concat
import requests
import json
from bs4 import BeautifulSoup
import csv
import googlemaps
import geocoder



# Load the environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()





API_KEY = os.getenv("PLACES_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)
response_list = []
website_urls = []
instagram_links = []






# Generate the location variable from the user's device IP address.
# This is used to get the location of the user's device.
g = geocoder.ip('me')
if g.ok:
    lat, lng = g.latlng
    location = f"{lat},{lng}"







def retrieve_google_place(API_KEY, coordinate=location, radius=5000):    
    """Gather fields from the google place API

    :param api_key: client's API key obtained from google cloud console, will look for local environment variable first
    :type api_key: string

    :param coordinate: latitude and longtitude separated by comma
    :type coordinate: string

    :param radius: define the distance in meters within which to return place results
    :type radius: integer

    :rtype: dataframe with a list of places around the coordinate input and the radius defined and extracted fields
            'name', 'place_id', 'rating', 'types', 'user_ratings_total', 'geometry.location.lat',
            'geometry.location.lng'
    """
    search_endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    parameters = {
        "key": API_KEY,
        "location": coordinate,
        "radius": radius,
        "type": 'restaurant',
        'website': 'website'
    }

    response = requests.get(search_endpoint, params=parameters)
    results = json.loads(response.content)
    response_list.extend(results['results'])
    time.sleep(2)
    while "next_page_token" in results:
        parameters['pagetoken'] = results['next_page_token'],
        res = requests.get(search_endpoint, params=parameters)
        results = json.loads(res.content)
        response_list.extend(results['results'])
        time.sleep(2)
    return response_list

#pass response_list into a csv file for later use.
def generate_csv(response_list):
    with open('response_list.csv', mode='w', newline='') as csv_file:
        fieldnames = ['name', 'place_id', 'rating', 'types', 'user_ratings_total', 'geometry.location.lat', 'geometry.location.lng']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for place in response_list:
            writer.writerow({
                'name': place.get('name'),
                'place_id': place.get('place_id'),
                'rating': place.get('rating'),
                'types': ', '.join(place.get('types', [])),
                'user_ratings_total': place.get('user_ratings_total'),
                'geometry.location.lat': place.get('geometry', {}).get('location', {}).get('lat'),
                'geometry.location.lng': place.get('geometry', {}).get('location', {}).get('lng')
            })

#pass response_list to create a dataframe
def create_response_df(response_list):
    wanted_columns = ['name', 'place_id', 'rating', 'geometry.location.lat', 'geometry.location.lng']

    new_response_list = [json_normalize(i, errors='ignore')[wanted_columns] for i in response_list]
    df = concat(new_response_list)
    df.to_csv('my_data_frame.csv', index=False)
    return df

def get_website_urls(location):
    # Use the Google Places API to search for nearby restaurants based on device location
    restaurants = gmaps.places_nearby(location=location, radius=5000, type='restaurant')

    # Iterate through the list of restaurants and retrieve their website URLs using getDetails
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


def scrape_instagram_links(website_urls):
    # must search each page and scrape instagram tag fro that url
    instagram_links = []
    for url in website_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        instagram_tag = soup.find('a', href=lambda href: href and 'instagram.com' in href)
        if instagram_tag:
            instagram_link = instagram_tag['href']
            instagram_links.append(instagram_link)
    print(f"instagram Links: {instagram_links}")
    return instagram_links




if __name__ == "__main__":
    retrieve_google_place(API_KEY)
    generate_csv(response_list)
    create_response_df(response_list)
    get_website_urls(location)
    scrape_instagram_links(website_urls)