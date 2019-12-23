# Faceapp Flask Face Recognition Back End

1. Install all requirements in requirements.txt
2. source env/bin/activate
3. Application has been optimized for docker container run. If you choose to run this server on local machine without docker, you will need to configure the app.py on lines: 12, 13, 14 with your local directory path. Additonally, dlib 19.19.0 will need to be installed. This requirement has been taken out of requirements.txt to optimize docker image build.
4. 'python3 app.py' to run server

# Docker Container setup commands

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