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
        callHEREMAPS(mappath)
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

    def list_possible_route(self, src, dest):
        self.possible_route = []
        small_list = [(src, 0)]
        for node in self.neighbours[src]:
            self.list_recursive(node, small_list, src, dest)
        return self.possible_route

    def list_recursive(self, node, small_list, src, dest):
        new_list = small_list + [node]
        # name, distance = node
        if node[0] == dest:
            self.possible_route.append(new_list)
            return
        for name, distance in self.neighbours[node[0]]:
            if name == src or (name in [i[0] for i in new_list]):
                pass
            else:
                self.list_recursive((name, distance), new_list, src, dest)


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

#country_list = main()

########################################################################################################################
##GETTING DISTANCE BETWEEN DISTANCE
##WILL BE USED FOR CALCULATING AND OBTAINING SHORTEST DISTANCE USING DIJKSTRA'S ALGORITHM

graph = Graph([
    ("kul", "thai", geodesic(kulcoordinate, thaicoordinate).kilometers),
    ("kul", "hk", geodesic(kulcoordinate, hkcoordinate).kilometers),
    ("kul", "sgp", geodesic(kulcoordinate, sgpcoordinate).kilometers),
    ("thai", "nz", geodesic(thaicoordinate, nzcoordinate).kilometers),
    ("thai", "ger", geodesic(thaicoordinate, gercoordinate).kilometers),
    ("thai", "haw", geodesic(thaicoordinate, hawcoordinate).kilometers),
    ("thai", "hk", geodesic(thaicoordinate, hkcoordinate).kilometers),
    ("usa", "braz", geodesic(usacoordinate, brazcoordinate).kilometers),
    ("hk", "thai", geodesic(hkcoordinate, thaicoordinate).kilometers),
    ("hk", "nz", geodesic(hkcoordinate, nzcoordinate).kilometers),
    ("hk", "ger", geodesic(hkcoordinate, gercoordinate).kilometers),
    ("hk", "haw", geodesic(hkcoordinate, hawcoordinate).kilometers),
    ("hk", "sgp", geodesic(hkcoordinate, sgpcoordinate).kilometers),
    ("sgp", "hk", geodesic(sgpcoordinate, hkcoordinate).kilometers),
    ("sgp", "nz", geodesic(sgpcoordinate, nzcoordinate).kilometers),
    ("sgp", "ger", geodesic(sgpcoordinate, gercoordinate).kilometers),
    ("sgp", "haw", geodesic(sgpcoordinate, hawcoordinate).kilometers),
    ("nz", "jpn", geodesic(nzcoordinate, jpncoordinate).kilometers),
    ("nz", "usa", geodesic(nzcoordinate, usacoordinate).kilometers),
    ("nz", "ger", geodesic(nzcoordinate, gercoordinate).kilometers),
    ("nz", "thai", geodesic(nzcoordinate, thaicoordinate).kilometers),
    ("nz", "hk", geodesic(nzcoordinate, hkcoordinate).kilometers),
    ("nz", "sgp", geodesic(nzcoordinate, sgpcoordinate).kilometers),
    ("ger", "jpn", geodesic(gercoordinate, jpncoordinate).kilometers),
    ("ger", "usa", geodesic(gercoordinate, usacoordinate).kilometers),
    ("ger", "haw", geodesic(gercoordinate, hawcoordinate).kilometers),
    ("ger", "thai", geodesic(gercoordinate, thaicoordinate).kilometers),
    ("ger", "hk", geodesic(gercoordinate, hkcoordinate).kilometers),
    ("ger", "sgp", geodesic(gercoordinate, sgpcoordinate).kilometers),
    ("ger", "nz", geodesic(gercoordinate, nzcoordinate).kilometers),
    ("haw", "jpn", geodesic(hawcoordinate, jpncoordinate).kilometers),
    ("haw", "usa", geodesic(hawcoordinate, usacoordinate).kilometers),
    ("haw", "thai", geodesic(hawcoordinate, thaicoordinate).kilometers),
    ("haw", "hk", geodesic(hawcoordinate, hkcoordinate).kilometers),
    ("haw", "sgp", geodesic(hawcoordinate, sgpcoordinate).kilometers),
    ("haw", "ger", geodesic(hawcoordinate, gercoordinate).kilometers),
    ("jpn", "aus", geodesic(jpncoordinate, auscoordinate).kilometers),
    ("jpn", "uk", geodesic(jpncoordinate, ukcoordinate).kilometers),
    ("jpn", "braz", geodesic(jpncoordinate, brazcoordinate).kilometers),
    ("jpn", "usa", geodesic(jpncoordinate, usacoordinate).kilometers),
    ("jpn", "nz", geodesic(jpncoordinate, nzcoordinate).kilometers),
    ("jpn", "ger", geodesic(jpncoordinate, gercoordinate).kilometers),
    ("jpn", "haw", geodesic(jpncoordinate, hawcoordinate).kilometers),
    ("usa", "aus", geodesic(usacoordinate, auscoordinate).kilometers),
    ("usa", "uk", geodesic(usacoordinate, ukcoordinate).kilometers),
    ("usa", "braz", geodesic(usacoordinate, brazcoordinate).kilometers),
    ("usa", "nz", geodesic(usacoordinate, nzcoordinate).kilometers),
    ("usa", "ger", geodesic(usacoordinate, gercoordinate).kilometers),
    ("usa", "haw", geodesic(usacoordinate, hawcoordinate).kilometers),
    ("usa", "jpn", geodesic(usacoordinate, jpncoordinate).kilometers),
    ("aus", "uk", geodesic(auscoordinate, ukcoordinate).kilometers),
    ("aus", "jpn", geodesic(auscoordinate, jpncoordinate).kilometers),
    ("aus", "usa", geodesic(auscoordinate, usacoordinate).kilometers),
    ("uk", "jpn", geodesic(ukcoordinate, jpncoordinate).kilometers),
    ("uk", "usa", geodesic(ukcoordinate, usacoordinate).kilometers),
    ("uk", "aus", geodesic(ukcoordinate, auscoordinate).kilometers),
    ("uk", "braz", geodesic(ukcoordinate, brazcoordinate).kilometers),
    ("braz", "uk", geodesic(brazcoordinate, ukcoordinate).kilometers),
    ("braz", "jpn", geodesic(brazcoordinate, jpncoordinate).kilometers),
    ("braz", "usa", geodesic(brazcoordinate, usacoordinate).kilometers)], country_list=None)
graph.list_possible_route("kul", "uk")
##MAPPING LINES AND DISTANCE USING HERE MAPS

def callHEREMAPS(locationlist):
    mapsweb = "https://tkchui.github.io/algomap/map1.html?path="
    newmapsweb = mapsweb + ",".join(locationlist)
    webbrowser.open_new(newmapsweb)


########################################################################################################################
##PROBABILITY OF RANDOM ROUTES


########################################################################################################################
def main():
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


#  print(time.time() - now)
if __name__ == "__main__":
    main()
