from collections import deque, namedtuple

import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import plotly
from matching import main
from matching import Newspaper
import os
import time
import webbrowser
import ssl
import certifi
import copy

##DIJSKTRA ALGORITHM for calculation
# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

weight_list = []


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


class Graph:
    def __init__(self, edges, country_list):
        # let's check that the data is right
        self.country_list = country_list
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
                return edge

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
        mappath = path.copy()
        #callHEREMAPS(mappath)
        return path

    def dijkstra_with_weight(self, source, dest):
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
                if neighbour != 'kul':
                    alternative_route = self.country_list[neighbour].count_sentiment() * distances[current_vertex] + cost
                    if alternative_route < distances[neighbour]:
                        distances[neighbour] = alternative_route
                        previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        mappath = path.copy()
        return path


##---------------------------------------------------------------------------------------------------------##
##OBTAINING COORDINATES FOR CITIES
plotly.tools.set_credentials_file(username='yychai97', api_key='TsWmwKFkn3hd8MMIDVEA')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="algo_airplane")

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

country_list = main()

########################################################################################################################
##GETTING DISTANCE BETWEEN DISTANCE
##WILL BE USED FOR CALCULATING AND OBTAINING SHORTEST DISTANCE USING DIJKSTRA'S ALGORITHM

graph = Graph([
    ("kul", "thai", geodesic(kulcoordinate, thaicoordinate).kilometers),
    ("kul", "sgp", geodesic(kulcoordinate, sgpcoordinate).kilometers),
    ("thai", "hk", geodesic(thaicoordinate, hkcoordinate).kilometers),
    ("thai", "jpn", geodesic(thaicoordinate, jpncoordinate).kilometers),
    ("thai", "aus", geodesic(thaicoordinate, auscoordinate).kilometers),
    ("thai", "sgp", geodesic(thaicoordinate, sgpcoordinate).kilometers),
    ("sgp", "hk", geodesic(sgpcoordinate, hkcoordinate).kilometers),
    ("sgp", "jpn", geodesic(sgpcoordinate, jpncoordinate).kilometers),
    ("sgp", "aus", geodesic(sgpcoordinate, auscoordinate).kilometers),
    ("hk", "thai", geodesic(hkcoordinate, thaicoordinate).kilometers),
    ("hk", "sgp", geodesic(hkcoordinate, sgpcoordinate).kilometers),
    ("hk", "jpn", geodesic(hkcoordinate, jpncoordinate).kilometers),
    ("hk", "aus", geodesic(hkcoordinate, auscoordinate).kilometers),
    ("hk", "haw", geodesic(hkcoordinate, hawcoordinate).kilometers),
    ("hk", "nz", geodesic(hkcoordinate, nzcoordinate).kilometers),
    ("hk", "uk", geodesic(hkcoordinate, ukcoordinate).kilometers),
    ("jpn", "thai", geodesic(jpncoordinate, thaicoordinate).kilometers),
    ("jpn", "sgp", geodesic(jpncoordinate, sgpcoordinate).kilometers),
    ("jpn", "hk", geodesic(jpncoordinate, hkcoordinate).kilometers),
    ("jpn", "aus", geodesic(jpncoordinate, auscoordinate).kilometers),
    ("jpn", "haw", geodesic(jpncoordinate, hawcoordinate).kilometers),
    ("jpn", "nz", geodesic(jpncoordinate, nzcoordinate).kilometers),
    ("jpn", "uk", geodesic(jpncoordinate, ukcoordinate).kilometers),
    ("aus", "thai", geodesic(auscoordinate, thaicoordinate).kilometers),
    ("aus", "sgp", geodesic(auscoordinate, sgpcoordinate).kilometers),
    ("aus", "hk", geodesic(auscoordinate, hkcoordinate).kilometers),
    ("aus", "jpn", geodesic(auscoordinate, jpncoordinate).kilometers),
    ("aus", "haw", geodesic(auscoordinate, hawcoordinate).kilometers),
    ("aus", "nz", geodesic(auscoordinate, nzcoordinate).kilometers),
    ("aus", "uk", geodesic(auscoordinate, ukcoordinate).kilometers),
    ("haw", "hk", geodesic(hawcoordinate, hkcoordinate).kilometers),
    ("haw", "jpn", geodesic(hawcoordinate, jpncoordinate).kilometers),
    ("haw", "aus", geodesic(hawcoordinate, auscoordinate).kilometers),
    ("haw", "nz", geodesic(hawcoordinate, nzcoordinate).kilometers),
    ("haw", "uk", geodesic(hawcoordinate, ukcoordinate).kilometers),
    ("haw", "usa", geodesic(hawcoordinate, usacoordinate).kilometers),
    ("haw", "braz", geodesic(hawcoordinate, brazcoordinate).kilometers),
    ("haw", "ger", geodesic(hawcoordinate, gercoordinate).kilometers),
    ("nz", "hk", geodesic(nzcoordinate, hkcoordinate).kilometers),
    ("nz", "jpn", geodesic(nzcoordinate, jpncoordinate).kilometers),
    ("nz", "aus", geodesic(nzcoordinate, auscoordinate).kilometers),
    ("nz", "haw", geodesic(nzcoordinate, hawcoordinate).kilometers),
    ("nz", "uk", geodesic(nzcoordinate, ukcoordinate).kilometers),
    ("nz", "usa", geodesic(nzcoordinate, usacoordinate).kilometers),
    ("nz", "braz", geodesic(nzcoordinate, brazcoordinate).kilometers),
    ("nz", "ger", geodesic(nzcoordinate, gercoordinate).kilometers),
    ("uk", "hk", geodesic(ukcoordinate, hkcoordinate).kilometers),
    ("uk", "jpn", geodesic(ukcoordinate, jpncoordinate).kilometers),
    ("uk", "aus", geodesic(ukcoordinate, auscoordinate).kilometers),
    ("uk", "haw", geodesic(ukcoordinate, hawcoordinate).kilometers),
    ("uk", "nz", geodesic(ukcoordinate, nzcoordinate).kilometers),
    ("uk", "usa", geodesic(ukcoordinate, usacoordinate).kilometers),
    ("uk", "braz", geodesic(ukcoordinate, brazcoordinate).kilometers),
    ("uk", "ger", geodesic(ukcoordinate, gercoordinate).kilometers),
    ("usa", "haw", geodesic(usacoordinate, hawcoordinate).kilometers),
    ("usa", "nz", geodesic(usacoordinate, nzcoordinate).kilometers),
    ("usa", "uk", geodesic(usacoordinate, ukcoordinate).kilometers),
    ("usa", "braz", geodesic(usacoordinate, brazcoordinate).kilometers),
    ("usa", "ger", geodesic(usacoordinate, gercoordinate).kilometers),
    ("braz", "haw", geodesic(brazcoordinate, hawcoordinate).kilometers),
    ("braz", "nz", geodesic(brazcoordinate, nzcoordinate).kilometers),
    ("braz", "uk", geodesic(brazcoordinate, ukcoordinate).kilometers),
    ("braz", "usa", geodesic(brazcoordinate, usacoordinate).kilometers),
    ("braz", "ger", geodesic(brazcoordinate, gercoordinate).kilometers),
    ("ger", "haw", geodesic(gercoordinate, hawcoordinate).kilometers),
    ("ger", "nz", geodesic(gercoordinate, nzcoordinate).kilometers),
    ("ger", "uk", geodesic(gercoordinate, ukcoordinate).kilometers),
    ("ger", "usa", geodesic(gercoordinate, usacoordinate).kilometers),
    ("ger", "braz", geodesic(gercoordinate, brazcoordinate).kilometers)], country_list=country_list)

##MAPPING LINES AND DISTANCE USING HERE MAPS

def callHEREMAPS(locationlist):
    mapsweb = "https://tkchui.github.io/algomap/map1.html?path="
    newmapsweb = mapsweb + ",".join(locationlist)
    webbrowser.open_new(newmapsweb)


########################################################################################################################
##PROBABILITY OF RANDOM ROUTES


########################################################################################################################


#  print(time.time() - now)
if __name__ == "__main__":
    print("Before adding weight of political sentiment, list of destinations: ")
    print(graph.dijkstra("kul", "usa"))
    print(graph.dijkstra("kul", "ger"))
    print(graph.dijkstra("kul", "uk"))
    print(graph.dijkstra("kul", "braz"))
    print(graph.dijkstra("kul", "jpn"))
    print(graph.dijkstra("kul", "aus"))
    print("After adding weight of political sentiment, list of destinations: ")
    print(graph.dijkstra_with_weight("kul", "usa"))
    print(graph.dijkstra_with_weight("kul", "ger"))
    print(graph.dijkstra_with_weight("kul", "uk"))
    print(graph.dijkstra_with_weight("kul", "braz"))
    print(graph.dijkstra_with_weight("kul", "jpn"))
    print(graph.dijkstra_with_weight("kul", "aus"))
