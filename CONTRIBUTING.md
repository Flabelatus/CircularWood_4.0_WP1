# CONTRIBUTING

## Running the Application

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

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
```

## Testing the API

To test the endpoints, Insomnia is used. Here is the download link: https://insomnia.rest/download

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

