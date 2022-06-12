#!python3.9

import json
import numpy as np
import math
from matplotlib import pyplot as plt

MACHINE_SPEED = 0.0562855   # mm/s

def empty(x: list, y: list) -> None:
    pass

def data(x: list, y: list, id: str, lr: tuple, mr: tuple, rr: tuple) -> float:
    print(f'In data{id}()')
    print(x, y)
    x, y = np.array(x), np.array(y)
    left_count, middle_count, right_count = 0, 0, 0
    left, middle, right = 0, 0, 0
    for i in x:
        if i > lr[0] and i < lr[1]:
            left += i
            left_count += 1
        if i > mr[0] and i < mr[1]:
            middle += i
            middle_count += 1
        if i > rr[0] and i < rr[1]:
            right += i
            right_count += 1
    left /= left_count
    right /= right_count
    middle /= middle_count
    delta_y = (right-left)*MACHINE_SPEED/2
    print(f'left_count: {left_count}, right_count: {right_count}')
    print(f'left: {left}, right: {right}, middle: {middle}, middle-left: {middle-left}, right-middle: {right-middle}')
    print(f'Δy = {delta_y} mm')
    print()

    return delta_y

def data6(x, y) -> float:
    return data(x, y, 6, (25, 60), (70, 130), (140, 180))

def data7(x, y) -> float:
    return data(x, y, 7, (25, 50), (50, 125), (125, 150))

def data8(x, y) -> float:
    return data(x, y, 8, (18, 41), (50, 125), (130, 155))

def data9(x, y) -> float:
    return data(x, y, 9, (1, 30), (35, 100), (100, 120))

def get_available_data(_delta_y: dict, _d: dict) -> tuple:
    delta_y, d = [], []
    for i in range(5, 9):
        delta_y.append(_delta_y['double-slit'][i])
        d.append(_d['double-slit'][i])
    delta_y, d = np.array(delta_y), np.array(d)
    return delta_y, d

def graph_scatter(_delta_y, _d):
    uncertain_value = calc_uncertain_value(_delta_y, _d)
    delta_y, d = get_available_data(_delta_y, _d)
    fig, ax = plt.subplots()
    ax.errorbar(1/d, delta_y, yerr=np.array([uncertain_value for i in range(4)]), fmt='o')
    plt.ylim((0, 5))
    plt.xlim((0, 5))
    plt.xlabel('$\\frac{1}{d}$ (${mm}^{-1}$)')
    plt.ylabel('Δy (mm)')
    plt.title('The Association between Δy and $\\frac{1}{d}$')
    plt.savefig('./graph/final_result_scatter.png')

def graph_line(_delta_y, _d):
    delta_y, d = get_available_data(_delta_y, _d)
    frac_d = 1/d
    m = np.sum((frac_d - frac_d.mean())*(delta_y - delta_y.mean()))/np.sum((frac_d - frac_d.mean())*(frac_d - frac_d.mean()))
    b = delta_y.mean() - m * frac_d.mean()
    x, y = np.arange(0, 6), m*np.arange(0, 6)+b
    print(f'b = {b}')
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.ylim((0, 5))
    plt.xlim((0, 5))
    plt.title('The Association between Δy and $\\frac{1}{d}$')
    plt.xlabel('$\\frac{1}{d}$ (${mm}^{-1}$)')
    plt.ylabel('Δy (mm)')
    plt.savefig('./graph/final_result_line.png')
    print()

def calc_uncertain_value(_delta_y, _d):
    delta_y, d = get_available_data(_delta_y, _d)
    a = math.sqrt(np.sum((delta_y - delta_y.mean())*(delta_y - delta_y.mean())))/math.sqrt(4)
    b = 1/(2*math.sqrt(3))
    u = math.sqrt(a*a + b*b)
    print(f'uncertain value = {u}')
    print()
    return u


def main():
    delta_y = { # mm
        'single-slit': [0 for i in range(2)],
        'double-slit': [0 for i in range(9)]
    }
    d = {   # mm
        'single-slit': [0.15, 0.15],
        'double-slit': [None, None, None, None, None, 0.25, 0.5, 0.75, 1]
    }
    procFunctions = {
        'single-slit': [empty for i in range(2)],
        'double-slit': [empty for i in range(9)]
    }
    procFunctions['double-slit'][5] = data6
    procFunctions['double-slit'][6] = data7
    procFunctions['double-slit'][7] = data8
    procFunctions['double-slit'][8] = data9
    data = None
    with open('./data/analysis_data.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())
    for slit_type in data:
        for i in range(len(data[slit_type])):
            delta_y[slit_type][i] = procFunctions[slit_type][i](data[slit_type][i][0], data[slit_type][i][1])
    graph_scatter(delta_y, d)
    graph_line(delta_y, d)
    

if __name__ == '__main__':
    main()