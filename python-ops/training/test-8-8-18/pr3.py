n=7
i=2
c=0

while (i < n/2):
    if n%i == 0:
        c=1
        break
    i=i+1
if c == 0:
    print("prime")
else:
    print("na")
