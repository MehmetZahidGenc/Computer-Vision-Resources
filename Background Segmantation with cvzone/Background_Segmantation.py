import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation

cam = cv2.VideoCapture(0)

segmentor = SelfiSegmentation()

while True:
    ret, frame = cam.read()

    BackGroundImage = cv2.imread('daisy.jpg') # your bg image path
    BackGroundImage = cv2.resize(BackGroundImage, (frame.shape[1], frame.shape[0]))

    # you can change threshold value as you want or according to status that you are in
    OutputFrame = segmentor.removeBG(frame, BackGroundImage, threshold=0.7)

    cv2.imshow('frame', frame)
    cv2.imshow('OutputFrame', OutputFrame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
