import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import defaultdict

def compute(data):
    inp = data.split("\n")[:-1]

    # parse the input
    time = inp[0].split()[1:]
    dist = inp[1].split()[1:]

    time = int(''.join(time))
    dist = int(''.join(dist))

    def dist_travelled(btn_hold, total_time):
        time_to_travel = total_time - btn_hold
        return time_to_travel * btn_hold

    races = []

    # collect options 
    options = []
    for i in range(1, time):
        # print(i, time)
        dt = dist_travelled(i, time)
        if dt > dist:
            options.append(dt)

    races.append(len(options))

    # multiple all numbers in the list
    from functools import reduce
    prod = reduce(lambda x,y: x*y, races) 
    return prod

INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

EXPECTED = 46

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
        print(compute(f.read()))