import ollama
import tiktoken

MODEL = "llama3.2"
PROMPT = "Write a one-sentence opening line for a mystery novel."

# Part 1: how text turns into tokens
enc = tiktoken.get_encoding("cl100k_base")
samples = {
    "short": "Hello, world!",
    "sentence": "Retrieval-augmented generation grounds answers in your own documents.",
    "code": "def add(a, b):\n    return a + b",
}
for name, text in samples.items():
    tokens = enc.encode(text)
    print(f"{name}: {len(text.split())} words -> {len(tokens)} tokens")

# Part 2: same prompt, low vs high temperature
for temp in (0, 1):
    print(f"\n--- temperature {temp} ---")
    for i in range(5):
        reply = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            options={"temperature": temp},
        )
        print(f"{i + 1}. {reply['message']['content'].strip()}")