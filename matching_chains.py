import os
import json

from Levenshtein import ratio
from collections import defaultdict
from itertools import combinations



def match_chains(venues_data):

    chain_lookup = defaultdict(str)
    id_lookup = defaultdict(set)

    combos = combinations(venues_data, 2)
    print dir(combos)

if __name__ == '__main__':

    # store and load data here
    data_dir = os.path.join(os.getcwd(), 'data')

    venues_list = json.load(os.path.join(data_dir, 'venue_data_list.json'))

    match_chains(venues_list)

