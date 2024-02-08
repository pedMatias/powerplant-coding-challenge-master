# powerplant-coding-challenge
![API](static/api.PNG "Flask rest plus api") 
API to calculate how much power each of a multitude of different powerplants need to produce (a.k.a. the production-plan) when the load is given and taking into account the cost of the underlying energy sources (gas, kerosine) and the Pmin and Pmax of each powerplant.

Since the webservice runs Flask Rest X Api, an interface, called swagger, is automatic generated. To access the endpoint access to http://localhost:8888/. 

## Dependencies
- python 3.10;
- Docker;

## Run Locally using venv
### Setup the project
1. Create Virtual environment:
```sh
$ python -m venv .venv
```

2. Activate virtual environment (example for Bash):
```sh
$ source .venv/Scripts/activate
```

3. Install requirements:
```sh
$ pip install -r requirements.txt
```

### Run the API
1. To run the webservice:
```sh
$ python app.py
```

3. Access the swagger running on http://localhost:8888/.

2. Call the POST endpoint running on http://localhost:8888/productionplan.
Example: ``` curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload1.json http://localhost:8888/productionplan ```



## Run using a Docker image
### Setup the project
1. Create docker image:
```sh
$ docker build -t powerplant-gems .
```

### Run the API

1. Run Docker image
```sh
$ docker run --name powerplant-gems -d powerplant-gems
```

2. Access the swagger running on http://localhost:8888/.

3. Call the POST endpoint running on http://localhost:8888/productionplan.
Example: ``` curl -X POST -H "Content-Type: application/json" -d @example_payloads/payload1.json http://localhost:8888/productionplan ```


## Future TODOs:
If I had more time I would:
- Create unittests for the different modules and functions;
- Add CO2 cost;
