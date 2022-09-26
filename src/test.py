import datetime

a = datetime.datetime.now()
b = datetime.datetime.now()
c = b - a
d = c.total_seconds()
print(b-a)
print(type(c))
print(d)