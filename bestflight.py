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
overallsum = 0


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

country_list = main()

########################################################################################################################
##GETTING DISTANCE BETWEEN DISTANCE
##WILL BE USED FOR CALCULATING AND OBTAINING SHORTEST DISTANCE USING DIJKSTRA'S ALGORITHM

graph = Graph([
    ("kul", "thai", geodesic(kulcoordinate, thaicoordinate).kilometers),
    ("kul", "sgp", geodesic(kulcoordinate, sgpcoordinate).kilometers),
    ("kul", "hk", geodesic(kulcoordinate, hkcoordinate).kilometers),
    ("thai", "hk", geodesic(thaicoordinate, hkcoordinate).kilometers),
    ("thai", "jpn", geodesic(thaicoordinate, jpncoordinate).kilometers),
    ("thai", "aus", geodesic(thaicoordinate, auscoordinate).kilometers),
    ("thai", "uk", geodesic(thaicoordinate, ukcoordinate).kilometers),
    ("sgp", "aus", geodesic(sgpcoordinate, auscoordinate).kilometers),
    ("hk", "jpn", geodesic(hkcoordinate, jpncoordinate).kilometers),
    ("jpn", "haw", geodesic(jpncoordinate, hawcoordinate).kilometers),
    ("jpn", "nz", geodesic(jpncoordinate, nzcoordinate).kilometers),
    ("aus", "nz", geodesic(auscoordinate, nzcoordinate).kilometers),
    ("aus", "uk", geodesic(auscoordinate, ukcoordinate).kilometers),
    ("haw", "usa", geodesic(hawcoordinate, usacoordinate).kilometers),
    ("haw", "braz", geodesic(hawcoordinate, brazcoordinate).kilometers),
    ("nz", "hk", geodesic(nzcoordinate, hkcoordinate).kilometers),
    ("nz", "haw", geodesic(nzcoordinate, hawcoordinate).kilometers),
    ("nz", "braz", geodesic(nzcoordinate, brazcoordinate).kilometers),
    ("uk", "usa", geodesic(ukcoordinate, usacoordinate).kilometers),
    ("uk", "braz", geodesic(ukcoordinate, brazcoordinate).kilometers),
    ("usa", "haw", geodesic(usacoordinate, hawcoordinate).kilometers),
    ("usa", "braz", geodesic(usacoordinate, brazcoordinate).kilometers),
    ("usa", "ger", geodesic(usacoordinate, gercoordinate).kilometers),
    ("braz", "haw", geodesic(brazcoordinate, hawcoordinate).kilometers),
    ("braz", "usa", geodesic(brazcoordinate, usacoordinate).kilometers),
    ("ger", "haw", geodesic(gercoordinate, hawcoordinate).kilometers),
    ("ger", "nz", geodesic(gercoordinate, nzcoordinate).kilometers),
    ("ger", "uk", geodesic(gercoordinate, ukcoordinate).kilometers)], country_list)


##MAPPING LINES AND DISTANCE USING HERE MAPS

def callHEREMAPS(locationlist):
    mapsweb = "https://tkchui.github.io/algomap/map1.html?path="
    newmapsweb = mapsweb + ",".join(locationlist)
    webbrowser.open_new(newmapsweb)


########################################################################################################################
##PROBABILITY OF RANDOM ROUTES
def probability_routes(sumofpath, overallsum):
    print("Probability of route: ")
    probability_oneroute = (sumofpath/ overallsum)
    return probability_oneroute



def get_total_distance(a_graph, src, dest):
    a_graph.list_possible_route(src, dest)
    return sum(get_distance_from_list(a_list) for a_list in a_graph.possible_route)


def get_distance_from_list(a_list):
    name_list = []
    global overallsum
    sum = 0
    for name, distance in a_list:
        name_list.append(name)
        sum += distance
    overallsum += sum
    print("Route: ", name_list)
    print("Total distance:", sum)
    print("------------------------------------------")
    return sum



########################################################################################################################


#  print(time.time() - now)
if __name__ == "__main__":
    print(get_total_distance(graph, "kul", "usa"))
    print()
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
