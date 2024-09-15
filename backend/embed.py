import os
import json

import torch
import numpy as np
from sentence_transformers import SentenceTransformer


# Load a pre-trained sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Sentences to encode
s1 = [
    "I go to school with my dad",
    "I go to school on foot",
    "I go to school by bus",
    "pancakes",
    "strawberries"
]

s2 = [
    "I go to school with my dad",
    "I go to school on foot",
    "I go to school by bus",
    "pancakes",
    "strawberries in a school"
]


def embed(sentences):
    # Encode sentences to get embeddings
    embeddings = model.encode(sentences)

    # Print the shape of the embeddings
    print(embeddings.shape)
    return embeddings


def graph(sentences, filename='graph.json'):
    # Encode sentences to get embeddings
    embeddings = model.encode(sentences)

    # Print the shape of the embeddings
    print(embeddings)

    def cosine_similarity(embedding1, embedding2):
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

    data = {
        'nodes': list(map(lambda x: {'id': x}, sentences)),
        'links': list({'source': sentences[i], 'target': sentences[j], 'value': cosine_similarity(embeddings[i], embeddings[j])} for i in range(5) for j in range(i+1,5))
    }

    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return super(MyEncoder, self).default(obj)
    with open(filename, 'w') as file:
        json.dump(data, file, cls=MyEncoder)

graph(s1, 'graph1.json')
graph(s2, 'graph2.json')