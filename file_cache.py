import os
import json


class JSONFileCache(object):

    def __init__(self):

        # directory for plots
        self.cache_dir = '/Users/martin/Dropbox/Work/Research/[R] - Fellowship/Venue Updates/cache'
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

    def file_exists(self, file_id):
        return os.path.isfile(os.path.join(self.cache_dir, file_id))

    def get_json(self, file_id):
        assert self.file_exists(file_id)

        with open(os.path.join(self.cache_dir, file_id), "r") as infile:
            return json.load(infile)


    def put_json(self, json_data, file_id):

        with open(os.path.join(self.cache_dir, file_id), "w") as outfile:
            json.dump(json_data, outfile)

