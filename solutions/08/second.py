import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import defaultdict
from math import gcd
from copy import deepcopy as copy_list

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

    def find_last_occurrence(input_sequence, mappings):
        keys_ending_with_A = [key for key in mappings.keys() if key[-1] == "A"]
        last_occurrences = {}
        interval_lengths = {}

        for i in range(99999999999999999999999):
            current_values = []
            reached_Z_count = 0

            for key_A in keys_ending_with_A:
                if input_sequence[i % len(input_sequence)] == "R":
                    next_value = mappings[key_A][1]
                else:
                    next_value = mappings[key_A][0]

                current_values.append(next_value)

                if next_value[-1] == "Z":
                    reached_Z_count += 1

                    last_occurrence = last_occurrences.get(key_A, -1)
                    if last_occurrence == -1:
                        last_occurrences[key_A] = i + 1
                    else:
                        interval_lengths[key_A] = (i + 1 - last_occurrence)

            if reached_Z_count == len(current_values):
                return i + 1

            if len(interval_lengths.keys()) == len(current_values):
                lcm = 1
                for interval_length in interval_lengths.values():
                    lcm = lcm * interval_length // gcd(lcm, interval_length)
                return lcm

            keys_ending_with_A = copy_list(current_values)

    a, mappings = parse_input(data)
    result = find_last_occurrence(a, mappings)
    print(result)

INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''

EXPECTED = 5905

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
        # 21003205388413
        print(compute(f.read()))