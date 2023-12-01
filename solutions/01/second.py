import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split("\n")[:-1]

    total = 0

    for word in inp:
        nu = ''

        location_nu = []
        for y in '0123456789':
            if y in word:
                last_loc = 0
                for i in range(word.count(y)):
                    last_loc = word.index(y, last_loc)
                    last_loc+=1
                    location_nu.append((y, last_loc))

        numbers_map = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6','seven':'7', 'eight':'8', 'nine':'9'}

        for x in ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']:
            if x in word:
                last_loc = 0
                for i in range(word.count(x)):
                    last_loc = word.index(x, last_loc)
                    last_loc+=1
                    location_nu.append((numbers_map[x], last_loc))

        # sort by indx
        location_nu.sort(key=lambda x: x[1])

        if len(location_nu)>1:
            nu = location_nu[0][0] + location_nu[-1][0]
        else:
            nu = location_nu[0][0] + location_nu[0][0]
        
        nu = int(nu)
        total+=nu

    return total

INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''

EXPECTED = 281

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