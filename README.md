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

Endpoints:

```
/residual_wood 
/residual_wood/{wood_id}
/tags
/tag/{tag_id}
/residual_wood/{wood_id}/tag/{tag_id}
/woods_tags/{woods_tag_id}
/tag/{tag_name}
/residual_wood/tag/{tag_name}
```

Methods:
```[GET, PUT, POST, DELETE]```

The API blueprints and their interactions are in the resources, directory.

In order to create the blueprints the flask-smorest library is used.

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

An example of the serialized JSON for the data relating to residual wood

```{
	"color": "222,130,34",
	"density": 0.19444153846153847,
	"height": 10.0,
	"id": 10,
	"image": "string",
	"info": "Intake for residual wood in Robot Lab HvA, for production of the Stool in WP1 for CW4.0 Project",
	"is_fire_treated": false,
	"is_planed": true,
	"is_straight": true,
	"label": "string",
	"length": 1674.0,
	"name": "string",
	"paint": "string",
	"price": 0.0,
	"project_type": "string",
	"reservation_name": "-",
	"reservation_time": "-",
	"reserved": false,
	"source": "HvA Jakoba Mulderhuis (JMH)",
	"timestamp": "2023-10-02 15:25-27",
	"type": "Hardwood",
	"weight": 13000.0,
	"width": 151.0,
	"wood_species": "string"
}
```

### Docker

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

### Running the application via Docker
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

### Developing and testing the API

For testing the API during development, you can use different tools such as Postman
or Insomnia. I used Insomnia. You can find an exported collection of requests inside
the insomnia directory in the project src. Once you installed Insomnia, you can import the collection of the
requests. 