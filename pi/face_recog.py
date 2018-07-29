import face_recognition
import cv2
import os
import numpy

FACE_ENCODINGS_DIR = 'face_encodings'


class FaceRecog(object):

    def __init__(self):
        # Create arrays of known face encodings and their names
        self.known_face_encodings = []
        self.known_face_names = []
        face_encoding_files = os.listdir(FACE_ENCODINGS_DIR)
        for each_encoding_file in face_encoding_files:
            self.known_face_encodings.append(
                numpy.load(os.path.join(FACE_ENCODINGS_DIR, each_encoding_file))
            )
            self.known_face_names.append(each_encoding_file)

    def process(self, frame, draw_on_frame=True):
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        faces = []
        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]

            if draw_on_frame:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            faces.append({
                'location': [top, right, bottom, left],
                'name': name
            })

        return faces 
