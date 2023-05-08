# restaurant-instagram-scraper

Depending on the user's device location, the app can search the restaurants within range (currently 5km) and returns their instagram links (if they have an instagram account).

The current itteration of this app requires a google cloud platform account and a Maps API Key. This key is placed in a .env file and called several times within the code.

## Local setup

Clone the repository to your favorite IDE, and in the repo's root directory, run

```
python -m venv .venv

(mac,linux)
   source .venv/bin/activate

(windows)
   .venv\Scripts\activate


pip install -r requirements.txt
```

Then you should be good to start


## run the app

(windows)
   python .\app.py