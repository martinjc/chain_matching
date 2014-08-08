import os
import json

from tables import *
from file_cache import JSONFileCache
from collections import defaultdict
from sqlalchemy.orm import sessionmaker, joinedload_all

# store and load data here
data_dir = os.path.join(os.getcwd(), 'data')
chains_dir = os.path.join(data_dir, 'chains')

def output_chains(id_lookup_list):

    output_data = {}

    with(open(os.path.join(chains_dir, 'chains_list.json')) as out_file:
        json.dump(id_lookup_list.iterkeys(), out_file)    

    for chain_id, venue_list in id_lookup_list.iteritems():

        chain_data = {}
        chain_data['venues'] = venue_list

        num_users = 0
        unique_users = set()
        num_checkins = 0

        venue_names = defaultdict(int)

        for venue in venue_list:

            venue = session.query(Venue).filter(Venue.foursq_id == v['foursq_id']).all()[0]
            visits = session.query(Venuesvisited).filter(Venuesvisited.venue == venue).all()

            num_users += len(visits)
            
            for visit in visits:

                num_checkins += visit.num_visits
                unique_users.add(visit.foursquser.id)

            venue_names[venue['name']] += 1

        name_count = 0
        max_name = ''
        for name, count in venue_names.iteritems():
            if count > name_count:
                max_name = name

        chain_data['name'] = max_name.replace(',', '')
        chain_data['num_users'] = num_users
        chain_data['num_checkins'] = num_checkins
        chain_data['unique_users'] = len(unique_users)

        with(open(os.path.join(chains_dir, '%s.json' % chain_id)) as out_file:
            json.dump(chain_data, out_file)

        output_data['chain_id'] = chain_data

    return output_data

if __name__ == '__main__':

    id_lookup_list = json.load(open(os.path.join(data_dir, 'id_lookup.json')))

    output_data = output_chains(id_lookup_list)

    with open(os.path.join(data_dir, 'chains_stats.json'), 'w') as out_file:
        json.dump(output_data, out_file)

    with open(os.path.join(data_dir, 'chains_stats.csv'), 'w') as out_file:
        for chain, data in output_data.iteritems():
            out_file.write('%s,%s,%d,%d,%d,%d\n' % (chain, data['name'], len(data['venues']), data['num_users'], data['num_checkins'], data['unique_users']))


