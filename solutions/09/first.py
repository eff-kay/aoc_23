import pytest
import argparse
import os.path


import re
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
from collections import defaultdict, Counter

def compute(data):
    inp = data.splitlines()
    inps = [list(map(int, x.split())) for x in inp]

    def go_down_until_constant(x:list):

        # take the diff between each number
        second_series = [x[i+1] - x[i] for i in range(len(x)-1) ]
        c = Counter(second_series)

        if len(c)==1:
            # this is a constant series
            # return the value at the input level
            constant = list(c.keys())[0]
            return x[-1]+constant
        else:
            # this is not a constant series
            # and recurse
            return x[-1]+go_down_until_constant(second_series)

    total = 0
    for inp in inps:
        total+=go_down_until_constant(inp)

    return total

INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

EXPECTED = 114

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
        # 211904 43364472
        print(compute(f.read()))