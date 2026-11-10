# %%

# Import PyTorch for tensor math and numerical operations, and Matplotlib for
# rendering the bigram frequency table as a heat map for visual inspection.
import torch
import matplotlib.pyplot as plt
%matplotlib inline

# Read the dataset as a list of names, one per line. Using splitlines() removes
# the newline characters while preserving the name text itself.
words = open('names.txt', 'r').read().splitlines()

# Count how often each character-to-character transition appears across the
# entire dataset. This produces a frequency table for bigrams, which is the
# simplest form of a character-level language model.
b = {}
for w in words:
    # Add start and end markers so transitions at the beginning and end of each
    # name are also counted; otherwise the first and last letters would never
    # appear in a valid pairwise sequence.
    chs = ["<S>"] + list(w) + ["<E>"]

    # zip() walks neighboring elements in the sequence. For example, the list
    # ["a", "b", "c"] becomes pairs ("a", "b") and ("b", "c").
    for ch1, ch2 in zip(chs, chs[1:]):
        bigram = (ch1, ch2)

        # Dictionary lookups are used to accumulate counts: a new pair starts at
        # 0 and each occurrence adds 1, so the final value reflects frequency.
        b[bigram] = b.get(bigram, 0) + 1

# This line is intentionally not stored: it is just a quick check to inspect the
# most common pairs by sorting frequency in descending order. In a real model,
# we would use these counts directly to build probabilities or sample from them.
sorted(b.items(), key=lambda kv: -kv[1])

# Build a 28 x 28 integer matrix. There are 26 lowercase letters plus two
# reserved boundary tokens, giving one slot for each valid character symbol.
# The matrix cells will store how often each bigram occurs.
N = torch.zeros((28, 28), dtype=torch.int32)

# Enumerate the distinct characters in a deterministic order so every character
# always maps to the same integer index. This makes the matrix stable and easy
# to interpret when visualized.
chars = sorted(list(set(''.join(words))))

# Create the integer encoding for characters. The ordering is based on the
# sorted character list, which keeps the mapping consistent across runs.
stoi = {s: i for i, s in enumerate(chars)}

# Reserve the final two slots for explicit token boundaries, leaving the first
# 26 positions for actual letters. This matches the size of the matrix and lets
# the model treat start/end markers as real tokens rather than invisible ones.
stoi["<S>"] = 26
stoi["<E>"] = 27

# Fill the bigram matrix by scanning every name again and counting transitions
# between adjacent characters, including the boundary markers.
for w in words:
    # Add start and end tokens so the first and last letters also get counted.
    chs = ["<S>"] + list(w) + ["<E>"]
    for ch1, ch2 in zip(chs, chs[1:]):
        # Convert each character to its numeric index and increment the matrix
        # entry for that transition. The row is the current character and the
        # column is the next character.
        ix1 = stoi[ch1]
        ix2 = stoi[ch2]
        N[ix1, ix2] += 1

# Reverse the mapping so we can print labels in the heat map using the original
# characters instead of only the integer IDs.
itos = {i: s for s, i in stoi.items()}

# Render the transition counts as a heat map. Brighter or darker cells highlight
# which character pairs are common; it gives a visual summary of the learned
# character-level statistics.
plt.figure(figsize=(16, 16))
plt.imshow(N, cmap='Blues')
for i in range(28):
    for j in range(28):
        # Display the symbol pair and the corresponding count in each matrix cell.
        chstr = itos[i] + itos[j]
        plt.text(j, i, chstr, ha="center", va="bottom", color="gray")
        plt.text(j, i, N[i, j].item(), ha="center", va="top", color="gray")
plt.axis("off")

# Video timestamp: 20:40 ("The spelled-out intro to language modeling: building makemore")
