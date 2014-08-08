import os
import json
import uuid
import math

from Levenshtein import ratio
from collections import defaultdict
from itertools import combinations



def match_chains(venues_data):

    chain_lookup = defaultdict(str)
    id_lookup = defaultdict(set)

    for i, v1 in enumerate(venues_data):

        print '%d' % (i)

        for v2 in venues_data[i+1:]:

            name_distance = ratio(v1['name'], v2['name'])
            if v1['url'] or v2['url']:
                url_distance = ratio(v1['url'], v2['url'])
            else:
                url_distance = 0
            if v1['twitter'] or v2['twitter']:
                twitter_distance = ratio(v1['twitter'], v2['twitter'])
            else:
                twitter_distance = 0

            total_distance = name_distance + url_distance + twitter_distance

            if total_distance > 0.9:

                if chain_lookup.get(v1['foursq_id'], False):
                    chain_id = chain_lookup[v1['foursq_id']]
                elif chain_lookup.get(v2['foursq_id'], False):
                    chain_id = chain_lookup[v2['foursq_id']]
                else:
                    chain_id = uuid.uuid4().hex

                chain_lookup[v1['foursq_id']] = chain_id
                chain_lookup[v2['foursq_id']] = chain_id

                id_lookup[chain_id].add(v1['foursq_id'])
                id_lookup[chain_id].add(v2['foursq_id'])

    return chain_lookup, id_lookup


if __name__ == '__main__':

    # store and load data here
    data_dir = os.path.join(os.getcwd(), 'data')

    venues_list = json.load(open(os.path.join(data_dir, 'venue_data_list.json')))

    chain_lookup, id_lookup = match_chains(venues_list)

    with open(os.path.join(data_dir, 'chain_lookup.json'), 'w') as out_file:
        json.dump(chain_lookup, out_file)

    with open(os.path.join(data_dir, 'id_lookup.json'), 'w') as out_file:
        json.dump(id_lookup, out_file)
