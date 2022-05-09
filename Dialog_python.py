# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_python.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_python(object):
    def setupUi(self, Dialog_python):
        Dialog_python.setObjectName("Dialog_python")
        Dialog_python.resize(350, 183)
        self.label = QtWidgets.QLabel(Dialog_python)
        self.label.setGeometry(QtCore.QRect(10, 10, 291, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog_python)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Dialog_python)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(Dialog_python)
        self.label_3.setGeometry(QtCore.QRect(10, 145, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog_python)
        QtCore.QMetaObject.connectSlotsByName(Dialog_python)

    def retranslateUi(self, Dialog_python):
        _translate = QtCore.QCoreApplication.translate
        Dialog_python.setWindowTitle(_translate("Dialog_python", "Dialog"))
        self.label.setText(_translate("Dialog_python", "Python version: 3.7"))
        self.label_2.setText(_translate("Dialog_python", "PyQt5 version: 5.13"))
        self.label_4.setText(_translate("Dialog_python", "Opencv version: 4.1.1.26"))
        self.label_3.setText(_translate("Dialog_python", "Version programm: beta 0.8.1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_python = QtWidgets.QDialog()
    ui = Ui_Dialog_python()
    ui.setupUi(Dialog_python)
    Dialog_python.show()
    sys.exit(app.exec_())
