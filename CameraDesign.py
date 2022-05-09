# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CameraDesign.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScreenshotWindow(object):
    def setupUi(self, ScreenshotWindow):
        ScreenshotWindow.setObjectName("ScreenshotWindow")
        ScreenshotWindow.resize(875, 621)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScreenshotWindow.sizePolicy().hasHeightForWidth())
        ScreenshotWindow.setSizePolicy(sizePolicy)
        ScreenshotWindow.setMinimumSize(QtCore.QSize(875, 621))
        self.gridLayout = QtWidgets.QGridLayout(ScreenshotWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.TakeScreenshot = QtWidgets.QPushButton(ScreenshotWindow)
        self.TakeScreenshot.setObjectName("TakeScreenshot")
        self.gridLayout.addWidget(self.TakeScreenshot, 1, 0, 1, 1)
        self.CameraLabel = QtWidgets.QLabel(ScreenshotWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CameraLabel.sizePolicy().hasHeightForWidth())
        self.CameraLabel.setSizePolicy(sizePolicy)
        self.CameraLabel.setMinimumSize(QtCore.QSize(800, 520))
        self.CameraLabel.setText("")
        self.CameraLabel.setScaledContents(True)
        self.CameraLabel.setObjectName("CameraLabel")
        self.gridLayout.addWidget(self.CameraLabel, 0, 0, 1, 1)

        self.retranslateUi(ScreenshotWindow)
        QtCore.QMetaObject.connectSlotsByName(ScreenshotWindow)

    def retranslateUi(self, ScreenshotWindow):
        _translate = QtCore.QCoreApplication.translate
        ScreenshotWindow.setWindowTitle(_translate("ScreenshotWindow", "Камера"))
        self.TakeScreenshot.setText(_translate("ScreenshotWindow", "Сделать скриншот"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ScreenshotWindow = QtWidgets.QWidget()
    ui = Ui_ScreenshotWindow()
    ui.setupUi(ScreenshotWindow)
    ScreenshotWindow.show()
    sys.exit(app.exec_())
