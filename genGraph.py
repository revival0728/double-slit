#!python3.9

import matplotlib.pyplot as plt
import numpy as np
import json

def main():
    data = None
    with open('./data/procData.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    for slit_type in data:
        id = 1
        for i in data[slit_type]:
            x = []
            y = []
            for t in i:
                x.append(t)
                y.append(i[t])
            x = np.array(x)
            y = np.array(y)
            fig, ax = plt.subplots()
            ax.plot(x, y)
            plt.savefig(f"./graph/{slit_type + '_' + str(id)}")
            id += 1

if __name__ == '__main__':
    main()