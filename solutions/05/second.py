import pytest
import argparse
import os.path
import re


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from collections import defaultdict

def compute(data):
    inp = data.split("\n")[:-1]

    seeds = [int(x) for x in re.findall(r"seeds: ([\d ]+)$", inp[0])[0].split()]
    others = data.split("\n\n")[1:]

    seed_to_soil = re.findall(r"^seed-to-soil map:\n([\d \n]+)", others[0], re.MULTILINE)[0].split("\n")

    seed_to_soil = [[int(x) for x in row.split()] for row in seed_to_soil]
    seed_to_soil = sorted(seed_to_soil, key=lambda x: x[1])
    
    soil_to_fert = re.findall(r"^soil-to-fertilizer map:\n([\d \n]+)?", others[1], re.MULTILINE)[0].split("\n")
    soil_to_fert = [[int(x) for x in row.split()] for row in soil_to_fert]
    soil_to_fert = sorted(soil_to_fert, key=lambda x: x[1])

    fert_to_wat = re.findall(r"^fertilizer-to-water map:\n([\d \n]+)?", others[2], re.MULTILINE)[0].split("\n")
    fert_to_wat = [[int(x) for x in row.split()] for row in fert_to_wat]
    fert_to_wat = sorted(fert_to_wat, key=lambda x: x[1])


    wat_to_light = re.findall(r"^water-to-light map:\n([\d \n]+)?", others[3], re.MULTILINE)[0].split("\n")

    wat_to_light = [[int(x) for x in row.split()] for row in wat_to_light]
    wat_to_light = sorted(wat_to_light, key=lambda x: x[1])

    li_to_temp = re.findall(r"^light-to-temperature map:\n([\d \n]+)?", others[4], re.MULTILINE)[0].split("\n")

    li_to_temp = [[int(x) for x in row.split()] for row in li_to_temp]
    li_to_temp = sorted(li_to_temp, key=lambda x: x[1])


    temp_to_humid = re.findall(r"^temperature-to-humidity map:\n([\d \n]+)?", others[5], re.MULTILINE)[0].split("\n")

    temp_to_humid = [[int(x) for x in row.split()] for row in temp_to_humid]

    temp_to_humid = sorted(temp_to_humid, key=lambda x: x[1])


    humid_to_loc = re.findall(r"^humidity-to-location map:\n([\d \n]+)?\n", others[6], re.MULTILINE)[0].split("\n")
    humid_to_loc = [[int(x) for x in row.split()] for row in humid_to_loc]

    humid_to_loc = sorted(humid_to_loc, key=lambda x: x[1])


    numbers = []


    def apply_range_on_lines(R, lines):
        intersect = []
        for line in lines:
            dest, src , sz = line
            range_end = src+sz
            non_intersect = []
            while R:
                (st,ed) = R.pop()
                # (src,sz) might cut (st,ed)
                before = (st,min(ed,src))
                inter = (max(st, src), min(src+sz, ed))
                after = (max(range_end, st), ed)
                if before[1]>before[0]:
                    non_intersect.append(before)
                if inter[1]>inter[0]:
                    intersect.append((inter[0]-src+dest, inter[1]-src+dest))
                if after[1]>after[0]:
                    non_intersect.append(after)

            R = non_intersect
        return intersect+R

    for s_loc in range(0, len(seeds), 2):
        st, ran = seeds[s_loc], seeds[s_loc+1]
        # seed_ranges.add(range(st, st+ran))
        R = [(st, st+ran)]
        R = apply_range_on_lines(R, seed_to_soil)
        R = apply_range_on_lines(R, soil_to_fert)
        R = apply_range_on_lines(R, fert_to_wat)
        R = apply_range_on_lines(R, wat_to_light)
        R = apply_range_on_lines(R, li_to_temp)
        R = apply_range_on_lines(R, temp_to_humid)
        R = apply_range_on_lines(R, humid_to_loc)

        print(R)
        numbers.append(min(R)[0])

    return min(numbers)+1

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