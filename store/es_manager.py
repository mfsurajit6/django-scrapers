import logging

from decouple import config
from elasticsearch import Elasticsearch, NotFoundError

from store.mapping import mapping


class EsManager:

    def __init__(self):
        self.index_name = config('ELASTICSEARCH_INDEX')
        self.es_client = Elasticsearch(
            [{
                'host': config('ELASTICSEARCH_HOST'),
                'port': config('ELASTICSEARCH_POST')
            }])
        self.mapping = mapping
        logging.info(self.es_client.ping())

    def create_index(self):
        """
        Create an ElasticSearch Index
        """
        self.es_client.indices.create(index=self.index_name, body=self.mapping, ignore=400)

    def populate_index(self, data):
        """
        Populate an index into elasticsearch
        :param data: dict, Data to be populated
        """
        self.es_client.index(index=self.index_name, body=data)

    def delete_data(self, store_type):
        """
        Delete the existing data from elastic search based on store type
        :param store_type: string, Type of store
        """
        query = {
            "size": 10000,
            "query": {
                "match": {"store_type": store_type}
            }
        }
        for res in self.es_client.search(body=query).get("hits").get("hits"):
            try:
                self.es_client.delete(index=self.index_name, doc_type=res["_type"], id=res["_id"])
            except NotFoundError:
                continue
