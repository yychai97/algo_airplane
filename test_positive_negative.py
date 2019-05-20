import os

newsentries = os.listdir('news/')

dictionary_positive = []
dictionary_negative = []
positive_words = open("positive_words.txt", "r")
#sample_positive = positive_words.read().lower().split()
for line_positive in positive_words:
    a = line_positive.lower().split(" ")
    dictionary_positive.append(a)
negative_words = open("negative_words.txt", "r")
#sample_negative = negative_words.read().lower().split()
for line_negative in negative_words:
    b = line_negative.lower().split()
    dictionary_negative.append(b)

def wordfrequency_positive(input1):





#    for line_positive in input1:
 #       if line_positive.split(" ") in dictionary_positive:
  #          print(line_positive.split())

#def wordfrequency_negative(input2):

 #   for line_negative_in input2:
  #      if line_negative.split()[0] in dictionary_negative:
   #         print(line_negative.split()[0])


for entry in newsentries:
    news_entry = "news/" + entry
    news_file = open(news_entry, "r")
    print("Reading file " + entry)
    wordfrequency_positive(news_file)
 #   wordfrequency_negative(news_file)
