# %%

# Import PyTorch, which provides tensor creation and numerical operations.
import torch

# Read the file as one name per line; splitlines() removes the line separators.
words = open('names.txt', 'r').read().splitlines()

# Map each character pair (bigram) to its total count across all names.
b = {}
for w in words:
    # Boundary markers let the first and last characters form pairs too.
    chs = ["<S>"] + list(w) + ["<E>"]

    # zip() pairs each character with the following one:
    # e.g. ["a", "b", "c"] with ["b", "c"] gives ("a", "b"), ("b", "c").
    for ch1, ch2 in zip(chs, chs[1:]):
        bigram = (ch1, ch2)

        # dict.get() returns the current count, or 0 if this pair is new.
        # Store the incremented count so repeated pairs are accumulated.
        b[bigram] = b.get(bigram, 0) + 1

# b.items() yields (bigram, count) pairs. The key function selects each count;
# negating it makes sorted() place the largest counts first.
# sorted() returns a new list; because this result is not assigned to a name,
# the sorted list is not kept for later use.
sorted(b.items(), key=lambda kv: -kv[1])

# Create a 28-by-28 matrix of integer counts, initially all zero.
# Rows and columns represent characters, including the two boundary markers.
N = torch.zeros((28, 28), dtype=torch.int32)

# Get the distinct characters used in the names, then sort them for a
# consistent character-to-number mapping.
chars = sorted(list(set(''.join(words))))
# Assign each character its position in the sorted list, starting at 0.
stoi = {s: i for i, s in enumerate(chars)}
# Reserve two additional IDs for the start and end markers.
# The character IDs must not reach 26 or 27, which are reserved for these markers.
stoi["<S>"] = 26
stoi["<E>"] = 27

# For every neighboring character pair, add one to its matrix cell.
for w in words:
    # Add boundary markers so the first and last letters are counted too.
    chs = ["<S>"] + list(w) + ["<E>"]
    for ch1, ch2 in zip(chs, chs[1:]):
        # Convert the characters to integer row and column indexes.
        ix1 = stoi[ch1]
        ix2 = stoi[ch2]
        # Count this transition: row ix1 character followed by column ix2 character.
        N[ix1, ix2] += 1
