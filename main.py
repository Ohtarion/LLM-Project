# Bigram-Analyse

# First name in names.txt is "emma".

words = open('names.txt', 'r').read().splitlines()
running = True
clock = 0
for w in words[:1]:
    for ch1, ch2 in zip(w, w[1:]):
        print(ch1, ch2)

grade_list = []

for i in range(100):
    grade_list.append(i)

open("grades.txt", "w").write(str(grade_list))
