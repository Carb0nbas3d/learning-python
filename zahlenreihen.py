import random

results = set()
maxn = 100

for a in range(1,maxn+1):
	for b in range(1, maxn+1):
		r = a*b
		results.add(r)

r2 = list(results)
r2.sort()
print(r2)
print("{} x {}".format(maxn, maxn))
print("number of results", len(r2))
print("percentage of {}: {}%".format(maxn*maxn,
         (len(r2) / (maxn*maxn))*100))
 
