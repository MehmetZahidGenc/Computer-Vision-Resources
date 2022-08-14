# -*- coding: utf-8 -*-

"""
                                                             Created by Mehmet Zahid GENÇ 


"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import os
from PredictorClasses import makeClassDataList, Img_Processor
import shutil
import collections
import cv2


class Ui_MainWindow(object):
    def __init__(self):
        self.images_names_list = []
        self.images_status_list = []
        self.actual_path = ''
        self.Image_number = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1445, 861)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 20, 1171, 701))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label.setLineWidth(10)
        self.label.setText("")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 745, 461, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(920, 730, 251, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        self.nextButton.clicked.connect(self.increase_Image_number)


        self.previousbutton = QtWidgets.QPushButton(self.centralwidget)
        self.previousbutton.setGeometry(QtCore.QRect(640, 730, 251, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.previousbutton.setFont(font)
        self.previousbutton.setObjectName("previousbutton")
        self.previousbutton.clicked.connect(self.decrease_Image_number)


        self.trueButton = QtWidgets.QPushButton(self.centralwidget)
        self.trueButton.setGeometry(QtCore.QRect(1180, 70, 251, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.trueButton.setFont(font)
        self.trueButton.setAutoFillBackground(False)
        self.trueButton.setCheckable(False)
        self.trueButton.setObjectName("trueButton")
        self.trueButton.clicked.connect(self.pushTrue)

        self.falseButton = QtWidgets.QPushButton(self.centralwidget)
        self.falseButton.setGeometry(QtCore.QRect(1180, 170, 251, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.falseButton.setFont(font)
        self.falseButton.setObjectName("falseButton")
        self.falseButton.clicked.connect(self.pushFalse)

        self.completeButton = QtWidgets.QPushButton(self.centralwidget)
        self.completeButton.setGeometry(QtCore.QRect(1180, 420, 251, 131))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.completeButton.setFont(font)
        self.completeButton.setObjectName("completeButton")
        self.completeButton.clicked.connect(self.completeProcess)

        self.openFolderButton = QtWidgets.QPushButton(self.centralwidget)
        self.openFolderButton.setGeometry(QtCore.QRect(10, 730, 251, 81))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.openFolderButton.setFont(font)
        self.openFolderButton.setObjectName("openFolderButton")
        self.openFolderButton.clicked.connect(self.openFolderButton_handler)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1445, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", " "))
        self.nextButton.setText(_translate("MainWindow", "Next Image"))
        self.previousbutton.setText(_translate("MainWindow", "Previous Image"))
        self.trueButton.setText(_translate("MainWindow", "True"))
        self.falseButton.setText(_translate("MainWindow", "False"))
        self.completeButton.setText(_translate("MainWindow", "Complete the Control"))
        self.openFolderButton.setText(_translate("MainWindow", "Open Folder"))


    def increase_Image_number(self):
        if self.Image_number < len(self.images_names_list)-1:
            self.Image_number = self.Image_number + 1
            self.Process_File()


    def decrease_Image_number(self):
        if self.Image_number > 0:
            self.Image_number = self.Image_number - 1
            self.Process_File()

        elif self.Image_number == 0:
            self.Image_number = 0


    def pushTrue(self):
        if 0 <= self.Image_number < len(self.images_names_list):
            self.images_status_list[self.Image_number] = True


    def pushFalse(self):
        if 0 <= self.Image_number < len(self.images_names_list):
            self.images_status_list[self.Image_number] = False


    def openFolderButton_handler(self):
        self.open_dialog_box()


    def open_dialog_box(self):
        self.images_names_list = []

        self.actual_path = str(QFileDialog.getExistingDirectory())

        dirs = os.listdir(self.actual_path + '/')

        for item in dirs:
            if ('.jpg' in item) or ('.png' in item):
                self.images_names_list.append(item)

        if len(self.images_names_list) > 0:
            self.openFolderButton.setEnabled(False)

        for i in range(len(self.images_names_list)):
            self.images_status_list.append(True)

        self.Process_File()


    def Process_File(self):
        maker_class_Data_list = makeClassDataList(actualPath=self.actual_path)

        status = maker_class_Data_list.controlExisting()

        img = cv2.imread(f'{self.actual_path}/{self.images_names_list[self.Image_number]}')

        if status:

            class_liste = maker_class_Data_list.prepare_Data_Of_Classes_Info()

            img_processor = Img_Processor(class_liste, Actual_path=self.actual_path)

            try:
                label_txt_file_data_list = img_processor.getInfo_img_data_labels(f'{self.actual_path}/{self.images_names_list[self.Image_number]}')

                self.trueButton.setEnabled(True)
                self.falseButton.setEnabled(True)

                img = img_processor.drawBoundingBox(label_txt_file_data_list, f'{self.actual_path}/{self.images_names_list[self.Image_number]}')

            except:
                self.images_status_list[self.Image_number] = False
                self.trueButton.setEnabled(False)
                self.falseButton.setEnabled(False)

        else:
            self.label_2.setText("Classes Txt file does not exist !!")
            print('Classes Txt file does not exist !!')
            self.trueButton.setEnabled(False)
            self.falseButton.setEnabled(False)
            self.openFolderButton.setEnabled(True)
            self.completeButton.setEnabled(False)

        self.displayImage(img, 1)


    def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8

        if (len(img.shape)) == 3:
            if (img.shape[2]) == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888

        img = QtGui.QImage(img, img.shape[1], img.shape[0], qformat)

        img = img.rgbSwapped()
        self.label.setPixmap(QtGui.QPixmap.fromImage(img))
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


    def completeProcess(self):
        self.openFolderButton.setEnabled(True)
        self.trueButton.setEnabled(False)
        self.falseButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.falseButton.setEnabled(False)
        self.previousbutton.setEnabled(False)
        self.completeButton.setEnabled(False)

        print(self.images_names_list)
        print(self.images_status_list)

        if os.path.exists(f'{self.actual_path}/True_images'):
            pass
            print('True_images folder exists')
        else:
            print('True_images does not exist')
            print('creating True_images Folder')
            os.mkdir(f'{self.actual_path}/True_images')
            print('True_images Folder created')


        if os.path.exists(f'{self.actual_path}/False_images'):
            pass
            print('False_images folder exists')
        else:
            print('False_images does not exist')
            print('creating False_images Folder')
            os.mkdir(f'{self.actual_path}/False_images')
            print('False_images Folder created')


        index = 0
        for status in self.images_status_list:
            if status:
                try:
                    shutil.move(f'{self.actual_path}/{self.images_names_list[index]}', f'{self.actual_path}/True_images')
                    img_name, format_of_image = self.images_names_list[index].split('.')
                    shutil.move(f'{self.actual_path}/{img_name}.txt', f'{self.actual_path}/True_images')
                except:
                    pass
            else:
                try:
                    shutil.move(f'{self.actual_path}/{self.images_names_list[index]}', f'{self.actual_path}/False_images')
                    img_name, format_of_image = self.images_names_list[index].split('.')
                    shutil.move(f'{self.actual_path}/{img_name}.txt', f'{self.actual_path}/False_images')
                except:
                    pass
            index = index + 1

        data = collections.Counter(self.images_status_list)

        False_number, True_number = data[0], data[1]

        print(f'Number of True labelled images of in {len(self.images_names_list)}: {True_number}')
        print(f'Number of False labelled images of in {len(self.images_names_list)}: {False_number}')

        labelling_accuracy = (True_number / len(self.images_status_list)) * 100

        self.label_2.setText(f'Labelling Accuracy is %{labelling_accuracy}')

        print(f'Labelling Accuracy is %{labelling_accuracy}')

        # sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
