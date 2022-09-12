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

* Ui_MainWindow class has method comes form Qt Designer and we add 2 or more method into class.

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
