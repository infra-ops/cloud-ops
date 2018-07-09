n = int(input("please enter no:"))
r1 = 0

while( n > 0):
    r2 = n % 10
    r1 = (r1*10) + r2
    n  =  n //10

print ("\n reverse no is: %d" %r1)
