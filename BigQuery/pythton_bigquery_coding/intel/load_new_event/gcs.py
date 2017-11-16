import re
import os

import datetime
from google.cloud import storage


class GoogleStorageClient:
    def __init__(self):
        self.__get_project_name()
        self.client = storage.Client(self.project_name)

    def get_uri_strings(self, bucket_name, max_date_obj, folder_name):
        return ["gs://" + bucket_name + '/' + item + '*' for item in self.__yield_prefixes_after_date(bucket_name, max_date_obj, folder_name)]

    def __get_project_name(self):
        """get environment variable for project_name'"""
        try:
            self.project_name = os.environ['project_name']
        except KeyError:
            self.project_name = "poc-tier1"

    def __mo_is_older_than_most_recent_date(self, mo, max_date_object):
        """compare date in match object with the most recent date"""
        return self.__mo_to_datetime(mo) > datetime.datetime.strptime(max_date_object, '%Y-%m-%d').date()

    def __mo_to_datetime(self, mo):
        return datetime.datetime(int(mo.group(1)), int(mo.group(2)), int(mo.group(3))).date()

    def __yield_prefixes_after_date(self, bucket_name, max_date_obj, prefix=None):
        """yield all directories created after a given date"""
        iterator = self.client.lookup_bucket(bucket_name).list_blobs(delimiter='/', prefix=prefix)
        list(iterator)  # Necessary to populate iterator.prefixes
        for p in iterator.prefixes:
            match_object = re.match('.+(\d{4})\/(\d{2})\/(\d{2})\/$', p)
            if match_object:
                if self.__mo_is_older_than_most_recent_date(match_object, max_date_obj):
                    yield p
            else:
                for p2 in list(self.__yield_prefixes_after_date(bucket_name, max_date_obj, prefix=p)):
                    yield p2


if __name__ == "__main__":
    print("starting gcs.py")
    client_storage = GoogleStorageClient()
    max_date_object = '2017-10-10'
    for p in client_storage.get_uri_strings("dm-data-cert-poc-tier1", max_date_object, 'meraki/new'):
        print p
