#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: index.py
# SPECIFICATION: Builds an inverted index from a document collection
#                using surface-level normalization and lemmatization.
# FOR: CS 4250 - Assignment #1
# TIME SPENT: 1 hour 30ish minutes ( was hungry )
#-------------------------------------------------------------------------

# Importing Python libraries
import pandas as pd
import re

# Reading the document collection
data = pd.read_csv("collection.csv")

# Defining the dictionary used for lemmatization
# --> add your Python code here
lemmas = {
    "homes": "home",
    "sales": "sale",
    "increases": "increase",
    "increasing": "increase",
    "rising": "rise"
}

# Creating the data structure that will store the inverted index
invertedIndex = {}

# Processing each document in the collection
for i, row in data.iterrows():

    docID = row["Document"]
    text = row["Text"]

    # Applying surface-level normalization
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)


    # Tokenizing the document
    tokens = text.split()


    # Applying lemmatization
    for j in range(len(tokens)):
        if tokens[j] in lemmas:
            tokens[j] = lemmas[tokens[j]]


    # Building the inverted index
    for term in tokens:

        if term not in invertedIndex:
            invertedIndex[term] = []

        if docID not in invertedIndex[term]:
            invertedIndex[term].append(docID)


# Printing the inverted index with terms ordered alphabetically
# Expected format:
# term1 : ['Doc1', 'Doc2']
# term2 : ['Doc3']
for term in sorted(invertedIndex):
    print(term, ":", invertedIndex[term])