import cv2
import numpy as np
import face_recognition
import os


class FaceRoiCreator:
    """
    model-path : path of 'opencv_dnn_model.caffemodel'
    config_path : path of 'opencv_dnn_model.prototxt'

    threshvalue : min confidence value for face detection and give bounding box info
    img_size : While analyzing, we resize the picture to the size we want. Thus, a faster transaction is carried out

    model : face detection model that created by using model_path and config_path parameter
    """

    def __init__(self, model_path, config_path, img_size, threshvalue):

        self.model_path = model_path
        self.config_path = config_path

        self.model = cv2.dnn.readNetFromCaffe(self.config_path, self.model_path)

        self.threshvalue = threshvalue
        self.img_size = img_size

    """
    Detect_faces method return 6 parameter

    face_roi : we found the faces and make roi for each face.
    rgb_frame_roi : we found the faces and make roi for each face. To analyze this face roi in mediapipe, convert rgb color space 

    face_x_min : min x value of bounding box
    face_x_max : max x value of bounding box

    face_y_min : min y value of bounding box
    face_y_max : max y value of bounding box

    """

    def Detect_faces(self, frame):
        try:

            blob = cv2.dnn.blobFromImage(cv2.resize(frame, self.img_size), 1.0, self.img_size, [104.0, 117.0, 123.0])
            self.model.setInput(blob)

            faces = self.model.forward().squeeze()[:, 2:]

            faces = faces[faces[:, 0] > self.threshvalue]

            probabilities, faces = faces[:, 0], faces[:, 1:]

            frame_height, frame_width = frame.shape[:2]

            faces *= np.array([frame_width, frame_height, frame_width, frame_height])

            for (x, y, w, h) in faces:
                face_x_min = int(x)
                face_x_max = int(w)
                face_y_min = int(y)
                face_y_max = int(h)

                width = face_x_max-face_x_min
                length = face_y_max-face_y_min

                face_roi = frame[face_y_min:face_y_min+length, face_x_min:face_x_min+width]

                rgb_frame_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

                cv2.rectangle(frame, (face_x_min, face_y_min), (face_x_max, face_y_max), (0, 255, 0),
                              3)  # Draw bounding box

            return rgb_frame_roi, face_x_min, face_x_max, face_y_min, face_y_max, face_roi

        except:
            pass



class FaceRecognition:

    def __init__(self, faces_images_path):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []

        self.result = os.listdir(faces_images_path)

        self.known_face_names = []

        self.known_face_encodings = []

        
        # it is necessary to extract information from the file using a method, this format was used for the purpose of example.
        self.people = {'Elon': {'Name': 'Elon', 'Age': '-', 'Sex': 'Male'},
                       'Jeff': {'Name': 'Jeff', 'Age': '-', 'Sex': 'Male'},
                       'Tom': {'Name': 'Tom', 'Age': '-', 'Sex': 'Male'},
                       'Trump': {'Name': 'Trump', 'Age': '-', 'Sex': 'Male'}}

        for i in self.result:
            data = i.split(".")
            data = data[0]
            self.known_face_names.append(data)
            image = face_recognition.load_image_file(f"faces/{i}")
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(face_encoding)



    def RecognizeFaces(self, face_roi, face_x_max, face_y_min, to_putting_frame):

        process_this_frame = True

        rgb_faces_roi = face_roi[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_faces_roi)
            face_encodings = face_recognition.face_encodings(rgb_faces_roi, face_locations)

            self.face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a label with a name below the face
            # cv2.rectangle(to_putting_frame, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)

            font = cv2.FONT_HERSHEY_DUPLEX

            name = name.split('-')[0]

            # you can print the information we have obtained on the screen or use it for different purposes
            result_name = self.people[name]['Name']
            result_age = self.people[name]['Age']
            result_sex = self.people[name]['Sex']
