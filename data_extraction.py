import os
import json

from tables import *
from urlparse import urlparse
from file_cache import JSONFileCache
from collections import defaultdict
from sqlalchemy.orm import sessionmaker, joinedload_all

def get_needed_venue_data():
    """
    We're comparing name, URL and twitter handle, so we need to get all the
    venues from the database, and extract this information from the venue cache.
    We'll also return venue_ids and location data as that may be needed later
    """

    # open the database and grab all the venues
    Session = sessionmaker(bind=engine)
    session = Session()
    venues = session.query(Venue).all()

    # access the cache of venue data
    cache = JSONFileCache()

    venues_data = []

    for venue in venues:

        # if the cache file doesn't exist, the venue has been deleted from the Foursquare
        # database and we therefore don't care about it
        if cache.file_exists('%s.json' % venue.foursq_id):
            venue_data = cache.get_json('%s.json' % venue.foursq_id)['response']['venue'] 

            venue_name = venue_data['name']
            venue_url = ''
            venue_twitter = ''
            venue_location = ''
            if venue_data.get('url', False):
                venue_url = urlparse(venue_data['url']).netloc
            if venue_data.get('contact', False):
                if venue_data['contact'].get('twitter', False):
                    venue_twitter = venue_data['contact']['twitter']
            if venue_data['location'].get('lat', False):
                venue_location = '%s,%s' % (venue_data['location']['lat'], venue_data['location']['lng'])

            v = {'foursq_id': venue.foursq_id, 'name': venue_name, 'url': venue_url, 'twitter': venue_twitter, 'location': venue_location}
            venues_data.append(v)

    return venues_data

if __name__ == '__main__':

    # store created data here
    data_dir = os.path.join(os.getcwd(), 'data')

    venues_list = get_needed_venue_data()

    with open(os.path.join(data_dir, 'venue_data_list.json'), 'w') as out_file:
        json.dump(venues_list, out_file)