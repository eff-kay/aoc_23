import pytest
import argparse
import os.path


import re
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
def compute(data):
    inp = data.split("\n")[:-1]

    numbers = []

    for row in inp:
        numbers_in_row = re.findall('Card\s+\d+: (.*)', row)
        winning, mine = numbers_in_row[0].split("|")

        winning = [int(x) for x in re.findall('\d+', winning)]
        mine = [int(x) for x in re.findall('\d+', mine)]

        mine_winning = [x for x in mine if x in winning]

        res = 0
        if len(mine_winning) > 0:
            res = 2**(len(mine_winning)-1)

        numbers.append(res)

     
    print(numbers)
    return sum(numbers)

INPUT_S = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''
EXPECTED = 13

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