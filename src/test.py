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