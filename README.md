# CW4.0 
```dev``` branch

## This repository contains the work files for the CW4.0 Research project in HVA Robot Lab
 For the CW4.0 the goal is to create a database of residual wood that can store information from the wood.

### Dependencies
For installing the dependencies, please look into the requirements.txt
or run this command in the terminal > ```pip install -r requirements.txt```

### Residual wood REST API
The API resources for wood and tagging of wood. The full documentation of the API endpoints are available at 
the swagger-ui accessing is through: http://localhost/swagger-ui for development server and 
https://rbotlab-residualwood.onrender.com/swagger-ui for the production server

The API blueprints and their interactions are in the resources, directory.

In order to create the blueprints the flask-smorest library is used.

### Database
The database is created using SQLAlchemy is used due to its features for ORM nature.
You can find the initiation of the database models in the ```./models/wood.py``` for the wood database
and ```./models/tags.py``` for the created tags that relates to the wood. 

The ```./models/wood_tags.py``` is the database table for the many-to-many relationship between tags and wood elements in
the database. As each wood can have several tags. And each tag can be associated with several woods from the database.

### Schema and Data validation
For the data validation, Marshmallow library is used to create the schemas that would be used. 
Each of the API methods check for these schemas. 

An example of the serialized JSON for the data relating to residual wood


### Docker
In order to run the server for development, you need to run the Docker container. 

#### How to create a docker image

```commandline
docker build --no-cache -t image_name .

```

#### How to run the Dockerfile locally

```commandline
docker run -dp 5000:5000 -w /app
 -v "/c/Users/username/directory/project_folder/project_name:/app" image_name

```

#### The Dockerfile setup for development

```commandline
FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

```

#### The Dockerfile setup for deployment

```commandline
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]
```

