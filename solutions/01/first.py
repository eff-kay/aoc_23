import pytest
import argparse
import os.path


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split("\n")[:-1]

    total = 0
    for word in inp:
        print(inp)
        nu = ''
        for x in word:
            if x in '123456789':
                nu+=x

        print(nu)
        if len(nu)>1:
            nu = nu[0] + nu[-1]
        else:
            nu = nu[0] + nu[0]

        nu = int(nu)
        print(nu)

        total+=nu


    return total

INPUT_S = '''\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''
EXPECTED = 142

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