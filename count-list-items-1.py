from collections import Counter
def word_count(filename):
    with open(filename) as f:
        return Counter(f.read().split())

counter = word_count('//insert text file')
for i in counter:
    print(i, ':', counter[i])