import os
import json
import requests

def retrieve_google_place_website(api_key=os.getenv("PLACES_API_KEY"), place_id=None):
    """Retrieve the website for the provided place_id

    :param api_key: client's API key obtained from google cloud console, will look for local environment variable first
    :type api_key: string

    :param place_id: unique identifier of a place
    :type place_id: string

    :rtype: string that represents a website url
    """
    place_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"    
    parameters = {
        "key": api_key,
        "place_id": place_id,
        "fields": "website"
    }
    response = requests.get(place_endpoint, params=parameters)
    results = json.loads(response.content)
    website_url = results['result']['website']
    print(website_url)
    return website_url


def retrieve_list_of_websites(place_id_list):
    """Collects a list of website url from the list of place_id

    :param place_id_list: list of place_id from pinging API or csv extracts
    :type place_id_list: list

    :rtype: list of website urls
    """
    website_list = []
    i = 0

    while i < len(place_id_list):
        try:
            website_list.append(retrieve_google_place_website(place_id=place_id_list[i]))
        except KeyError:
            print('Restaurant {} does not have a website.'.format(place_id_list[i]))
        i += 1
    print(website_list)
    return website_list