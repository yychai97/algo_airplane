from _ast import keyword
from collections import deque, namedtuple, Counter
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import sys
import polyline
import googlemaps
from datetime import datetime
from matching import main

##Djisktra ALgo for calc
# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

##---------------------------------------------------------------------------------------------------------##

plotly.tools.set_credentials_file(username = 'yychai97', api_key = 'OWIMPYbRvRbxNupsoiWe')
geolocator = Nominatim(user_agent="wia2005")

kul = geolocator.geocode("kuala lumpur malaysia")
nz = geolocator.geocode("new zealand")
jpn = geolocator.geocode("japan")
aus = geolocator.geocode("australia")
thai = geolocator.geocode("thailand")
usa = geolocator.geocode("united states")
uk = geolocator.geocode("united kingdom")
ger = geolocator.geocode("germany")
braz = geolocator.geocode("brazil")
haw = geolocator.geocode("hawaii")
hk = geolocator.geocode("hong kong")
sgp = geolocator.geocode("singapore")
kulcoordinate = (kul.latitude, kul.longitude)
nzcoordinate = (nz.latitude, nz.longitude)
jpncoordinate = (jpn.latitude, jpn.longitude)
auscoordinate = (aus.latitude, aus.longitude)
thaicoordinate = (thai.latitude, thai.longitude)
usacoordinate = (usa.latitude, usa.longitude)
ukcoordinate = (uk.latitude, uk.longitude)
gercoordinate = (ger.latitude, ger.longitude)
brazcoordinate = (braz.latitude, braz.longitude)
hawcoordinate = (haw.latitude, haw.longitude)
hkcoordinate = (hk.latitude, hk.longitude)
sgpcoordinate = (sgp.latitude, sgp.longitude)

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

country_list = main()

graph = Graph([
    ("kul", "thai", geodesic(kulcoordinate, thaicoordinate).kilometers*country_list["Thailand"].count_sentiment()),
    ("kul", "hk", geodesic(kulcoordinate, hkcoordinate).kilometers),
    ("kul", "sgp", geodesic(kulcoordinate, sgpcoordinate).kilometers),
    ("thai", "nz", geodesic(thaicoordinate, nzcoordinate).kilometers*country_list["newzealand"].count_sentiment()),
    ("thai", "ger", geodesic(thaicoordinate, gercoordinate).kilometers*country_list["germany"].count_sentiment()),
    ("thai", "haw", geodesic(thaicoordinate, hawcoordinate).kilometers*country_list["hawaii"].count_sentiment()),
    ("thai", "hk", geodesic(thaicoordinate, hkcoordinate).kilometers),
    ("hk", "nz", geodesic(hkcoordinate, nzcoordinate).kilometers*country_list["newzealand"].count_sentiment()),
    ("hk", "ger", geodesic(hkcoordinate, gercoordinate).kilometers*country_list["germany"].count_sentiment()),
    ("hk", "haw", geodesic(hkcoordinate, hawcoordinate).kilometers*country_list["hawaii"].count_sentiment()),
    ("hk", "sgp", geodesic(hkcoordinate, sgpcoordinate).kilometers),
    ("sgp", "nz", geodesic(sgpcoordinate, nzcoordinate).kilometers*country_list["newzealand"].count_sentiment()),
    ("sgp", "ger", geodesic(sgpcoordinate, gercoordinate).kilometers*country_list["germany"].count_sentiment()),
    ("sgp", "haw", geodesic(sgpcoordinate, hawcoordinate).kilometers*country_list["hawaii"].count_sentiment()),
    ("nz", "jpn", geodesic(nzcoordinate, jpncoordinate).kilometers*country_list["Janpan"].count_sentiment()),
    ("nz", "usa", geodesic(nzcoordinate, usacoordinate).kilometers*country_list["Unitedstates"].count_sentiment()),
    ("nz", "ger", geodesic(nzcoordinate, gercoordinate).kilometers*country_list["germany"].count_sentiment()),
    ("ger", "jpn", geodesic(gercoordinate, jpncoordinate).kilometers*country_list["Japan"].count_sentiment()),
    ("ger", "usa", geodesic(gercoordinate, usacoordinate).kilometers*country_list["Unitedstates"].count_sentiment()),
    ("ger", "haw", geodesic(gercoordinate, hawcoordinate).kilometers*country_list["hawaii"].count_sentiment()),
    ("haw", "jpn", geodesic(hawcoordinate, jpncoordinate).kilometers*country_list["Japan"].count_sentiment()),
    ("haw", "usa", geodesic(hawcoordinate, usacoordinate).kilometers*country_list["Unitedstates"].count_sentiment()),
    ("jpn", "aus", geodesic(jpncoordinate, auscoordinate).kilometers*country_list["australia"].count_sentiment()),
    ("jpn", "uk", geodesic(jpncoordinate, ukcoordinate).kilometers*country_list["UK"].count_sentiment()),
    ("jpn", "braz", geodesic(jpncoordinate, brazcoordinate).kilometers),
    ("jpn", "usa", geodesic(jpncoordinate, usacoordinate).kilometers*country_list["Unitedstates"].count_sentiment()),
    ("usa", "aus", geodesic(usacoordinate, auscoordinate).kilometers*country_list["australia"].count_sentiment()),
    ("aus", "uk", geodesic(auscoordinate, ukcoordinate).kilometers*country_list["UK"].count_sentiment()),
    ("usa", "uk", geodesic(usacoordinate, ukcoordinate).kilometers*country_list["UK"].count_sentiment()),
    ("braz", "uk", geodesic(brazcoordinate, ukcoordinate).kilometers*country_list["UK"].count_sentiment()),
    ("usa", "braz", geodesic(usacoordinate, brazcoordinate).kilometers)])

print(graph.dijkstra("kul", "aus"))
####################

gmaps = googlemaps.Client(key='AIzaSyAKeF3vJdrKjN7YHsDKAfrOFjP5wLxaSo8')

#
# ##
# txt = "GEEKS FOR GEEKS"
# pat = "GEEK"
# q = 101  # A prime number
# search(pat, txt, q)
