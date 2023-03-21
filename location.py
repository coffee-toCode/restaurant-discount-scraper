#testing script. moved to APP.py address possibly not needed. 
import geocoder

g = geocoder.ip('me')
if g.ok:
    lat, lng = g.latlng
    LOCATION = f"{lat},{lng}"

# Example usage:
print(f"User's location: {LOCATION}")
#print(f"User's address: {address}")