import ollama

MODEL = "llama3.2"
SYSTEM = "You are a helpful, concise assistant.If you’re not sure of a fact, say so instead of guessing numbers."


def new_history():
    return [{"role": "system", "content": SYSTEM}]


def ask(messages):
    """The only function that talks to the model. Swap providers here."""
    stream = ollama.chat(model=MODEL, messages=messages, stream=True,
                         options={"temperature": 1})
    reply, usage = "", None
    for chunk in stream:
        piece = chunk["message"]["content"]
        print(piece, end="", flush=True)
        reply += piece
        if chunk.get("done"):
            usage = (chunk.get("prompt_eval_count"), chunk.get("eval_count"))
    print()
    return reply, usage


history = new_history()
print("Chat with Llama. Type /reset to clear, /quit to exit.")

while True:
    user = input("\nYou: ").strip()
    if user == "/quit":
        break
    if user == "/reset":
        history = new_history()
        print("(history cleared)")
        continue
    if not user:
        continue

    history.append({"role": "user", "content": user})
    print("Bot: ", end="")
    reply, (tokens_in, tokens_out) = ask(history)
    history.append({"role": "assistant", "content": reply})
    print(f"(tokens in: {tokens_in}, out: {tokens_out}, messages: {len(history)})")