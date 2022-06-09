#!python3.9

import json
import numpy as np
import matplotlib.pyplot as plt

def empty(x, y):
    pass

def data6(x, y):
    print(x, y)
    x, y = np.array(x), np.array(y)
    left_count, middle_count, right_count = 0, 0, 0
    left, middle, right = 0, 0, 0
    for i in x:
        if i > 25 and i < 60:
            left += i
            left_count += 1

def main():
    procFunctions = {
        'single-slit': [empty for i in range(2)],
        'double-slit': [empty for i in range(9)]
    }
    procFunctions['double-slit'][5] = data6
    data = None
    with open('./data/analysis_data.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    for slit_type in data:
        for i in range(len(data[slit_type])):
            procFunctions[slit_type][i](data[slit_type][i][0], data[slit_type][i][1])

if __name__ == '__main__':
    main()