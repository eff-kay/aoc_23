import pytest
import argparse
import os.path


import re
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
from collections import defaultdict

def compute(data):
    inp = data.split("\n")[:-1]

    # parse the input
    time = list(map(int, inp[0].split()[1:]))
    dist = list(map(int, inp[1].split()[1:]))

    def dist_travelled(btn_hold, total_time):
        time_to_travel = total_time - btn_hold
        return time_to_travel * btn_hold

    races = []

    for time, dist in zip(time, dist):
        # collect options 
        options = []
        for i in range(1, time):
            # print(i, time)
            dt = dist_travelled(i, time)
            print(dt)
            if dt > dist:
                options.append(dt)
        print(len(options)) 
        races.append(len(options))

    # multiple all numbers in the list
    from functools import reduce
    prod = reduce(lambda x,y: x*y, races) 
    return prod

INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 288

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