# restaurant-discount-scraper

Depending on the user's range input, the app can search the restaurants within that range and the discount deals they offer from their instagram posts (if they have an instagram account).

## Local setup

Clone the repository to your favorite IDE, and in the repo's root directory, run

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then you should be good to start!

## Wishlist

- [ ] Determine how many [Google Maps API requests](https://developers.google.com/maps/documentation/places/web-service/details) can be made for a free account
- [ ] Nice and helpful UI to present the filtered result (could include details such as restaurant's contact and actual website)
- [ ] Maybe or maybe not a database needed to store the returned results (depends on the design, maybe two users' range inputs overlap big enough to not have to ping the API for fresh data)
- [ ] Write tests for the functions in `app.py`
