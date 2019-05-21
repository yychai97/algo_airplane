from collections import deque, namedtuple
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import os
import string
import time
import webbrowser




##DIJSKTRA ALGORITHM for calculation
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
##OBTAINING COORDINATES FOR CITIES
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

print("Before adding weight of political sentiment, the shortest path for KL to US is ")
print(graph.dijkstra("kul", "aus"))
########################################################################################################################
##MAPPING LINES AND DISTANCE USING HERE MAPS

def callHEREMAPS(location1, location2):
    mapsweb = webbrowser.open_new("https://tkchui.github.io/algomap/map1.html?path=" + str(location1) + "," + str(location2))


callHEREMAPS("Australia", "United States")


########################################################################################################################
##EXTRACTING WORDS
##PLOT BAR GRAPHS OF POSITIVE AND NEGATIVE WORDS BASED ON EACH NEWS
##WORD COUNT AND STOPS WORD


trans_table = str.maketrans(string.punctuation + string.ascii_uppercase,
                            " " * len(string.punctuation) + string.ascii_lowercase)


def get_word_from_file(word):
    word = word.translate(trans_table)
    return word.split()


class Newspaper:
    def __init__(self, name, file):
        self.country = name
        self.word_list = get_word_from_file(file)

        self.word_dict = {}
        self.stop_dict = {}
        self.positive = {}
        self.neutral = {}
        self.negative = {}

    def generate_word_stop(self):
        """
        This is used to generate dict for word frequency.
        :return: None
        """
        for word in self.word_list:
            if not rabin_karp(word, "stop_word.txt"):
                if word in self.word_dict:
                    self.word_dict[word] += 1
                else:
                    self.word_dict[word] = 1
            elif len(word) > 1:
                if word in self.stop_dict:
                    self.stop_dict[word] += 1
                else:
                    self.stop_dict[word] = 1

    def generate_sentiment(self):
        """
        This is used to generate dict for word frequency.
        :return: None
        """
        for word, value in self.word_dict.items():
            if rabin_karp(word, "positive_words.txt"):
                self.positive[word] = value

            if rabin_karp(word, "negative_words.txt"):
                self.negative[word] = value

    def get_sum(self, name):
        attr = getattr(self, name)
        return sum(attr.values())


def plot_count(country_list):
    country_name = []
    country_stop = []
    country_word = []

    for name, newspapers in country_list.items():
        country_stop.append(sum(newspaper.get_sum("stop_dict") for newspaper in newspapers))
        country_word.append(sum(newspaper.get_sum("word_dict") for newspaper in newspapers))
        country_name.append(name)

    trace1 = go.Bar(
        x=country_name,
        y=country_word,
        name='Word Count'
    )
    trace2 = go.Bar(
        x=country_name,
        y=country_stop,
        name='Stop Count'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='grouped-bar')


def plot_sentiment(newspaper_list, name):
    num = [i for i in range(len(newspaper_list))]
    positive = [newspaper.get_sum("positive") for newspaper in newspaper_list]
    negative = [newspaper.get_sum("negative") for newspaper in newspaper_list]

    trace1 = go.Bar(
        x=num,
        y=positive,
        name='Positive'
    )
    trace2 = go.Bar(
        x=num,
        y=negative,
        name='Negative'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=name)


def rabin_karp(pattern, file_name):
    words = open(file_name).read().translate(trans_table)
    length = len(pattern)
    hpattern = hash(pattern)

    is_matched = False
    for i in range(0, len(words) - length):
        hword = hash(words[i:length + i])
        if hword == hpattern:
            if pattern == words[i:length + i]:
                is_matched = True
                break

    return is_matched


def main():
    now = time.time()
    country_list = {}
    for i in os.listdir("news"):
        # Read everything
        country = i[:-6]
        newspaper_list = country_list.setdefault(country, [])
        f = open(os.path.join("news", i), encoding='ISO-8859-1')
        news = Newspaper(country, f.read())
        f.close()
        news.generate_word_stop()
        news.generate_sentiment()
        newspaper_list.append(news)
        country_list[country] = newspaper_list

    plot_count(country_list)
    for name, newspaper_list in country_list.items():
        plot_sentiment(newspaper_list, name)
    print(time.time() - now)
    return country_list

if __name__ == "__main__":
    main()

########################################################################################################################
##HISTOGRAMS OF POSITIVE AND NEGATIVE WORDS




########################################################################################################################
##WEIGHTING POLITICAL SENTIMENT INTO DATA





########################################################################################################################
##PROBABILITY OF RANDOM ROUTES