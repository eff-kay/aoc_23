import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
def compute(data):
    inp = data.split("\n")[:-1]

    max_x = len(inp[0])
    max_y = len(inp)

    num = ''
    numbers = []
    is_isolated = True
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

            if val not in '0123456789' or j == max_x - 1:
                # start the num again
                if num != '' and not is_isolated:
                    try:
                        numbers.append(int(num))
                        print(num)
                    except ValueError:
                        pass

                # reset the num and isolated
                num = ''
                is_isolated = True
            
    return sum(numbers)

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
EXPECTED = 4361

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