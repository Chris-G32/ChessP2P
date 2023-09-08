import collections

data=collections.deque(maxlen=10)


for i in range(15):
    data.append(i)

remove_candidates=[]
for i in data:
    if i ==11:
        remove_candidates.append(i)
    print(i)
for i in remove_candidates:
    data.remove(i)

print(data[2])