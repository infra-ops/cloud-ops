
"""
def prime(n):
    count = 0
    for i in range(1, (n+1)): 
         if n % i == 0: 
             count += 1
    if count > 2:
        print "Not a prime"
    else:
        print "A prime"
"""

"""
def prime(x):
    if x<2:
        return False
    for i in range(2,x):
        if not x%i:
           return False
    return True
"""


n=7
def check(n):
    x = True
    for i in range(2, n):
        if n%i == 0:
            x = False
            break
    if x:
        print("prime")
    else:
        print("not prime")
check(n)          




#for i in range(20):
#    print i, prime(i)

#x = int(raw_input("enter a prime number"))
#print prime(x)



