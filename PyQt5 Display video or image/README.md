# Display "video" or "image" with PyQt5

* We use Qt Designer to create and design main window

### Creating and designing main window

* Step 1 - create main window

![1](https://user-images.githubusercontent.com/71969819/189677827-16d28567-045e-4d8d-b697-387ded02e72f.png)


* Step 2 - Search label object

![2](https://user-images.githubusercontent.com/71969819/189677981-b144205d-e252-4b80-858a-122feb56a6af.png)


* Step 3 - let's place the label and change the name as we want

![3](https://user-images.githubusercontent.com/71969819/189678226-78da9774-9234-4e00-9428-d10ea409afb1.png)


* Step 4 - Define properties of QFrame of label object 

![4](https://user-images.githubusercontent.com/71969819/189678526-9c2f34fb-8896-465e-a179-1ae1371bca1d.png)


### Attention! 
  Before proceeding to next step , you must convert the ui file to py file

### In any python editor(visual studio, pycharm, ... ext), you make some functions to display images or videos.

* Ui_MainWindow class has method comes from Qt Designer and we add 2 or more method into class.

```
def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8

        if (len(img.shape)) == 3:
            if (img.shape[2]) == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888

        img = QtGui.QImage(img, img.shape[1], img.shape[0], qformat)

        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

```


```
def start_video(self):

        cam = cv2.VideoCapture(0)

        while cam.isOpened():
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)

            self.displayImage(frame, 1)

            if cv2.waitKey(16) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

```

* in the algorithm we have created, the last part of the code should look like this

```
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())

```

* Entire code block

```
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1092, 654)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.imgLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgLabel.setGeometry(QtCore.QRect(10, 10, 871, 541))
        self.imgLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.imgLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgLabel.setLineWidth(7)
        self.imgLabel.setObjectName("imgLabel")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1092, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.imgLabel.setText(_translate("MainWindow", " "))

    def displayImage(self, img, window=1):
        qformat = QtGui.QImage.Format_Indexed8

        if (len(img.shape)) == 3:
            if (img.shape[2]) == 4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888

        img = QtGui.QImage(img, img.shape[1], img.shape[0], qformat)

        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QtGui.QPixmap.fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def start_video(self):

        cam = cv2.VideoCapture(0)

        while cam.isOpened():
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)

            self.displayImage(frame, 1)

            if cv2.waitKey(16) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


```


