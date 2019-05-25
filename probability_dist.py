

def getNumberOfWords(positive_words, negative_words):
    weight_postive = positive_words * 1.5
    weight_negative = negative_words * 2.0
    return  weight_postive, weight_negative

def newScore(minDistance):
    newscore = minDistance + getNumberOfWords()

    return newscore
def main():



if __name__ == '__main__':
    main()

