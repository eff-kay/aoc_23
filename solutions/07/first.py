import pytest
import argparse
import os.path


import re
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
from collections import defaultdict, Counter

def compute(data):
    inp = data.split("\n")[:-1]
    card_ranks = "23456789TJQKA"

    # determine card type
    highest_rank = len(inp) - 1

    types_of_cars_per_rank = {'high_card': 0, 'one_pair':1, 'two_pair':2, 'three':3, 'full_house': 4, 'four': 5, 'five': 6}

    # determine card type

    hand_type_to_rank = defaultdict(list)
    from collections import Counter
    for hand in inp:
        cards, bid = hand.split(" ")

        # determine if its a high card, no pairs
        c = Counter(cards)
        if len(c)==1:
            hand_type_to_rank['five'].append((cards, bid))

        elif len(c)==2 and max(c.values())==4:
            hand_type_to_rank['four'].append((cards, bid))

        elif len(c)==2 and max(c.values())==3:
            hand_type_to_rank['full_house'].append((cards, bid))

        elif len(c)==3 and max(c.values())==3:
            hand_type_to_rank['three'].append((cards, bid))
        
        elif len(c)==3:
            hand_type_to_rank['two_pair'].append((cards, bid))

        elif len(c)==4:
            hand_type_to_rank['one_pair'].append((cards, bid))

        elif len(c)==5:
            hand_type_to_rank['high_card'].append((cards, bid))
        
    hand_type_to_rank = dict(sorted(hand_type_to_rank.items(), key=lambda x: types_of_cars_per_rank[x[0]]))
    print(hand_type_to_rank)
    total = 0
    rank = 1
    for i, (t, v) in enumerate(hand_type_to_rank.items()):
        v = sorted(v, key=lambda x: [card_ranks.index(c) for c in x[0]]) 

        for j, (cards, bid) in enumerate(v):
            hand_type_to_rank[t][j] = (cards, bid)
            total += int(bid) * rank
            rank+=1

    print(total, hand_type_to_rank)
    return total

INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440

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
        # 211904 43364472
        print(compute(f.read()))