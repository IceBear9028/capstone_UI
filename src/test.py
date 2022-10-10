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
    '3' : [15,16],
    'a' : [7,8,9,10,11,12]
}
g = f['a']
print(f['a'])
print(g)
print(g, g[-1])

f['b'] = 10
print(f)

g = {}
item = 0
for i in range(10):
    g['{0}'.format(i)] = item
    item += 1

print(g)