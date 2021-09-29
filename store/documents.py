from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from store.models import Store, StoreType

@registry.register_document
class StoreDocument(Document):
    store_type = fields.ObjectField(properties={
        'store_type': fields.TextField(),
    })

    class Index:
        name = 'stores'

    settings = {
        'number_of_shards':1,
        'number_of_replicas':0
    }

    class Django:
        model = Store

        fields = [
            'store_name', 'store_address', 'store_city', 'store_state', 
            'store_zip', 'store_phone', 'store_latitude', 'store_longitude',
        ]
        related_models = [StoreType, ]