import face_recognition
import cv2
import os

FACES_DIR = 'faces'
ENCODINGS_DIR = 'face_encodings'


faces_list = os.listdir(FACES_DIR)
for each_face_file in faces_list:
    print("Processing file {}".format(each_face_file))
    face_image = face_recognition.load_image_file(os.path.join(FACES_DIR, each_face_file))
    face_encoding = face_recognition.face_encodings(face_image)[0]
    person_name = each_face_file.split('.')[0]
    face_encoding.dump(os.path.join(ENCODINGS_DIR, person_name))

print("Done")
