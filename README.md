# Wood Database REST API

```master``` branch

## This repository contains the work files of API written for the CW4.0 Research project in HVA Robot Lab

For the CW4.0 work package one, the goal was to create a database of residual wood that can store information from the wood.
In order to develop the application, Flask is used. Flask is relatively easy and quick to start framework, but if the goal is
to scale this application up, it's probably better to enable concurrency and for that we can use a different frameworks like 
Fast API or Django. 

### Contact

- Development: Javid Jooshesh j.jooshesh@hva.nl


### Dependencies

For installing the dependencies, please look into the requirements.txt
or run this command in the terminal > ```pip install -r requirements.txt```

### Residual wood REST API

The API resources for wood and tagging of wood. The full documentation of the API endpoints are available at
the swagger-ui accessing is through: http://localhost/api-docs for development server and
https://robotlab-residualwood.onrender.com/api-docs for the production server

### Database

The database is created using SQLAlchemy.
You can find the initiation of the database models in the ```./models/wood.py``` for the wood database
and ```./models/tags.py``` for the created tags that relates to the wood.

The ```./models/wood_tags.py``` is the database table for the many-to-many relationship between tags and wood elements
in
the database. As each wood can have several tags. And each tag can be associated with several woods from the database.

### Schema and Data validation

For the data validation, Marshmallow library is used to create the schemas that would be used.
Each of the API methods check for these schemas.

## Quick Start

In order to run the server for development, you can either download all required libraries and run the `app.py` file or
run the Docker container (which is recommended)

### Running the `app.py` file
If you opt to run the `app.py` file after installing all the requirements, you need to change the end line from `
    return app
` to the following statement: 
```
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
```
this way you make sure that the application is executed and the database is initialized. 


## Running the Application with Docker

Install Docker (You can download and install Docker Desktop)

In order to run this api for development, please create a Docker image and run
the app in the container.

### How to create a docker image

```commandline
docker build --no-cache -t image_name .

```

### How to run the Dockerfile locally

```commandline
docker run -dp 5000:5000 -w /app
 -v "/c/Users/username/directory/project_folder/project_name:/app" image_name

```

### The Dockerfile setup for development

```commandline
FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

```

### The Dockerfile setup for deployment

```commandline
FROM python:3.10
WORKDIR /app

RUN useradd -m -s /bin/bash robotlab
RUN chown -R robotlab:robotlab /app
USER robotlab

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
```

## Testing the API

For testing the API during development, you can use different tools such as Postman
or Insomnia. I used Insomnia. You can find an exported collection of requests inside
the insomnia directory in the project src. Once you installed Insomnia, you can import the collection of the
requests. 

Here is the download link: https://insomnia.rest/download

### Setting up the Insomnia profile

Once you downloaded and run the Insomnia app, now it's time to import the collection of
requests for all the endpoints registered in the API.

There is an exported collection available to get you started.
You can find the JSON file that is basically the collection of the 'HTTP' requests inside the `./insomnia` directory.
You need to import this
JSON file inside the Insomnia to load the API requests collection. After that, you would need to proceed with setting
the
environment variables such as `url`, `access_token` in Insomnia.

You can google and check the documentations of the Insomnia to do it. but basically you would
need to set the environment variables like this as example:

```
{
    "url": "http://localhost:5000",
    "access_token": <The access_token from the JWT>
}
```

## Adding new models

### Creating new model
The database is initiated as 'db' inside `./db.py`. To create and add new database models, use the same db instance. You
can import it in your
model and use the `Model` object from the SQLAlchemy. Please check how the other models are created.
Don't forget to document your code where it's necessary.

Inside `./models/wood.py`
### Example:
```python
from db import db


class WoodModel(db.Model):
    __tablename__ = 'wood'
    
    # Create the primary key ID
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(80))
    length = db.Column(db.Float(precision=2))
    width = db.Column(db.Float(precision=2))
    height = db.Column(db.Float(precision=2))
```

### Adding the Schema
After you create the new model, add the relevant schema for the model in the `schema.py`.
Inside the schema the `flask-marshmallow` library is used (docs can be
found: https://flask-marshmallow.readthedocs.io/en/latest/)

### Example:
```python
from marshmallow import fields, Schema


class WoodSchema(Schema):
    # Dump only, as the ID is not used in the POST Request payload.
    id = fields.Int(dump_only=True)
    
    name = fields.Str()
    length = fields.Float()
    width = fields.Float()
    height = fields.Float()
```

### Migrating the database
After adding the new models (tables) and the schema, now its time to migrate the new database schema.
To do that we use `flask-migrate`. Basically once you want to migrate your db you can type:
```commandline
flask db migrate -m "your migration message"
flask db upgrade
```
To downgrade to previous migration version:
```commandline
flask db downgrade
```

To get more help:
```commandline
flask db --help
```

## Adding new resources

For creating the endpoints for the resource in the API, in this application, the flask views are used. The endpoints
are created as blueprints. 

### Example
To add new `GET` method, to get all the wood entries inside `./resources/wood.py`
```python
from flask_smorest import Blueprint
from flask.views import MethodView

# import wood model
from models import WoodModel

# import wood schema
from schema import WoodSchema

wood_blueprint = Blueprint('Wood Model', 'wood', description='Operations on the wood resource')

@wood_blueprint.route('/wood')
class WoodList(MethodView):
    
    # set the response status code and the schema for the request
    @wood_blueprint.response(200, WoodSchema(many=True))
    def get(self):
        wood = WoodModel.query.all()
        return wood
```

### Example with Protected Route:

```python
from flask_jwt_extended import jwt_required 

@wood_blueprint.route('/wood')
class WoodList(MethodView):
    
    # Now the route requires authentication
    @jwt_required()
    @wood_blueprint.response(200, WoodSchema(many=True))
    def get(self):
        wood = WoodModel.query.all()
        return wood

```
For more documentations on authentication using JWT, check out https://jwt.io/

Then you can add them to the api inside the `app.py`.
```python
from resources.wood import wood_blueprint


def create_app(db_url=None):
    app = Flask(__name__)
    api = Api(app)

    api.register_blueprint(wood_blueprint)

```
created resources to create yours. And don't forget to add the docstrings to your functions.

After that you can immediately add the newly created endpoints and methods in Insomnia to test them. 

