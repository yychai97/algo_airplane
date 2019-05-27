import os
import string
import plotly.plotly as py
import plotly.graph_objs as go
import time
from concurrent import futures

trans_table = str.maketrans(string.punctuation + string.ascii_uppercase,
                            " " * len(string.punctuation) + string.ascii_lowercase)


def get_word_from_file(word):
    word = word.translate(trans_table)
    return word.split()


class Country:
    def __init__(self, name):
        self.name = name
        self.newspaper_list = []
        self.sentiment = {}
        self.word = {}

    def add_newspaper(self, newspaper):
        self.newspaper_list.append(newspaper)

    def count_sentiment(self):
        if len(self.sentiment) == 0:
            self.sentiment["positive"] = sum(newspaper.get_sum("positive") for newspaper in self.newspaper_list)
            self.sentiment["negative"] = sum(newspaper.get_sum("negative") for newspaper in self.newspaper_list)
            self.sentiment["neutral"] = int(sum(newspaper.get_sum("word_dict") for newspaper in self.newspaper_list)) \
                                        - self.sentiment["positive"] - self.sentiment["negative"]

        return (self.sentiment["positive"]) * (-0.25) + (self.sentiment["negative"]) * (0.3)

    def count_word_stop(self):
        if len(self.word) == 0:
            self.word["stop"] = sum(newspaper.get_sum("stop_dict") for newspaper in self.newspaper_list)
            self.word["word"] = sum(newspaper.get_sum("word_dict") for newspaper in self.newspaper_list)

        return self.word["stop"], self.word["word"]

    def __eq__(self, obj):
        return isinstance(obj, Country) and obj.name == self.name


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

    def process_sentiment(self):
        max_worker = min(len(self.word_dict), 20)
        with futures.ThreadPoolExecutor(max_worker) as executor:
            to_do = []
            for word_list in self.word_dict.keys():
                future = executor.submit(self._generate_sentiment, word_list)
                to_do.append(future)

            results = []
            for future in futures.as_completed(to_do):
                res = future.result()
                print(future)
                results.append(res)

    def _generate_sentiment(self, word):
        """
        This is used to generate dict for word frequency.
        :return: None
        """
        if rabin_karp(word, "positive_words.txt"):
            self.positive[word] = self.word_dict[word]
        if rabin_karp(word, "negative_words.txt"):
            self.negative[word] = self.word_dict[word]

    def get_sum(self, name):
        attr = getattr(self, name)
        return sum(attr.values())


def plot_count(country_list):
    country_name = []
    country_stop = []
    country_word = []

    for country in country_list.values():
        country_stop.append(country.word["word"])
        country_word.append(country.word["stop"])
        country_name.append(country.name)

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


def plot_sentiment(country_list):
    num = []
    positive = []
    negative = []
    neutral = []
    for country in country_list.values():
        num.append(country.name)
        positive.append(country.sentiment["positive"])
        negative.append(country.sentiment["negative"])
        neutral.append(country.sentiment["neutral"])

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
    trace3 = go.Bar(
        x=num,
        y=neutral,
        name='Neutral'
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename="country")


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
        country_name = i[:-6]
        country = country_list.setdefault(country_name, Country(country_name))

        f = open(os.path.join("news", i), encoding='ISO-8859-1')
        news = Newspaper(country_name, f.read())
        f.close()
        news.generate_word_stop()
        news.process_sentiment()
        country.add_newspaper(news)
        country_list[country_name] = country
    # plot_count(country_list)
    # for name, newspaper_list in country_list.items():
    #     plot_sentiment(newspaper_list, name)
    _ = [country.count_sentiment() for country in country_list.values()]
    _ = [country.count_word_stop() for country in country_list.values()]

    plot_sentiment(country_list)
    plot_count(country_list)
    print(time.time() - now)
    return country_list


if __name__ == "__main__":
    x = main()
    print(x)
