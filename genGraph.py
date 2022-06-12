#!python3.9

from openData import get_procData
import matplotlib.pyplot as plt
import numpy as np

def gen_graph(fn: str, x: list, y: list) -> None:
    if len(x) == 0:
        x.append(0)
    if len(y) == 0:
        y.append(1)
    x = list(map(float, x))
    x = np.array(x)
    y = np.array(y)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.xlim(0, max(x)+1)
    plt.xlabel('time (s)')
    plt.ylabel('light intensity (V)')
    plt.savefig(fn)

def gen_scatter(fn: str, x: list, y: list) -> None:
    if len(x) == 0:
        x.append(0)
    if len(y) == 0:
        y.append(1)
    x = list(map(float, x))
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    plt.xlabel('time (s)')
    plt.ylabel('light intensity (V)')
    plt.savefig(fn)

def main():
    data = get_procData()

    for slit_type in data:
        id = 1
        for i in data[slit_type]:
            x = []
            y = []
            for t in i:
                x.append(t)
                y.append(i[t])
            gen_graph(f"./graph/{slit_type + '_' + str(id)}", x, y)
            id += 1

if __name__ == '__main__':
    main()