import os
import json

from tables import *
from file_cache import JSONFileCache
from collections import defaultdict
from sqlalchemy.orm import sessionmaker, joinedload_all

def output_chains(id_lookup_list):

    output_data = {}

    for chain_id, venue_list in id_lookup_list:

        output_data['chain_id'] = chain_id
        output_data['venues'] = []

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

        output_data['name'] = max_name.replace(',', '')
        output_data['num_users'] = num_users
        output_data['num_checkins'] = num_checkins
        output_data['unique_users'] = len(unique_users)

    return output_data

if __name__ == '__main__':

    id_lookup_list = json.load(open(os.path.join(data_dir, 'id_lookup.json')))

    output_data = output_chains(id_lookup_list)

    with open(os.path.join(data_dir, 'chains_stats.json'), 'w') as out_file:
        json.dump(output_data, out_file)

