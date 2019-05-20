import os
import string
import plotly.plotly as py
import plotly.graph_objs as go

trans_table = str.maketrans(string.punctuation + string.ascii_uppercase,
                            " " * len(string.punctuation) + string.ascii_lowercase)


def get_word_from_file(word):
    word = word.translate(trans_table)
    return word.split()


def generate_dict(word_list, word_dict, stop_dict, file_name):
    for word in word_list:
        if not rabin_karp(word, file_name):
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        elif len(word) > 1:
            if word in stop_dict:
                stop_dict[word] += 1
            else:
                stop_dict[word] = 1

    return word_dict, stop_dict


def plot_count(country_word_list: dict, country_stop_list: dict):
    """

    :param country_word_list: dict
    :param country_stop_list:
    :return:
    """
    country = list(country_word_list.keys())
    count = [sum(country_word_list[i].values()) for i in country]
    stop_count = [sum(country_stop_list[i].values()) for i in country]

    trace1 = go.Bar(
        x=country,
        y=count,
        name='Word Count'
    )
    trace2 = go.Bar(
        x=country,
        y=stop_count,
        name='Stop Count'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='grouped-bar')


def plot_sentiment(sentiment, country_name):
    country = list(sentiment.keys())
    positive = [i['positive'] for i in sentiment.values()]
    negative = [i['negative'] for i in sentiment.values()]

    trace1 = go.Bar(
        x=country,
        y=positive,
        name='Positive'
    )
    trace2 = go.Bar(
        x=country,
        y=negative,
        name='Negative'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='sentiment')


def rabin_karp(pattern, file_name):
    words = open(file_name).read()
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
    country_word_list = {}
    country_stop_list = {}
    country_sentiment = {}
    for i in os.listdir("news"):
        # Read everything
        country = i[:-6]

        try:
            # Get country name
            word_dict = country_word_list[country]
            stop_dict = country_stop_list[country]
            sentiment = country_sentiment[country]
        except KeyError:
            word_dict = {}
            stop_dict = {}
            sentiment = {"positive": 0, "negative": 0}

        f = open(os.path.join("news", i), encoding='ISO-8859-1')
        word_list = get_word_from_file(f.read())
        f.close()

        word_dict, stop_dict = generate_dict(word_list, word_dict, stop_dict, "stop_word.txt")

        country_word_list[country] = word_dict
        country_stop_list[country] = stop_dict

        # Getting from word list
        for word, value in country_word_list[country].items():
            # getting positive
            if rabin_karp(word, "positive_words.txt"):
                sentiment["positive"] += 1
            elif rabin_karp(word, "negative_words.txt"):
                sentiment["negative"] += 1

        country_sentiment[country] = sentiment

    plot_count(country_word_list, country_stop_list)
    plot_sentiment(country_sentiment)


if __name__ == "__main__":
    main()
