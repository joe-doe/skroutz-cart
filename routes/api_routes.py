import json
from bson import json_util
from flask_restplus import (
    Resource,
    fields
)
from flask import request


def register_api_routes(api, model):

    class FindBest(Resource):
        def get(self):
            response = model.find_best()
            return json.loads(json_util.dumps(response))

    class Store(Resource):
        request_model = api.model('request_store', {
            'items_url_list': fields.List(fields.String(description='Item URL',
                                                        required=True))
        })

        @api.doc(body=request_model)
        def post(self):
            item = request.get_json()['items_url_list']

            response = model.store(item)
            return response

    api.add_resource(FindBest, '/find_best')
    api.add_resource(Store, '/store')
