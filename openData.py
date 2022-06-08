#!python3.9

import json

def get_procData() -> dict:
    data = None
    with open('./data/procData.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data