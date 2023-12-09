import pytest
import argparse
import os.path


import re
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
from collections import defaultdict, Counter

def compute(data):
    def parse_input(input_data):
        lines = input_data.split("\n\n")
        a, b = lines
        mappings = {}
        for line in b.splitlines():
            key, value = line.split(" = ")
            value = value.replace("(", "").replace(")", "").split(", ")
            mappings[key] = (value[0], value[1])
        return a, mappings

    def find_value(a, mappings):
        g = "AAA"
        for i in range(99999999):
            if a[i % len(a)] == "R":
                g = mappings[g][1]
            else:
                g = mappings[g][0]

            if g == "ZZZ":
                return i + 1

    a, mappings = parse_input(data)
    result = find_value(a, mappings)
    print(result)

INPUT_S = '''\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''
EXPECTED = 6440

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        # 19631
        print(compute(f.read()))