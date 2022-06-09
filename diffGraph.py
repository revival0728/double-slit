#!python3.9

from matplotlib import mlab
import numpy as np
from openData import get_procData
from genGraph import gen_graph, gen_scatter
import json

def slice_dict(dt: dict, keys: list, l: int, r: int) -> list:
    ret = []
    for i in range(l, r):
        ret.append(dt[keys[i]])
    return ret

def compare(type: str, l, r, m):
    if type == 'min':
        if l == None:
            l = 1e18
        if r == None:
            r = 1e18
        if (l > m and r > m):
            return True
    if type == 'max':
        if l == None:
            l = -1e18
        if r == None:
            r = -1e18
        if(r < m and l < m):
            return True
    return False

def tolerant(n: float) -> float:
    if abs(n) < 0.1:
        return 0
    return n

def calc_average(arg: list) -> float:
    if len(arg) == 0:
        return 0
    return sum(arg) / len(arg)

def calc_slope(dt: dict, all_time: list, i: int, check_range: int) -> float:
    if (i-1 < 0 or i+1 >= len(all_time)):
        return 0
    m = []
    for j in range(1, check_range):
        if(i-j >= 0 and i+j < len(all_time)):
            m.append((dt[all_time[i+j]]-dt[all_time[i-j]])/(float(all_time[i+j])-float(all_time[i-j])))
        else:
            break
    # l, r = 0, len(m)
    # mid = (l + r) // 2
    # while (tolerant(abs(calc_average(m[l:mid]) - calc_average(m[l:r]))) != 0) and (l < r):
    #     r = mid
    #     mid = (l + r) // 2
    # m = m[l:r]
    return (sum(m)/len(m))


def check_local_max(dt: dict, all_time: list, i: int, check_range: int) -> bool:    # check_range -> s
    # left, right = None, None
    # if(i-check_range >= 0):
    #     left = max(slice_dict(dt, all_time, i-check_range, i-1))
    # if(i+check_range < len(all_time)):
    #     right = max(slice_dict(dt, all_time, i+1, i+check_range))
    # if(compare('max', left, right, dt[all_time[i]])):
    #     return True
    # else:
    #     return False
    if (i-1 < 0 or i+1 >= len(all_time)):
        return False
    mm = calc_slope(dt, all_time, i, check_range)
    ml = calc_slope(dt, all_time, i-1, check_range)
    mr = calc_slope(dt, all_time, i+1, check_range)
    if(abs(mm) < 0.001 and ml > 0 and mr < 0):
        return True
    else:
        return False

def seperate_data(dt: dict) -> tuple:
    x, y = [], []
    for k in dt:
        x.append(k)
        y.append(dt[k])
    return x, y

def main():
    data = get_procData()
    check_range = {
        'single-slit': [5, 5],
        'double-slit': [150, 150, 150, 150, 150, 250, 300, 250, 350]
    }
    analysis_data = {}

    for slit_type in data:
        id = 1
        analysis_data[slit_type] = []
        for dt in data[slit_type]:
            # x, y = map(np.array , seperate_data(dt))
            all_time_float = list(map(float, dt.keys()))
            all_time_float.sort()
            all_time = list(map(str, all_time_float))
            x, y = [], []
            for i in range(1, len(all_time)-1):
                if(check_local_max(dt, all_time, i, check_range[slit_type][id-1])):
                    y.append(dt[all_time[i]])
                    x.append(all_time[i])
            x = list(map(float, x))
            analysis_data[slit_type].append([x, y])
            # local_max = argrelextrema(y, np.greater, order=10)[0]
            # axis_x, axis_y = [], []
            # for i in local_max:
            #     axis_x.append(x[i])
            #     axis_y.append(y[i])
            gen_scatter(f"./graph/diff_{slit_type}_{id}.png", x, y)
            id += 1
    
    with open('./data/analysis_data.json', 'w', encoding='utf8') as f:
        json.dump(analysis_data, f)

if __name__ == '__main__':
    main()