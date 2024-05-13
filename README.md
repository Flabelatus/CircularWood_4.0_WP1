# Wood Database REST API

```master``` branch

## This repository contains the work files of API written for the CW4.0 Research project in HVA Robot Lab

For the CW4.0 work package one, the goal was to create a database of residual wood that can store information from the wood.
In order to develop the application, Flask is used. Flask is relatively easy and quick to start framework, but if the goal is
to scale this application up, it's probably better to enable concurrency and for that we can use a different frameworks like 
Fast API or Django. 

### Contact

- Development: Javid Jooshesh j.jooshesh@hva.nl

### Wood Database REST API

The API resources for wood and tagging of wood. The full documentation of the API endpoints are available at
the api-docs accessing is through: http://localhost/api-docs for development server and
https://robotlab-residualwood.onrender.com/api-docs for the production server

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

If you are using Windows or Mac, Install Docker via downloading and installing Docker Desktop

In order to run this api for development, please create a Docker image and run
the app in the container.

Running the application in the Docker container can be done via two ways in this project via `Dockerfile` or `docker-compose` command. Following is the instructions for both ways.

## 1. Docker via Dockerfile
### Create a docker image

```commandline
docker build --no-cache -t image_name .

```

### Run the Dockerfile locally

```commandline
docker run -dp 5000:5000 -w /app
 -v "/c/Users/username/directory/project_folder/project_name:/app" image_name

```

## 2. Docker via docker-compose 
### Run the Docker via docker-compose (simpler method)
There is a docker-compose.yml file in the project root that can be used to create the image and container via the following command
```commandline
docker-compose up -d
```
### Remove the docker container via docker-compose
```commandline
docker-compose down
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

## Contributing to the API
 please check the CONTRIBUTING.md document
