import json
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import sys
import json
import os

import endpoint_api
from flask import request

app = Flask(__name__)
api = Api(app)

class Sensor_list(Resource):
    def get(self, data_group):
        print(data_group)
        return endpoint_api.get_sensors_list(data_group)


class Data_group_list(Resource):
    def get(self):
        return endpoint_api.get_datagroups()


class Query_group(Resource):
    def get(self, user_submission):
        print(user_submission)
        parsed_input = user_submission.split('|')
        return endpoint_api.query_database(parsed_input[0], parsed_input[1], parsed_input[2])


api.add_resource(Sensor_list, "/sensors/<string:data_group>")
api.add_resource(Data_group_list, "/data-groups/")
api.add_resource(Query_group, "/query/<string:user_submission>")
if __name__ == '__main__':
    app.run(debug=True)
