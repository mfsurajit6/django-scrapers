mapping = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
    },
    'mappings': {
        'properties': {
            'store_type': {
                'type': 'text'
            },
            'store_name': {
                'type': 'text'
            },
            'store_address': {
                'type': 'text'
            },
            'store_city': {
                'type': 'text'
            },
            'store_state': {
                'type': 'text'
            },
            'store_zip': {
                'type': 'text'
            },
            'store_phone': {
                'type': 'text'
            },
            'store_latitude': {
                'type': 'text'
            },
            'store_longitude': {
                'type': 'text'
            },
            'created_at': {
                'type': 'text'
            }
        }
    }
}
