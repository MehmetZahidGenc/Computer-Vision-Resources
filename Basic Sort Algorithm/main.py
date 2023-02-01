import cv2
import numpy as np
from ZahidTrack import ZahidSort

sorting_algorithm = ZahidSort()
liste = ['img.png']

for img_names in liste:
    img = cv2.imread(img_names)
    detect_ids = sorting_algorithm.runner([[60, 35, 335, 140]], main_frame=img) # bbox: [[x1,y1,w1,h1], [x2,y2,w2,h2]]
    enhanced_image = sorting_algorithm.enhance_visuality(bbox_list=[[60, 35, 335, 140]], detected_ids=detect_ids, main_frame=img, rect=True)
    cv2.imshow('enhanced_image', enhanced_image)
    cv2.waitKey(0)
    print(f"Detected ids: {detect_ids}")