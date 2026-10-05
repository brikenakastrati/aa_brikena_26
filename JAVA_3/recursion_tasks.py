def m1(a):
    if len(a) <= 1:
        return len(a)
    mid = len(a) >> 1
    return m1(a[:mid]) + m1(a[mid:]) + 1

print(m1([1, 2, 3, 4, 5, 6, 7, 8])) #call it with an array of length 8
#this function returns: 15 
#this function makes 15 calls


#second function
def m2(n):
    if n == 0:
        return 1
    return n - mm(m2(n - 1))

def mm(n):
    if n == 0:
        return 0
    return n - m2(mm(n - 1))

print(m2(20)) #call it for m2=20

#it prints: 13
#m2 is called 814 times
#mm is called 813 times, so it total it makes 1,627 calls


def m3(n):
    if n <= 1:
        return 1
    return m3(n - 1) + m3(n - 1)

print(m3(20))
#call it for m3=20
#it prints: 524288
#it makes 1,048,575 calls