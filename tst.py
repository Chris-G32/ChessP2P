import math
import time
def bar(a,n):
    k=n
    b=1
    c=a
    twos=0
    count=0
    while k>0:
        if k%2==0:
            k=k/2
            c=c*c
            twos+=1
            # print("even")
            # print(k)
        else:
            k=k-1
            b=b*c
            # print("odd")
            # print(k)
            # notTwos+=1
        
    # print(notTwos)
        count+=1
    return count
# val=(2**512)
# print(val)
# print(6**1000)
results={}
for i in range(1000):
    results[i]=bar(2,i)
# bar(6,N)
greater_log={}
worst_count=0
for key,val in results.items():
    try:
        worst_case=2*(int(math.log2(int(key))))
    except:
        continue
    if val>worst_case:
        greater_log[key]=[val,worst_case]
        print("Greater than upper bound")
    elif val==worst_case:
        worst_count+=1
        print("Worst case")
print(f"Worst case hit count: {worst_count}")
print("Greater log: ")
for key,val in greater_log.items():
    print(f"key: {key}, actual: {val[0]}, worst: {val[1]}")
time.sleep(10)
# print(math.log10(N)**2)
# print(2*math.log2(N))
# print(math.sqrt(N))
# print(bar(2,601))

# print(bar(5,17634))