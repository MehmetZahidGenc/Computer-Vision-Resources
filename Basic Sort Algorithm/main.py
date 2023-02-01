import cv2
import numpy as np
from ZahidTrack import ZahidSort

sorting_algorithm = ZahidSort()

detect_ids = sorting_algorithm.runner(bbox_list, main_frame=img) # bbox_list: [[x1,y1,w1,h1], [x2,y2,w2,h2]]
enhanced_image = sorting_algorithm.enhance_visuality(bbox_list, detected_ids=detect_ids, main_frame=img, rect=True)
