# -*- coding: utf-8 -*-

"""
                                                             Created by Mehmet Zahid GENÇ 

"""


import cv2
import numpy as np
import os


class makeClassDataList:
    def __init__(self, actualPath):
        self.actualPath = actualPath
        self.classes_data_list = []

    def controlExisting(self):
        status_of_existing = os.path.exists(self.actualPath+'/classes.txt')

        return status_of_existing

    def prepare_Data_Of_Classes_Info(self):
        classes_txt_file = open('classes.txt', 'r')
        Lines_classes = classes_txt_file.readlines()

        for line_class in Lines_classes:
            data_class = line_class.split(' ')

            self.classes_data_list.append(data_class[0])

        return self.classes_data_list


class Img_Processor:
    def __init__(self, classes_data_list, Actual_path):
        self.classes_data_list = classes_data_list
        self.Actual_path = Actual_path


    def getInfo_img_data_labels(self, img_info):
        label_txt_file_data_list = []

        img_name, format_of_image = img_info.split('.')

        if os.path.exists(f'{img_name}.txt'):
            img_label_txt_file = open(f'{img_name}.txt', 'r')

            Lines_of_label_txt_file = img_label_txt_file.readlines()

            for line in Lines_of_label_txt_file:
                data_of_label_txt_file = line.split(' ')

                data = []

                for i in range(5):
                    data.append(data_of_label_txt_file[i])

                label_txt_file_data_list.append(data)

            return label_txt_file_data_list

        else:
            print('Txt file does not exist !!')


    def drawBoundingBox(self, label_txt_file_data_list, img_info):
        img = cv2.imread(f'{img_info}')

        dh, dw, _ = img.shape

        for i in range(len(label_txt_file_data_list)):

            class_id, x, y, w, h = int(label_txt_file_data_list[i][0]), float(label_txt_file_data_list[i][1]), float(
                label_txt_file_data_list[i][2]), \
                                   float(label_txt_file_data_list[i][3]), float(label_txt_file_data_list[i][4])

            l = int((x-w / 2) * dw)
            r = int((x+w / 2) * dw)
            t = int((y-h / 2) * dh)
            b = int((y+h / 2) * dh)

            if l < 0:
                l = 0
            if r > dw-1:
                r = dw-1
            if t < 0:
                t = 0
            if b > dh-1:
                b = dh-1

            cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)

            cv2.putText(img, self.classes_data_list[class_id][:len(self.classes_data_list[class_id])-1], (l, t),
                        cv2.FONT_HERSHEY_PLAIN,
                        1, (0, 0, 255), 1)

        return img
