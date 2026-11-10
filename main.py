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

# b.items() yields (bigram, count) pairs; sort them by count, largest first.
# Each kv is one such pair, so kv[1] is the count; negating it makes sorted()
# order the counts descending while keeping each bigram attached to its count.
for bigram, count in sorted(b.items(), key=lambda kv: -kv[1]):
    print(bigram, ":", count)
