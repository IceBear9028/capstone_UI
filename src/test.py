import datetime

a = datetime.datetime.now()
b = datetime.datetime.now()
c = b - a
d = c.total_seconds()
print(b-a)
print(type(c))
print(d)
print(type(d))

print(10 ** 6)
e = int(d*(10**6))
print(e)
print(type(e))


f = {
    '1' : [1,2,3,4,5,6,7],
    '2' : [8,9,10,11,12,13,14],
    '3' : [15,16]
}
print(f['1'][len(f['1'])-1])