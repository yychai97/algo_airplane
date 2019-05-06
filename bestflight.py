from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username = 'yychai97', api_key = 'OWIMPYbRvRbxNupsoiWe')
geolocator = Nominatim(user_agent = "wia2005")
location = geolocator.geocode("Raub Pahang")
location2 = geolocator.geocode("Kuala Lumpur")
coordinates = (location.latitude, location.longitude)
coordinates2 = (location2.latitude, location.longitude)

print(location.address)
print((location.latitude, location.longitude))
print(location2.address)
print((location2.latitude, location2.longitude))
print(geodesic(coordinates, coordinates2).kilometers)

trace0 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = go.Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = [trace0, trace1]

py.plot(data, filename = 'basic-line', auto_open=True)