from flask import Flask
from PIL import Image
import face_recognition

app = Flask(__name__)

@app.route('/test')
def index():
  image = face_recognition.load_image_file("./test/biden.jpg")
  face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

  print("I found {} face(s) in this photograph.".format(len(face_locations)))

  for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()
  return "Hello, World!"

@app.route('/api/recognize')
def recognize():
  return "this works"


if __name__ == "__main__":
  app.run(debug=True)