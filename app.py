import googlemaps
from googlemaps import places
import os
import config
import time
import timeit
from pandas import json_normalize, concat, read_csv
import requests
import json
import pytesseract as pyt
from PIL import Image
from bs4 import BeautifulSoup
import re
from jinja2 import Template
import io
import sys
import subprocess
from pipes import quote
import shutil
from urllib import request
import doctest


def retrieve_google_place(api_key=config.API_KEY, coordinate=config.LOCATION, radius=5000):
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
    response_list = []
    parameters = {
        "key": api_key,
        "location": coordinate,
        "radius": radius,
        "type": 'restaurant'
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


def create_response_df(response_list):
    wanted_columns = ['name', 'place_id', 'rating', 'types', 'user_ratings_total', 'geometry.location.lat',
                      'geometry.location.lng']

    new_response_list = [json_normalize(i, errors='ignore')[wanted_columns] for i in response_list]
    df = concat(new_response_list)
    return df


def retrieve_google_place_website(api_key=config.API_KEY, place_id=None):
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

    return website_list


def scrape_social_media(url):
    """Scrape the instagram account from the webpage's source code

    :param url: url of the restaurant's website (ex, www.domain.(com)|(ca) OR domain.(com)|(ca))
    :type url: string

    :rtype: string that reflects the restaurant's social media website url (instagram.com/)
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    if re.match('.+www.+', url) is not None:
        domain_with_anchor = re.search("\..+\.(?!ca)|\..+\.(?!com)", url)
        domain = url[domain_with_anchor.start() + 1:domain_with_anchor.end() - 1]
    else:
        domain_with_anchor = re.search("/.+\.(?!ca)|/.+\.(?!com)", url)
        domain = url[domain_with_anchor.start() + 2:domain_with_anchor.end() - 1]
    for link in soup.find_all('a', attrs={
        'href': re.compile("(instagram)\.(com)/.*{}.*".format(domain[:5]))}):
        social_media_url = link.get('href')
        return social_media_url


def process_image(pic):
    pyt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(pyt.image_to_string(Image.open(pic)))


def instagram_discount_text(json_file):
    """Process the captions of a post to identify the posts with highest relevance to discount"""
    with open(json_file, 'r', encoding='utf-8') as json_format:
        comment_json = json.load(json_format)['GraphImages']
    image_url = [re.search('\/(?!.*\/).*(?=\.(jpg))', i['display_url']).group(0)[1:] for i in comment_json]
    image_text = [''.join(j['node']['text'] for j in i['edge_media_to_caption']['edges']) for i in comment_json]
    image_url_dict = dict(zip(image_url, image_text))
    discount_keyword = ['discount', '\%', '\$', '(\s|\W)off(\s|\W)', 'price', '(\s|\W)card(\s|\W)', 'certificate',
                        'stamp', 'point', 'sale', 'sample', 'offer']
    relevant_post = {(k, v) for p in discount_keyword for k, v in image_url_dict.items() if re.search(p, v) is not None}
    return relevant_post


def start_instagram_scraper():
    os.chdir(r"venv\Scripts")
    print(os.getcwd())
    cp = subprocess.run(
        ["instagram-scraper", "hakatashoryuken", "--comments"],
        universal_newlines=True, shell=True, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cp.stdout)


def printTohtml(relevant_post):
    html_text = """<html>
    <head>...</head>
    <body>
        {% for image, text in posts %}
            <div style="float:left"><img src="static/{{ image }}.jpg"></div>
            <div style="float:right">{{ text }}</div>
        {% endfor %}
        <div style="clear:both"></div>
    </body>
    </html>"""

    my_templ = Template(html_text)
    with io.open('temp.html', 'w', encoding='utf-8') as f:
        f.write(my_templ.render(posts=relevant_post))


if __name__ == "__main__":
    print([i['place_id'] for i in retrieve_google_place(radius=10000)])
    # restaurant_df = read_csv('restaurant_on_google.csv')
    # res_place_id_list = restaurant_df['place_id'].tolist()
    # res_official_url = retrieve_list_of_websites(res_place_id_list)
    # scrape_list = [(url, requests.get(url).status_code) for url in res_official_url if
    #                requests.get(url).status_code < 400]
    # print(len(scrape_list))
    # res_instagram_url = [scrape_social_media(res[0]) for res in scrape_list]
    # print(res_instagram_url, len(res_instagram_url))

    # process_image('static/101250309_1440344812830050_4269460284752014425_n.jpg')
    # relevant_list = instagram_discount_text('static/konjiki_ramen.json')
    # printTohtml(relevant_list)
    # start_instagram_scraper()