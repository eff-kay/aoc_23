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
    print(seed_to_soil)

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
    print(seeds)
    for seed in seeds:
        def apply_range(key_val, map):
            for (dst, src, val) in map:
                print(dst, src, val, key_val)
                if src<=key_val<src+val:
                    key_val = dst+key_val-src
                    print(key_val)
                    break
                else:
                    key_val = key_val
                
            return key_val
        soil = apply_range(seed, seed_to_soil)

        fert = apply_range(soil, soil_to_fert)
        # wat = wat_map[fert]
        wat = apply_range(fert, fert_to_wat)
        # light = limap[wat]
        # print(light)
        light = apply_range(wat, wat_to_light)
        # temp = tmap[light]
        temp = apply_range(light, li_to_temp)
        # print(temp)
        # hum = hmap[temp]
        hum = apply_range(temp, temp_to_humid)
        loc = apply_range(hum, humid_to_loc)

        print(seed, soil, fert, wat, light, temp, hum, loc)
        numbers.append(loc)

    return min(numbers)

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
EXPECTED = 35

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