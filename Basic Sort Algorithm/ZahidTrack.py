import cv2
import numpy as np


class ZahidSort:
    def __init__(self, h_bins=50, s_bins=60, h_ranges = [0, 180], s_ranges = [0, 256], channels = [0, 1], thresh_value = 0.60, enhanced_visuality = True):
        self.h_bins = h_bins
        self.s_bins = s_bins
        self.histSize = [self.h_bins, self.s_bins]
        self.h_ranges = h_ranges
        self.s_ranges = s_ranges
        self.ranges = self.h_ranges+self.s_ranges
        self.channels = channels
        self.compare_method = cv2.HISTCMP_CORREL
        self.id = 0
        self.dataDictionary = {}
        self.thresh_value = thresh_value
        self.enhanced_Visuality = enhanced_visuality

        # for enhance visuality
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 1
        self.color = (255, 0, 0)
        self.thickness = 1

    @staticmethod
    def reverse_dict(original_dict):
        new_dict = {}
        for k, v in original_dict.items():
            dict_element = {k: v}
            dict_element.update(new_dict)
            new_dict = dict_element
        return new_dict

    def print_DataDict(self):
        print(self.dataDictionary)

    def printLen(self):
        print(len(self.dataDictionary))

    def enhance_visuality(self, bbox_list, detected_ids, main_frame, rect=False):
        if self.enhanced_Visuality:
            for i in range(len(bbox_list)):
                bbox = bbox_list[i]
                id_number = detected_ids[i]
                id_x, id_y = bbox[0]+int(bbox[3]/2), bbox[1]
                enhancedImage = cv2.putText(main_frame, str(id_number), (id_x, id_y), self.font, self.fontScale, self.color, self.thickness, cv2.LINE_AA)
                if rect:
                    cv2.rectangle(enhancedImage, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]),
                                  color=(0, 0, 255), thickness=3)
            return enhancedImage


    def runner(self, bbox_list, main_frame):
        # bbox_list = [[x1,y1,w1,h1], [x2,y2,w2,h2]]
        cropped_images = [] # it includes crop images from main frame
        detection_id = 0
        detected_ids = []

        for bbox in bbox_list:
            crop_image = main_frame[bbox[0]:bbox[0]+bbox[3], bbox[1]:bbox[1]+bbox[2]]
            cropped_images.append(crop_image)

        for i in range(len(cropped_images)):
            image = np.array(cropped_images[i])

            img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            hist_img = cv2.calcHist([img_hsv], self.channels, None, self.histSize, self.ranges, accumulate=False)
            hist_img = cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

            if len(self.dataDictionary) > 0:
                compared_values_list = []
                for id_number in self.dataDictionary.keys():
                    compared_image = self.dataDictionary[id_number]
                    compared_value = cv2.compareHist(compared_image, hist_img, self.compare_method)
                    if compared_value > self.thresh_value:
                        detection_id = int(id_number)
                    compared_values_list.append(compared_value)

                if len([compared_values_list[i] for i in range(len(self.dataDictionary)) if compared_values_list[i] >= self.thresh_value]) != 0:
                    pass # not include new object
                else: # include new object or objects
                    if len(self.dataDictionary) > 10: # Geçmişe dair 10 tane id bilgisini içerisinde tutacaktır.
                        new_dict = self.reverse_dict(self.dataDictionary)
                        new_dict.popitem()
                        new_dict = self.reverse_dict(new_dict)
                        self.dataDictionary = new_dict
                    detection_id = self.id
                    self.dataDictionary[str(self.id)] = hist_img
                    self.id = self.id+1

            else: # It will only work for the initial state
                self.dataDictionary[str(self.id)] = hist_img
                self.id = self.id+1
                detection_id = 0

            detected_ids.append(detection_id)

        return detected_ids