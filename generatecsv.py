import csv

def generate_csv(response_list):
    with open('places.csv', mode='w', newline='') as csv_file:
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

retrieve_google_place()
generate_csv(response_list)