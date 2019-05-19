from _ast import keyword
from collections import deque, namedtuple
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import googlemaps

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

########################################################################################################################
##RABIN-KARP ALGORITHM
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

########################################################################################################################
#CHECK FOR POSITIVE AND NEGATIVE WORDS

def wordfrequency_positive(input):
    positive_words = open("positive_words.txt", "r")
    sample_positive = positive_words.read().lower().split();
    frequency_positive = {}
    for i in input:
        if (i in sample_positive):
            frequency_positive[i] += 1
        else:
            frequency_positive[i] = 1

def wordfrequency_negative(input):
    negative_words = open("negative_words.txt", "r")
    frequency_negative = {}
    for i in input:
        if (i in negative_words):
            frequency_negative[i] += 1
        else:
            frequency_negative[i] = 1

########################################################################################################################

plotly.tools.set_credentials_file(username = 'yychai97', api_key = 'OWIMPYbRvRbxNupsoiWe')
geolocator = Nominatim(user_agent = "wia2005")

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
coordinateset = [kulcoordinate, nzcoordinate, jpncoordinate, auscoordinate, thaicoordinate, usacoordinate, ukcoordinate, gercoordinate
                 , brazcoordinate, hawcoordinate, hkcoordinate, sgpcoordinate]

graph = Graph([
    ("kul", "thai", geodesic(kulcoordinate, thaicoordinate).kilometers),
    ("kul", "hk", geodesic(kulcoordinate, hkcoordinate).kilometers),
    ("kul", "sgp", geodesic(kulcoordinate, sgpcoordinate).kilometers),
    ("thai", "nz", geodesic(thaicoordinate, nzcoordinate).kilometers),
    ("thai", "ger", geodesic(thaicoordinate, gercoordinate).kilometers),
    ("thai", "haw", geodesic(thaicoordinate, hawcoordinate).kilometers),
    ("thai", "hk", geodesic(thaicoordinate, hkcoordinate).kilometers),
    ("hk", "nz", geodesic(hkcoordinate, nzcoordinate).kilometers),
    ("hk", "ger", geodesic(hkcoordinate, gercoordinate).kilometers),
    ("hk", "haw", geodesic(hkcoordinate, hawcoordinate).kilometers),
    ("hk", "sgp", geodesic(hkcoordinate, sgpcoordinate).kilometers),
    ("sgp", "nz", geodesic(sgpcoordinate, nzcoordinate).kilometers),
    ("sgp", "ger", geodesic(sgpcoordinate, gercoordinate).kilometers),
    ("sgp", "haw", geodesic(sgpcoordinate, hawcoordinate).kilometers),
    ("nz", "jpn", geodesic(nzcoordinate, jpncoordinate).kilometers),
    ("nz", "usa", geodesic(nzcoordinate, usacoordinate).kilometers),
    ("nz", "ger", geodesic(nzcoordinate, gercoordinate).kilometers),
    ("ger", "jpn", geodesic(gercoordinate, jpncoordinate).kilometers),
    ("ger", "usa", geodesic(gercoordinate, usacoordinate).kilometers),
    ("ger", "haw", geodesic(gercoordinate, hawcoordinate).kilometers),
    ("haw", "jpn", geodesic(hawcoordinate, jpncoordinate).kilometers),
    ("haw", "usa", geodesic(hawcoordinate, usacoordinate).kilometers),
    ("jpn", "aus", geodesic(jpncoordinate, auscoordinate).kilometers),
    ("jpn", "uk", geodesic(jpncoordinate, ukcoordinate).kilometers),
    ("jpn", "braz", geodesic(jpncoordinate, brazcoordinate).kilometers),
    ("jpn", "usa", geodesic(jpncoordinate, usacoordinate).kilometers),
    ("usa", "aus", geodesic(usacoordinate, auscoordinate).kilometers),
    ("aus", "uk", geodesic(auscoordinate, ukcoordinate).kilometers),
    ("usa", "uk", geodesic(usacoordinate, ukcoordinate).kilometers),
    ("braz", "uk", geodesic(brazcoordinate, ukcoordinate).kilometers),
    ("usa", "braz", geodesic(usacoordinate, brazcoordinate).kilometers)])

print(graph.dijkstra("kul", "aus"))
########################################################################################################################

trace0 = go.Scatter(x = [coordinateset], y = coordinateset.__contains__('longitude'))
#trace1 = go.Scatter(
 #   x=[1, 2, 3, 4],
  #  y=[16, 5, 11, 9]
#)
data = [trace0]
py.plot(data, filename = 'basic-line', auto_open=True)

########################################################################################################################

gmaps = googlemaps.Client(key='AIzaSyAKeF3vJdrKjN7YHsDKAfrOFjP5wLxaSo8')
print("hallo")

##


txt = "GEEKS FOR GEEKS"
pat = "GEEK"
q = 101  # A prime number
search(pat, txt, q)
