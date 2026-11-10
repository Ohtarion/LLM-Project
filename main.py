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

# Create a 2D PyTorch tensor containing 3 rows and 5 columns of zeros.
# dtype=torch.int32 means each value is stored as a 32-bit integer.
N = torch.zeros((28, 28), dtype=torch.int32)

chars = sorted(list(set(''.join(words))))
stoi = {s: i for i, s in enumerate(chars)}
stoi["<S>"] = 26
stoi["<E>"] = 27


for w in words:
    chs = ["<S>"] + list(w) + ["<E>"]
    for ch1, ch2 in zip(chs, chs[1:]):
        ix1 = stoi[ch1]
        ix2 = stoi[ch2]
        N[ix1, ix2] += 1
