q1.What is a token, and roughly how many tokens are 1,000 English words?
a1.Token is a chunk of a text, either a whole part, or a part of the word, or any punctuation in english, 1000 english words would be rougly 1300-1400 tokens, which is 3/4 th of a word

q2. What does the context window limit, and what happens when you exceed it?
a2. Context window is the max number of tokens the model can consider at once, if exceeded the model fails with an error

q3.Why does temperature 0 give more repeatable answers?
a3. Because the model almost always picks the most likely token in temp 0.

q4. Name two causes of hallucination.
a4. the model tendency to give any answer rather that to not give one and the questions past its cutoff.

q5. Why can’t an LLM answer questions about your company’s internal documents out of the box?
a5. LLM is trained on the data it's fed on and most likely company's internal documents are very confidential and are not exposed in any kind of training data