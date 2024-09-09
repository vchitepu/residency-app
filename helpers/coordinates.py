import geopy.geocoders import Nominatim

class GeoCoord:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="Mapper")

    def locate(self, city, state):
        loc = self.geolocator.geocode(city + ", " + state)
        return (loc.longitude, loc.latitude)


