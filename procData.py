#!python3.9

import json

def main():
    # Read Data
    data = None
    procData = {
        'single-slit': [],
        'double-slit': []
    }

    with open('./data/data-info.json', 'r', encoding='utf8') as f:
        data = json.loads(f.read())

    for slit_type in data:
        for data_info in data[slit_type]:
            procData[slit_type].append({})
            with open(f"./data/{data_info['fileName']}", 'r', encoding='utf8') as f:
                for i in f.readlines():
                    v, t = map(float, i.strip().split())
                    procData[slit_type][-1][t] = v

    with open('./data/procData.json', 'w', encoding='utf8') as f:
        json.dump(procData, f)

if __name__ == '__main__':
    main()