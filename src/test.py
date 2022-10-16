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
    'a' : [7,8,9,10,11,12],
    'c' : {'x':True, 'y':True, 'z':True},
    'd' : {'x':{'1':{'_1':False, '__2':'a'},'2':{'_1':False, '__2':'a'},'3':{'_1':False, '__2':'a'}}}
}
g = f['a']
print(f['d']['x'].values())
print(f['a'])
print(g)
print(g, g[-1])
print(f['c']['x'])


f['b'] = 10
print(f)
print(f['d']['x'].get('__1'))
g = {}
item = 0
for i in range(10):
    g['{0}'.format(i)] = item
    item += 1
print(range(10))

print(g)

n = 10
for i in range(10):
    print('i = {0}'.format(i))
    for j in range(i*n, 2*(i+1)*n):
        print(j)

print(int(10/3))


import numpy as np

nu = np.array([])
for i in range(10):
    nu = np.insert(nu,0,int(i))

print(nu)
print(str(np.mean(nu)),np.mean(nu))
if np.mean(nu) < 10:
    print('맞음')




