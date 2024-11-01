from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import numpy as np

# Read names from csv file (https://familieretshuset.dk/navne/navne/godkendte-fornavne)
names=pd.read_csv("names.csv")

# Sort, first by length, then alphabetically
names_sort=sorted(names["Name"],key = lambda x : (len(x),x))

# Empty dict of Letters
letters = defaultdict(lambda:0)

# Count of letters
for i in names_sort:
    for j in [x for x in i]:
        if j not in (" ","-","'"):
            letters[j.lower()] += 1

# Sorting and filtering
letters = dict(sorted(letters.items(),key=lambda x:x[1], reverse=True))
letters = dict(filter(lambda x: x[1] > 500, letters.items()))

# Plotting
plt.subplot(2, 1, 1)
plt.title("Number of letters")
plt.bar(letters.keys(), letters.values())
plt.subplots_adjust(hspace=0.5,)

# WordCloud
wc = WordCloud().generate_from_frequencies(frequencies=letters)
plt.subplot(2, 1, 2)
plt.title("WordCloud")
plt.imshow(wc)
plt.axis("off")
plt.show()
