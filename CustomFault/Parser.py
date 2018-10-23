#! /usr/bin/env python3

import json
class Parser():
    def __init__(self, jsonFile):
        self.jsonFile = jsonFile
        with open(jsonFile, 'r') as f:
            self.attrs = json.load(f)
    def dump(self):
        print(self.attrs)
if __name__ == '__main__':
    parser = ''
    with open('test.json', 'r') as f:
        parser = json.load(f)
    print(parser['LmServer'])

