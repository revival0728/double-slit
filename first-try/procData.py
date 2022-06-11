#!python3.9

import matplotlib.pyplot as plt
import numpy as np

def procDeltaY(data):
    ret = []
    for i in data:
        ret.append(sum(i)/len(i))
    return ret

def calcM(x, y):
    s = 0
    for i in range(1, len(x)):
        s += ((y[i]-y[i-1])/(x[i]-x[i-1]))
    return s/(len(x)-1)

def calcB(m, x0, y0):
    return m*(0-x0)+y0

# Data for plotting (mm)
r = 6467.5
d = [0.25, 0.5, 0.75, 1]
deltaYs = [
    (1.69, 1.576, 1.63),
    (0.876, 0.835, 0.83),
    (0.555, 0.53, 0.553),
    (0.41, 0.42)
]

deltaY = procDeltaY(deltaYs)


npD = np.array(d)
npDeltaY = np.array(deltaY)


#Calculate data

m = calcM(npD, 1/npDeltaY)

print(f'm = {m}')
print(f'b = {calcB(m, npD[0], (1/npDeltaY)[0])}')

#Plot

fig, ax = plt.subplots()
ax.plot(1/npD, npDeltaY)

ax.set(xlabel='1/d (mm)', ylabel='delta Y (mm)',
       title='association bewteen 1/d and DeltaY')
ax.grid()

fig.savefig("test.png")
plt.show()