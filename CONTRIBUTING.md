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

### Making a commit
To maintain a clean and readable git history, we follow the Conventional Commits format. Please use the following structure for your commit messages:

#### Format

`<type>(<scope>): <subject>`
type: Indicates the type of change. Use one of the following:

feat: New feature
fix: Bug fix
docs: Documentation changes
style: Code style changes (formatting, etc.)
refactor: Code changes without fixing bugs or adding part_file_path
test: Adding or updating tests
chore: Other changes that don't modify src or test files
scope: (Optional) The area of the code affected (e.g., parser, api).

subject: A brief description of the change in imperative, present tense (e.g., "add feature", "fix bug").

#### Examples

feat(parser): add ability to parse arrays
fix(api): handle null response correctly
docs(readme): update installation instructions
References
If your commit closes an issue, include it in the message footer:

`Closes #123`

Following these guidelines helps us keep a consistent and useful commit history. Thank you for your contributions!

Example: `git commit -m "feat(parser): add ability to parse arrays" -m "The parser can now handle arrays. This change allows us to process data correctly from our API." -m "Closes #345"
`

### Before pushing the commit
The database application is hosted on a web service provided by render.com. To make sure we dont lose the data on this server, the data.db file inside the ./instance directory is 
also tracked by git. And we should save a backup of the database on the render.com to the repository directory before pushing the commits. Reason being, that we dont have super user access to the render server and the service also implements a CI/CD pipeline that makes it convenient to backup the database this way. There is a shell script inside the applications root directory `db-backup.sh` to execute before pushing the commit. 

If you look into the backup script, you will see that it not only copies the data.db contents but also the images from the static directory from the render to your local repository. This is not a reliable way of handling this challenge but until an alternative solution is in place, we follow this proceadure. 


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

# Import the Data Model Interface
from models.interface_model import DataModelInterface


# Each data model needs to inherit from the db.Model and the DataModelInterface 
class WoodModel(db.Model, DataModelInterface):
    # Choose the table name in the database
    __tablename__ = 'wood'
    
    # Create the primary key ID
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(80))
    length = db.Column(db.Float(precision=2))
    width = db.Column(db.Float(precision=2))
    height = db.Column(db.Float(precision=2))
    created_at = db.Column(db.String)

    # Add the partial fields
    # Partial fields would be excluded from certain methods by choice for example
    # the 'id', or 'created_at' needs to be excluded from the PATCH method when updating the the row
    # Therefore, 'id' and 'created_at' field would be in the list of partial fields

    @property
    def partials(self):
        partials = (
            [
                "id",
                "created_at"
            ],
        )
        return self._get_status_fields(partials[0])

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
    created_at = fields.Str()

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

# Create the bluprint
wood_blueprint = Blueprint('Wood Model', 'wood', description='Operations on the wood resource')


# Add the route to the blueprint
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

# Additionally import the jwt_required from the flask_jwt_extended
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

After this step, add the created routes inside the `Resources` class, in the `./resources/routes.py`. There are different categories of endpoints based on its functionality. The `crud` field is for general CRUD operations. If you have other methods, feel free to add them. There is an example of `function_handler` field added in the following snippet for the reservation handling.


```python

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import *


class Resources:
    
    __routes__ = {
        
        # Your model name
        "wood": {

            # The endpoint topic for general CRUD
            "crud": {
                "endpoints": [
                    "/wood",             
                ]
            },

            # The endpoints for specific functionaility from API
            "function_handler": {
                "endpoints": [
                    "/wood/reserve/<int:wood_id>",
                    "/wood/unreserve/<int:wood_id>"
                ]
            },

            # Table name from the data model
            "tablename": WoodModel.__tablename__
        },
    }
```

Then you can add them to the api inside the `app.py`.
```python
# Import the new created resource and data model
from resources.wood import wood_blueprint
from models import WoodModel


# Inside the function where the app is created register the blueprint
def create_app(db_url=None):
    app = Flask(__name__)
    api = Api(app)

    # Ensure to add the model specific function and endpoint to fetch the modifiable fields
    @app.route('/wood/modifiable-fields')
    def get_wood_model_modifiable_fields():
        modifiable_fields = get_modifiable_fields(WoodModel)
        return jsonify(modifiable_fields=modifiable_fields)


    # Register the blueprint
    api.register_blueprint(wood_blueprint)

```
created resources to create yours. And don't forget to add the docstrings to your functions.

After that you can immediately add the newly created endpoints and methods in Insomnia to test them. 

## Document your newly created data model and resources

Add the docstrings to the functions

#### Generate the Documentation using Sphinx

Generate the new html documentation from the newly added modules using the Sphinx library. But before running the 
Make file to generate the documentations, check the `conf.py` file inside the `./docs` directory.
```bash
cd ./docs
```
You need to manually exclude certain fields from the model and resources you added from the documentation.
for that you would need to add the following adjustments:

```python

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import models

excluded_fields = []

# Fetch attribute names for all models
wood_attr_names = dir(models.WoodModel)

# Just after the `exclude_fields` function, add the following line
excl_wood_attr = exclude_fields(wood_attr_names)

# Then add your excluded_wood_attr to the list of `excluded_fields`
excluded_fields = (
    excl_wood_attr + 
)

```

Please note that your model is not the only one there, so you would need to take the steps carefully and 
add your model following the same template in order to not break anything un-intentionally.

After your adjusted the `conf.py` file then you can generate the docs using the Make file
```bash
make html
```

This would overwrite the contents of the documentations in the html and add your module as well. 


## Template Usage Instructions for CHANGELOG.md File

### **How to Document Changes**
   - Start all new updates under the `[Unreleased]` section.
   - Categorize each change under the appropriate section:
     - **✨ Added** — New features, new API endpoints, enhancements, etc.
     - **🛠️ Changed** — Changes to existing features, workflows, or refactoring.
     - **🐛 Fixed** — Resolved issues, crashes, performance improvements, etc.
     - **⚠️ Deprecated** — Features planned for removal in a future release.
     - **🚫 Removed** — Features, code, endpoints, or functionalities that have been removed.
   
### **When Releasing a New Version**
   - Move all entries from **[Unreleased]** to a new version section (e.g., `## [1.2.0] - 2024-11-15`).
   - Use [Semantic Versioning](https://semver.org/):
     - **MAJOR** version when you make incompatible API changes.
     - **MINOR** version when you add functionality in a backward-compatible manner.
     - **PATCH** version when you make backward-compatible bug fixes.
   
#### **Example Changelog Entry**
   ```markdown
   ## [1.2.0] - 2024-11-15
   ### ✨ Added
   - [x] New admin dashboard for role management.
   - [x] Added support for multi-factor authentication (MFA).

   ### 🛠️ Changed
   - [x] Updated `/api/users` endpoint to support pagination.
   - [x] Improved the performance of the login process.

   ### 🐛 Fixed
   - [x] Resolved issue with JWT tokens expiring prematurely.
   - [x] Fixed race condition in the data synchronization process.

   ### ⚠️ Deprecated
   - [x] Deprecated `/api/v1/old-endpoint`. Please migrate to `/api/v2/new-endpoint`.

   ### 🚫 Removed
   - [x] Removed unused endpoints `/api/v1/test-endpoint`.

### 📘 How to Phrase Deprecation Notices

When deprecating features, methods, or endpoints, it's important to clearly communicate **what's being deprecated**, **when it will be deprecated**, and **what users should do instead**. Use the following guidelines and phrasing examples to ensure clarity and consistency in your changelog.

---

#### 🔥 **Best Practices**
1. **Be Specific About the Version**  
   Indicate the exact version where the deprecation will occur, e.g.,  
   _"Will be deprecated in v2.0.0"_.  
   If the version is unknown, use **"in an upcoming release"** or **"in the next major release"**.

2. **Provide a Migration Path**  
   Suggest an alternative method, function, or endpoint that users should switch to.  
   Example:  
   > The `oldFunctionName()` method will be deprecated in v3.0.0.  
   > Use `newFunctionName()` instead to ensure compatibility with future versions.

3. **Clarify Future Removal**  
   If deprecation will lead to removal, communicate it clearly.  
   Example:  
   > The `/api/old-endpoint` will be deprecated in v2.5.0 and **removed in v3.0.0**.  
   > Migrate to `/api/new-endpoint` before v3.0.0 to avoid issues.

4. **Use Consistent Phrasing**  
   Stick to consistent terms, such as:  
   - **"Scheduled for deprecation in vX.X.X"**  
   - **"Will be deprecated in vX.X.X"**  
   - **"This feature will be deprecated after vX.X.X"**  

---

#### 📘 **Phrasing Templates**
Use these ready-to-go phrases to document your deprecations in changelogs.

#### ⚠️ **Simple Deprecation**
> The `oldFunctionName()` method will be deprecated in v2.0.0.  
> Use `newFunctionName()` instead to maintain compatibility.

#### ⚠️ **Deprecation with Exact Version**
> The `/api/old-endpoint` is **scheduled for deprecation in v2.0.0**.  
> Users are encouraged to migrate to `/api/new-endpoint`.

#### ⚠️ **Deprecation with Removal Notice**
> The `oldFunctionName()` method will be deprecated in v2.5.0 and **removed in v3.0.0**.  
> Please switch to `newFunctionName()` to avoid breaking changes.

#### ⚠️ **Deprecation with No Version Specified**
> The `legacyFunction()` method is scheduled for deprecation **in an upcoming release**.  
> We recommend migrating to `modernFunction()`.

#### ⚠️ **Deprecation with Migration Path**
> The `/api/legacy-auth` endpoint will be deprecated in v1.8.0.  
> Switch to `/api/oauth2-auth` to stay up-to-date with security standards.

---

#### 📘 **How to Document Deprecations in a Changelog**

Here’s an example of how to add deprecation notices to a **CHANGELOG.md** file.

    ## [Unreleased]
    ### ⚠️ Deprecated
    - The `/api/old-endpoint` is **scheduled for deprecation in v2.0.0**. Use `/api/new-endpoint` instead.
    - The `oldFunctionName()` method **will be deprecated in v1.5.0**. Use `newFunctionName()` to ensure compatibility.