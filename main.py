# %%
import torch
import matplotlib.pyplot as plt

words = open("names.txt", "r", encoding="utf-8").read().splitlines()

b = {}
for w in words:
    chs = ["<S>"] + list(w) + ["<E>"]
    for ch1, ch2 in zip(chs, chs[1:]):
        bigram = (ch1, ch2)
        b[bigram] = b.get(bigram, 0) + 1

N = torch.zeros((28, 28), dtype=torch.int32)
chars = sorted(list(set("".join(words))))
stoi = {s: i for i, s in enumerate(chars)}
stoi["<S>"] = 26
stoi["<E>"] = 27

for w in words:
    chs = ["<S>"] + list(w) + ["<E>"]
    for ch1, ch2 in zip(chs, chs[1:]):
        ix1 = stoi[ch1]
        ix2 = stoi[ch2]
        N[ix1, ix2] += 1

itos = {i: s for s, i in stoi.items()}

plt.figure(figsize=(16, 16))
plt.imshow(N, cmap="Blues")
for i in range(28):
    for j in range(28):
        chstr = itos[i] + itos[j]
        plt.text(j, i, chstr, ha="center", va="bottom", color="gray")
        plt.text(j, i, str(N[i, j].item()),
                 ha="center", va="top", color="gray")
plt.axis("off")
