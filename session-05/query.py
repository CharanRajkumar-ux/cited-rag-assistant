from store import get_collection

collection = get_collection()
print(f"Loaded {collection.count()} documents from disk.\n")


def show(query, k=3, where=None, where_document=None, label=""):
    results = collection.query(
        query_texts=[query],
        n_results=k,
        where=where,
        where_document=where_document,
    )
    print(f"=== {query} {label}===")
    for doc, meta, dist in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        print(f"  {1 - dist:.2f}  [{meta['topic']}] {doc}")
    print()


# Experiment 1: the same vague question, with and without a filter
show("How long does it take?")
show("How long does it take?", where={"topic": "cooking"}, label="(cooking only) ")
show("How long does it take?", where={"topic": "support"}, label="(support only) ")

# Experiment 2: how many results? k = 1, 3 and 10
for k in (1, 3, 10):
    show("Virat Kohli in 2022", k=k, label=f"(k={k}) ")

# Experiment 3: the exact-code problem from Session 4
show("my payment failed with E-4013")
show("my payment failed with E-4013",
     where_document={"$contains": "E-4013"}, label="(must contain E-4013) ")

# Experiment 4: the questions your chatbot got wrong
show("Who won the final of the 2022 Asia Cup?")
show("What is the highest individual score in Test cricket?")