from PyQt5 import QtCore, QtGui, QtWidgets

import sys


class Ui_Main(QtWidgets.QWidget):
       def setupUi(self, Main):
           Main.setObjectName("Main")
           Main.resize(800, 480)

           self.QtStack = QtWidgets.QStackedLayout()

           self.stack1 = QtWidgets.QWidget()
           self.stack2 = QtWidgets.QWidget()
           self.stack3 = QtWidgets.QWidget()

           self.Window1UI()
           self.Window2UI()
           self.Window3UI()

           self.QtStack.addWidget(self.stack1)
           self.QtStack.addWidget(self.stack2)
           self.QtStack.addWidget(self.stack3)

       def Window1UI(self):
           self.stack1.resize(800, 480)

           #PushButton1#
           self.PushButton1 = QtWidgets.QPushButton(self.stack1)
           self.PushButton1.setText("BUTTON 1")
           self.PushButton1.setGeometry(QtCore.QRect(10, 10, 100, 100))

           #PushButton2#
           self.PushButton2 = QtWidgets.QPushButton(self.stack1)
           self.PushButton2.setText("BUTTON 2")
           self.PushButton2.setGeometry(QtCore.QRect(150, 150, 100, 100))

       def Window2UI(self):
           self.stack2.resize(800, 480)
           self.stack2.setStyleSheet("background: red")

       def Window3UI(self):
           self.stack3.resize(800, 480)
           self.stack3.setStyleSheet("background: blue")