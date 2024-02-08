from flask import Flask
from flask_restx import Api

from src.ws import production_plan_api

app = Flask(__name__)

api = Api(
    title="GEMS API",
    version="1.0",
    description="""
    API to calculate the power production plan for a variety of power plants 
    based on the given load profile, considering the cost of different energy 
    sources (gas, kerosene), and the minimum and maximum power output of each 
    power plant.
    """,
)
api.add_namespace(production_plan_api)
api.init_app(app)

app.run(port=8888, host="0.0.0.0")
