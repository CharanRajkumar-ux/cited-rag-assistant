import re

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

SENTENCES = [
    "I bought a new car last week.",
    "The automobile needs a service before the long drive.",
    "Electric vehicles are becoming cheaper to run.",
    "My bicycle has a flat tyre.",
    "Java is my favourite programming language.",
    "I don't enjoy writing Java code.",
    "Spring Boot makes it easy to build REST APIs.",
    "Python is popular for data science and machine learning.",
    "Virat Kohli scored a century at the MCG.",
    "The batsman hit three sixes in the final over.",
    "England won the Ashes series.",
    "It is raining heavily in Manchester today.",
    "Bring an umbrella, the forecast says showers.",
    "The sun is shining and it's warm outside.",
    "Add salt and pepper before roasting the vegetables.",
    "This curry recipe uses cumin, turmeric and chilli.",
    "Error code E-4012 means the payment was declined.",
    "Error code E-4013 means the card has expired.",
    "I forgot my password and cannot log in.",
    "Click 'reset credentials' to recover access to your account.",
]

QUERIES = [
    "vehicle maintenance",
    "wet weather",
    "how do I get back into my account",
    "error E-4013",
    "I hate Java",
    "E-4012", 
    "my payment failed with E-4013"
]

# Turn every sentence into a vector of 384 numbers
model = SentenceTransformer(MODEL_NAME)
embeddings = model.encode(SENTENCES, normalize_embeddings=True)


def search(query: str, k: int = 3, min_score: float = 0.3):
    """Semantic search: rank sentences by cosine similarity to the query.

    Returns up to k results, keeping only those scoring min_score or more.
    """
    q = model.encode(query, normalize_embeddings=True)
    scores = embeddings @ q
    best = np.argsort(-scores)[:k]
    return [(float(scores[i]), SENTENCES[i]) for i in best if scores[i] >= min_score]


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9-]+", text.lower()))


def keyword_search(query: str, k: int = 3):
    """Keyword search: rank sentences by how many query words they share."""
    q = words(query)
    scores = [len(q & words(s)) for s in SENTENCES]
    best = np.argsort(scores)[::-1][:k]
    return [(scores[i], SENTENCES[i]) for i in best]


# Part 1: what an embedding looks like
print(f"Each sentence is {embeddings.shape[1]} numbers.")
print(f"First five numbers for sentence 1: {np.round(embeddings[0][:5], 3)}")

# Part 2: which sentences does the model think are closest and furthest apart?
sims = embeddings @ embeddings.T
pairs = [
    (sims[i, j], i, j)
    for i in range(len(SENTENCES))
    for j in range(i + 1, len(SENTENCES))
]
pairs.sort(reverse=True)

print("\nMost similar pairs:")
for score, i, j in pairs[:5]:
    print(f"  {score:.2f}  {SENTENCES[i]}  |  {SENTENCES[j]}")

print("\nLeast similar pairs:")
for score, i, j in pairs[-5:]:
    print(f"  {score:.2f}  {SENTENCES[i]}  |  {SENTENCES[j]}")

# Part 3: meaning vs keywords, side by side
for query in QUERIES:
    print(f"\n=== {query} ===")
    print("Meaning (embeddings):")
    results = search(query)
    if not results:
        print("  (no results scored 0.3 or more)")
    for score, sentence in results:
        print(f"  {score:.2f}  {sentence}")
    print("Keywords:")
    for score, sentence in keyword_search(query):
        print(f"  {score}     {sentence}")