# Faceapp Flask Face Recognition API Server

API server for Face App. See front end here: https://github.com/etseng02/faceapp

This flask server contains the facial recognition portion of Face App. This server has been dockerized. You may choose to run the app locally or run as a docker container.

## Run API server locally

1. Install all requirements in requirements.txt via "pip3 install -r requirements.txt"
2. Create a .env file at root level of server. Insert the following and populate inside the quotations with the path pointing to the respective uploads, results and faces folders.
Unfinished example:
```
  IMAGE_UPLOADS=""
  IMAGE_RESULTS=""
  IMAGE_FACES=""
```

Completed example for .env file:
```
  IMAGE_UPLOADS="app/uploads"
  IMAGE_RESULTS="app/results"
  IMAGE_FACES="app/faces"
```
3. Run "source env/bin/activate" in terminal to activate .env variables
4. "flask run" to run server

## Docker Container setup commands

docker build -t faceappflask .

docker container run -p 5000:5000 -d --name faceappflask faceappflask

## Requirements
  Click==7.0
  dlib==19.19.0
  face-recognition==1.2.3
  face-recognition-models==0.3.0
  Flask==1.1.1
  Flask-Cors==3.0.8
  itsdangerous==1.1.0
  Jinja2==2.10.3
  MarkupSafe==1.1.1
  numpy==1.17.4
  Pillow==6.2.1
  six==1.13.0
  virtualenv==16.7.9
  Werkzeug==0.16.0