import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import defaultdict
def compute(data):
    inp = data.split("\n")[:-1]

    max_x = len(inp[0])
    max_y = len(inp)

    num = ''
    numbers = []
    numbers_gear_map = defaultdict(list)
    is_isolated = True
    gears = set()
    for i, row in enumerate(inp):
        for j, val in enumerate(row):

            if val in '0123456789':
                num += val

                dy_dx = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0),(1,1)]

                for dy, dx in dy_dx: 
                    i_loc = i + dy
                    j_loc = j + dx

                    if 0 <= i_loc < max_y and 0<= j_loc < max_x:
                        ch = inp[i_loc][j_loc]

                        if ch not in '.0123456789':
                            is_isolated &= False

                        # check if its a gear
                        if ch == '*':
                            gears.add((i_loc, j_loc))

            if val not in '0123456789' or j == max_x - 1:
                # start the num again
                if num != '' and not is_isolated:
                    try:
                        numbers.append(int(num))
                        for loc in gears:
                            numbers_gear_map[loc].append(int(num))

                    except ValueError:
                        pass

                # reset the num and isolated
                gears = set()
                num = ''
                is_isolated = True

    res_gears = []
    for k, v in numbers_gear_map.items():
        if len(v) == 2:
            res_gears.append(v[0] * v[1])

    return sum(res_gears)

INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''

EXPECTED = 467835

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