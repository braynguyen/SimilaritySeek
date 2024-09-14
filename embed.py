import os

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


# def graph
# # Encode sentences to get embeddings
# embeddings = model.encode(sentences)
#
# # Print the shape of the embeddings
# print(embeddings)
#
# def cosine_similarity(embedding1, embedding2):
#     return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
#
# adjacency = np.array([[cosine_similarity(embeddings[i], embeddings[j]) for j in range(5)] for i in range(5)])
# print(adjacency)
