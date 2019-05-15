from _ast import keyword

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import polyline
import googlemaps
import requests
from datetime import datetime


##Djisktra ALgo for calc
class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def printSolution(self, dist):
        print("Vertex tDistance from Source")
        for node in range(self.V):
            print(node, "t", dist[node])

    def minDistance(self, dist, sptSet):
        min = sys.maxsize

        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    def djikstra(self, src):

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * (self.V)

        for cout in range(self.V):
            u = self.minDistance(dist, sptSet)
            sptSet[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and sptSet[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
        self.printSolution(dist)

##rabin-karp algo
d = 256

# pat  -> pattern
# txt  -> text
# q    -> A prime number

def search(pat, txt, q):
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0
    t = 0
    h = 1

    for i in range(M - 1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q

    for i in range(N - M + 1):

        if p == t:
            # Check for characters one by one
            for j in range(M):
                if txt[i + j] != pat[j]:
                    break

            j += 1
            if j == M:
                print
                "Pattern found at index " + str(i)


        if i < N - M:
            t = (d * (t - ord(txt[i]) * h) + ord(txt[i + M])) % q

            if t < 0:
                t = t + q


##---------------------------------------------------------------------------------------------------------##

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

g = Graph(9)
g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]
          ]

g.djikstra(0)


####################

gmaps = googlemaps.Client(key='AIzaSyAKeF3vJdrKjN7YHsDKAfrOFjP5wLxaSo8')
print("hallo")

##
txt = "GEEKS FOR GEEKS"
pat = "GEEK"
q = 101  # A prime number
search(pat, txt, q)
