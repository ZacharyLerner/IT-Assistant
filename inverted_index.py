import math
import json
from collections import defaultdict
from text_proccesing import tokenize

#loads default documents and model names
documents = {}
current_model_name = None

# runs to check if the documents is loaded, needed for TF_IDF, but only needs to run once per model switch
def check_doc(json_path, model_name):
    global documents, current_model_name
    if model_name not in documents:  # Check if documents for the model are already loaded
        with open(json_path, 'r') as f:
            adobe_info = json.load(f)
        documents[model_name] = adobe_info['document']
        current_model_name = model_name

# Creates an inverted index based on the document, used later for TF_IDF
def create_inverted_index(documents):
    inverted_index = defaultdict(lambda: defaultdict(int))
    doc_lengths = {}
    for doc_id, line in enumerate(documents, start=1):
        tokens = tokenize(line)
        doc_lengths[doc_id] = len(tokens)
        for word in tokens:
            inverted_index[word][doc_id] += 1
    return inverted_index, doc_lengths

# Calculates Term Frequency for items in the Documents
def get_tf(inverted_index, doc_lengths):
    tf = defaultdict(dict)
    for word, doc_freq in inverted_index.items():
        for doc_id, freq in doc_freq.items():
            tf[word][doc_id] = freq / doc_lengths[doc_id]
    return tf

# Calculates the Inverse Document Frequency  for items in the Documents 
def get_idf(inverted_index, num_docs):
    idf = {}
    for word, doc_freq in inverted_index.items():
        idf[word] = math.log(num_docs / len(doc_freq))
    return idf

# Caculates the TF_IDF for all items in the Document
def get_tf_idf(tf, idf):
    tf_idf = defaultdict(dict)
    for word, doc_freq in tf.items():
        for doc_id, tf_value in doc_freq.items():
            tf_idf[word][doc_id] = tf_value * idf[word]
    return tf_idf

# Searched through the TF_IDF and compiles a ranked list of top documents based on the Query
def search(query, tf_idf, documents):
    query_tokens = tokenize(query)
    scores = {doc_id: 0 for doc_id in range(1, len(documents) + 1)}
    for word in query_tokens:
        if word in tf_idf:
            for doc_id, tf_idf_score in tf_idf[word].items():
                scores[int(doc_id)] += tf_idf_score
    ranked_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return ranked_docs

# 
def make_tf_idf(file_name, documents):
    inverted_index, doc_lengths = create_inverted_index(documents)
    tf = get_tf(inverted_index, doc_lengths)
    idf = get_idf(inverted_index, len(documents))
    tf_idf = get_tf_idf(tf, idf)
    # Write TF-IDF model to a text file
    with open(file_name, "w") as f:
        f.write(json.dumps(tf_idf))

def query(query_str, num_results, model_name):
    if model_name == "its":
        json_path = "file_management/itsdata.json"
        model_path = "models/its_tf_idf.txt"
    elif model_name == "tls":
        json_path = "file_management/tlsdata.json"
        model_path = "models/tls_tf_idf.txt"
    else:
        raise ValueError("Invalid model name")

    check_doc(json_path, model_name)

    if current_model_name is None:
        return "No documents loaded."

    try:
        with open(model_path, "r") as f:
            tf_idf = json.load(f)
    except FileNotFoundError:
        return f"Model file not found: {model_path}"
    except json.JSONDecodeError:
        return f"Error decoding JSON from model file: {model_path}"

    ranked_results = search(query_str, tf_idf, documents[model_name])
    results = query_str + "\n"
    results += "Top " + str(num_results) + " Results for " + query_str + "\n"

    for i in range(min(num_results, len(ranked_results))):
        results += "Result " + str(i+1) + "\n"
        results += documents[model_name][ranked_results[i][0] - 1] + "\n"

    return results

# Example usage
"""
make_tf_idf("models/tls_tf_idf.txt", load_documents("file_management/tlsdata.json"))
print(query("sample query", 5, "tls"))
"""
