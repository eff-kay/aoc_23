import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import defaultdict

def compute(data):
    inp = data.split("\n")[:-1]
    cards_map = defaultdict(int)
    for i, row in enumerate(inp, 1):
        cards_map[i] += 1
        numbers_in_row = re.findall('Card\s+\d+: (.*)', row)
        winning, mine = numbers_in_row[0].split("|")

        winning = [int(x) for x in re.findall('\d+', winning)]
        mine = [int(x) for x in re.findall('\d+', mine)]

        mine_winning = [x for x in mine if x in winning]

        # fetch the current card instances
        wins_so_far = cards_map[i]
        wins_so_far = 1 if wins_so_far == 0 else wins_so_far
        
        total_wins = len(mine_winning)

        for _ in range(wins_so_far):
            for j in range(i+1, i+1+total_wins):
                cards_map[j] += 1
    return sum(list(cards_map.values()))

INPUT_S = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''

EXPECTED = 30

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