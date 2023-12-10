# CONTRIBUTING

## Running the Application
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
To test the endpoints, Insomnia is used. Here is the download link: 

### Setting up the Insomnia profile
Once you downloaded and run the Insomnia app, now it's time to import the collection of 
requests for all the endpoints registered in the API.

There is an exported collection available to get yourself started. 
You can find the JSON file inside the `./insomnia` directory. You need to import this
JSON file inside the Insomnia. After that, you would need to proceed with setting the 
environment variables such as `url`, `access_token` in Insomnia. 

You can google and check the documentations of the Insomnia to do it. but basically you would
need to set the environment variables like this as example: 
```
{
    "url": "http://localhost:5000",
    "access_token": <The access_token from the JWT>
}
```
