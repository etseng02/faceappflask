from flask import Flask, request, send_file, send_from_directory
from PIL import Image, ImageDraw
import face_recognition
from flask_cors import CORS
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)


@app.route('/test')
def index():
  obama_image = face_recognition.load_image_file("./test/obama.jpg")
  obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

  # Load a second sample picture and learn how to recognize it.
  biden_image = face_recognition.load_image_file("./test/biden.jpg")
  biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

  known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
  ]
  known_face_names = [
      "Barack Obama",
      "Joe Biden"
  ]

  unknown_image = face_recognition.load_image_file("./test/two_people.jpg")

  # Find all the faces and face encodings in the unknown image
  face_locations = face_recognition.face_locations(unknown_image)
  face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

  pil_image = Image.fromarray(unknown_image)
  # Create a Pillow ImageDraw Draw instance to draw with
  draw = ImageDraw.Draw(pil_image)

  # Loop through each face found in the unknown image
  for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown"

    # If a match was found in known_face_encodings, just use the first one.
    # if True in matches:
    #     first_match_index = matches.index(True)
    #     name = known_face_names[first_match_index]

    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]

    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
  del draw

  # Display the resulting image
  pil_image.show()

    # You can also save a copy of the new image to disk if you want by uncommenting this line
    # pil_image.save("image_with_boxes.jpg")
  return "Hello, World!"
  
  
app.config["IMAGE_UPLOADS"] = "/Users/eddietseng/Developer/faceappflask/uploads"
app.config["IMAGE_RESULTS"] = "/Users/eddietseng/Developer/faceappflask/results"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG"]

def allowed_image(filename):
  if not "." in filename:
    return false

  ext = filename.rsplit(".", 1)[1]

  if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
    return True
  else:
    return False

@app.route('/api/recognize', methods=['POST'])
def recognize():

  print(request)

  if request.method == "POST":

    if request.files:

        image = request.files["image"]

        if image.filename == "":
          print ("Image must have a filename")
          return "400"

        if not allowed_image(image.filename):
          print ("That image extension is not allowed")
          return "400"
        else:
          filename = secure_filename(image.filename)
          image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
          print ("image saved")

          obama_image = face_recognition.load_image_file("./test/obama.jpg")
          obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

          # Load a second sample picture and learn how to recognize it.
          biden_image = face_recognition.load_image_file("./test/biden.jpg")
          biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

          known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
          ]
          known_face_names = [
            "Barack Obama",
            "Joe Biden"
          ]

          unknown_image = face_recognition.load_image_file('./uploads/{}'.format(filename))

          face_locations = face_recognition.face_locations(unknown_image)
          face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

          pil_image = Image.fromarray(unknown_image)
          draw = ImageDraw.Draw(pil_image)

          # Loop through each face found in the unknown image
          for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
              name = known_face_names[best_match_index]

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

          # Remove the drawing library from memory as per the Pillow docs
          del draw

          # Display the resulting image
          pil_image.save(os.path.join(app.config["IMAGE_RESULTS"], filename))


          return send_file('/Users/eddietseng/Developer/faceappflask/results/{}'.format(filename), attachment_filename=filename, cache_timeout=0)
          # print(filename)
          # return send_from_directory('uploads', filename)

  return "Hello world"

@app.route('/api/train')
def train():

  return "this api/train"


if __name__ == "__main__":
  app.run(debug=True)