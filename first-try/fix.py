#!python3.9

import matplotlib.pyplot as plt
import numpy as np
import math

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

def calc_uncertain_value(delta_y, d):
    a = math.sqrt(np.sum((delta_y - delta_y.mean())*(delta_y - delta_y.mean())))/math.sqrt(4)
    b = 0.1/(2*math.sqrt(3))
    u = math.sqrt(a*a + b*b)
    print(f'uncertain value = {u}')
    return u

def scatter(deltaY, d):
    fig, ax = plt.subplots()

    u = calc_uncertain_value(deltaY, d)

    ax.errorbar(1/d, deltaY, yerr=np.array([u for i in range(4)]), fmt='o')
    ax.set(xlabel='$\\frac{1}{d}$ (mm)', ylabel='Δy (mm)',
        title='The Association bewteen $\\frac{1}{d}$ and Δy')

    plt.xlim((0, 5))
    plt.ylim((0, 5))

    fig.savefig("./graph/test_scatter.png")

def line(delta_y, d):
    fig, ax = plt.subplots()

    frac_d = 1/d
    m = np.sum((frac_d - frac_d.mean())*(delta_y - delta_y.mean()))/np.sum((frac_d - frac_d.mean())*(frac_d - frac_d.mean()))
    b = delta_y.mean() - m * frac_d.mean()
    x, y = np.arange(0, 6), m*np.arange(0, 6)+b
    print(f'm = {m}')
    print(f'b = {b}')

    ax.plot(x, y)
    ax.set(xlabel='$\\frac{1}{d}$ (${mm}^{-1}$)', ylabel='Δy (cm)',
        title='The Association bewteen $\\frac{1}{d}$ and Δy')

    plt.xlim((0, 5))
    plt.ylim((0, 5))

    fig.savefig("./graph/test_line.png")

def main():
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

    scatter(npDeltaY, npD)
    line(npDeltaY, npD)


if __name__ == '__main__':
    main()