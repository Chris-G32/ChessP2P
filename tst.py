import collections
import json

data=collections.deque(maxlen=10)
class tmp:
    def __init__(self):
        self.a='g'
        self.b='h'
a=tmp()
a_dict=a.__dict__
s=json.dumps(a_dict)
print(s)
# for i in range(15):
#     data.append(i)

# remove_candidates=[]
# for i in data:
#     if i ==11:
#         remove_candidates.append(i)
#     print(i)
# for i in remove_candidates:
#     data.remove(i)

# print(data[2])