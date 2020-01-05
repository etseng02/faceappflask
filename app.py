from flask import Flask, request, send_file, send_from_directory
from PIL import Image, ImageDraw
import face_recognition
from flask_cors import CORS
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.config["IMAGE_UPLOADS"] = os.getenv('IMAGE_UPLOADS')
app.config["IMAGE_RESULTS"] = os.getenv('IMAGE_RESULTS')
app.config["IMAGE_FACES"] = os.getenv('IMAGE_FACES')
app.config["ALLOWED_IMAGE_EXTENSIONS"] = os.getenv('ALLOWED_IMAGE_EXTENSIONS')
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

          known_face_encodings = []
          known_face_names = []

          for file in os.listdir(app.config["IMAGE_FACES"]):
            # print(file)
            #load image file and encode
            temp_image = face_recognition.load_image_file("./faces/{}".format(file))
            temp_encoding = face_recognition.face_encodings(temp_image)[0]

            # Append image file encoding into known_face_encodings
            known_face_encodings.append(temp_encoding)

            #Process file name for dashes and takes out ext
            name_without_ext = file.rsplit(".", 1)[0]
            name_without_dash = name_without_ext.rsplit("-", -1)

            def listToString(s):
              str1 = " "
              return (str1.join(s))

            final_name = listToString(name_without_dash)
  
            # Append name into known_face_names 
            known_face_names.append(final_name)

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

          return send_file(app.config["IMAGE_RESULTS"] + "/" + filename, attachment_filename=filename, cache_timeout=0)

  return "Hello world"

@app.route('/api/train', methods=['POST'])
def train():

  if request.method == "POST":

    if request.files:
      
      image = request.files["image"]

      # image should not have a blank name
      if image.filename == "":
        print ("Image must have a filename")
        return "400"
      
      #file should have the proper extension
      if not allowed_image(image.filename):
        print ("That image extension is not allowed")
        return "400"

      # save image to faces
      filename = secure_filename(image.filename)
      image.save(os.path.join(app.config["IMAGE_FACES"], filename))

      # Process Image for faces
      processing_image = face_recognition.load_image_file(image)
      face_locations = face_recognition.face_locations(processing_image)
      print("I found {} face(s) in this photograph.".format(len(face_locations)))
      
      # no face detected, delete image
      if len(face_locations) < 1:
        os.remove(app.config["IMAGE_FACES"] + '/' + filename)
        return "no faces"

      # more than 2 faces detected, delete image
      if len(face_locations) > 1:
        os.remove(app.config["IMAGE_FACES"] + '/' + filename)
        return "too many faces"

  return "saved"


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)