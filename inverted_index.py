import math
import json
from collections import defaultdict
from text_proccesing import tokenize

documents = []

# Load documents
with open('file_management/data.json', 'r') as f:
    adobe_info = json.load(f)
documents.extend(adobe_info['document'])

def create_inverted_index(documents):
    inverted_index = defaultdict(lambda: defaultdict(int))
    doc_lengths = {}
    doc_id = 1
    for line in documents:
        tokens = tokenize(line)
        doc_lengths[doc_id] = len(tokens)
        for word in tokens:
            inverted_index[word][doc_id] += 1
        doc_id += 1
    return inverted_index, doc_lengths

def get_tf(inverted_index, doc_lengths):
    tf = defaultdict(dict)
    for word, doc_freq in inverted_index.items():
        for doc_id, freq in doc_freq.items():
            tf[word][doc_id] = freq / doc_lengths[doc_id]
    return tf

def get_idf(inverted_index, num_docs):
    idf = {}
    for word, doc_freq in inverted_index.items():
        idf[word] = math.log(num_docs / len(doc_freq))
    return idf

def get_tf_idf(tf, idf):
    tf_idf = defaultdict(dict)
    for word, doc_freq in tf.items():
        for doc_id, tf_value in doc_freq.items():
            tf_idf[word][doc_id] = tf_value * idf[word]
    return tf_idf

def search(query, tf_idf):
    query_tokens = tokenize(query)
    print(query_tokens)
    scores = {doc_id: 0 for doc_id in range(1, len(documents) + 1)}
    for word in query_tokens:
        if word in tf_idf:
            for doc_id, tf_idf_score in tf_idf[word].items():
                scores[int(doc_id)] += tf_idf_score
    ranked_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ranked_docs




def make_tf_idf(file_path):
    inverted_index, doc_lengths = create_inverted_index(documents)
    tf = get_tf(inverted_index, doc_lengths)
    idf = get_idf(inverted_index, len(documents))
    tf_idf = get_tf_idf(tf, idf)

    print(tf_idf)
        # Write TF-IDF model to a text file

    with open("tf_idf.txt", "w") as f:
        f.write(json.dumps(tf_idf))


tf_idf = {}

file_name= "tf_idf.txt"

#make_tf_idf(file_name)

# Read TF-IDF model from file
with open(file_name, "r") as f:
    tf_idf = json.load(f)

# Example query
query = "courses appear instructor days"
ranked_results = search(query, tf_idf)

# Display results
print("Top 3 Results for", query)
num_results = 5

for i in range(num_results):
    print(documents[ranked_results[i][0]-1])
    print()


