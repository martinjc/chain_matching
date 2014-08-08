import os
import json
import uuid
import math
import operator

from Levenshtein import ratio
from collections import defaultdict
from itertools import combinations

def match_chains(venues_data):

    chain_lookup = defaultdict(str)
    id_lookup = defaultdict(set)

    for i, v1 in enumerate(venues_data):

        print '%d, %s' % (i, v1['name']),

        chain_id = ''

        # have we already found a chain that this venue belongs to?
        if chain_lookup.get(v1['foursq_id'], False):
            chain_id = chain_lookup[v1['foursq_id']]
            id_lookup[chain_id].add(v1['foursq_id'])
            print '\t\t\t\t\t\t\t\t\talready chained'
        # if not, it may be a candidate for a new chain
        else:
            chain_id = chain_id = uuid.uuid4().hex
            id_lookup[chain_id].add(v1['foursq_id'])
            print '\t\t\t\t\t\t\t\t\tsearching'
            for v2 in venues_data[i+1:]:

                if not chain_lookup.get(v2['foursq_id'], False):

                    name_distance = ratio(v1['name'], v2['name'])
                    if v1['url'] or v2['url']:
                        if v1['url'] == v2['url'] and v1['url']:
                            url_distance = 0.5
                        else:
                            url_distance = 0
                    else:
                        url_distance = 0
                    if v1['twitter'] or v2['twitter']:
                        if v1['twitter'] == v2['twitter'] and v1['twitter']:
                            twitter_distance = 0.5
                        else:
                            twitter_distance = 0    
                    else:
                        twitter_distance = 0

                    total_distance = name_distance + url_distance + twitter_distance

                    if total_distance >= 0.9:

                        print "\t%f, %s" % (total_distance, v2['name'])

                        chain_lookup[v2['foursq_id']] = chain_id
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
