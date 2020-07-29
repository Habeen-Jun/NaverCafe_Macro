# PyQt5 clipboard
#
# Gets text from the system clipboard
# If you copy text to the clipboard,
# output is shown in the console.
#
# pythonprogramminglanguage.com
#

import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import QSize
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ExampleWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(440, 240))    
        self.setWindowTitle("PyQt5 Clipboard example") 

        # Add text field
        self.b = QTextEdit(self)
        self.b.insertPlainText("Use your mouse to copy text to the clipboard.\nText can be copied from any application.\n")
        self.b.move(10,10)
        self.b.resize(400,200)
        self.cursor = QTextCursor(self.b.document())

        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

    # Get the system clipboard contents
    def clipboardChanged(self):
        img = QApplication.clipboard().mimeData()
        print(img)
        print(self.b.canInsertFromMimeData(img))
        # self.b.insertFromMimeData(text)
        self.b.insertFromMimeData(img)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )