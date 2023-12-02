import pytest
import argparse
import os.path

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(data):
    inp = data.split("\n")[:-1]
    ret = None
    game_values = []
    RED, GREEN, BLUE = 12, 13, 14

    for i, row in enumerate(inp, 1):
        sets = row.split(": ")[1].split("; ")
        sets = [[x.split(' ') for x in s.split(', ')] for s in sets]
        game_values.append([i,sets])

    ret = set()
    for i, games in game_values:
        for game in games:
            for draw in game:
                if (draw[1] == 'red' and int(draw[0]) > RED) or (draw[1]=='green' and int(draw[0]) > GREEN) or (draw[1]=='blue' and int(draw[0]) > BLUE):
                    ret.add(i)

    ret = [x for x in range(1, len(inp)+1) if x not in ret]
    return sum(ret)

INPUT_S = '''\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
EXPECTED = 8

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