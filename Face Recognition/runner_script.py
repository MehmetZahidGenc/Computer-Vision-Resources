from Face_Recognition import FaceRoiCreator, FaceRecognition
import cv2


roi_creator_object = FaceRoiCreator(model_path='opencv_dnn_model.caffemodel', config_path='opencv_dnn_model.prototxt', threshvalue=0.80, img_size=(300, 300))

recognizer_object = FaceRecognition(faces_images_path='faces/')


cam = cv2.VideoCapture(0)

while cam.isOpened:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)

    try:
        rgb_frame_roi, face_x_min, face_x_max, face_y_min, face_y_max, face_roi = roi_creator_object.Detect_faces(frame)

        recognizer_object.RecognizeFaces(rgb_frame_roi, face_x_max, face_y_min, frame)

        cv2.imshow('faces_roi', face_roi)

    except:
        pass

    cv2.imshow('frame', frame)

    if cv2.waitKey(16) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
