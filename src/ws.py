from flask_restx import Namespace, Resource, fields, reqparse, abort
from flask import request, jsonify

from src.production_plan import generate_production_plan
from src.config import *

production_plan_api = Namespace("productionplan", description="Production Planning")


@production_plan_api.route("")
class ProductionPlan(Resource):

    @production_plan_api.doc("")
    def post(self):
        """Production Planning"""
        try:
            data = request.get_json()
            # Validate input
            for key in EXPECTED_PAYLOAD_KEYS:
                if key not in data.keys():
                    abort(400, f"Key {key} is missing from json, payload.")

            # Calculate power production plan
            production_plan = generate_production_plan(payload=data)

            # Generate response
            response = jsonify(production_plan)
            response.status_code = 200
            return response

        except Exception as e:
            abort(500, f"Exception: {str(e)}.")
