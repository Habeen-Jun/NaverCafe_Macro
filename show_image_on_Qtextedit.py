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
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QTextEdit, QPushButton, QBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import urllib.request
from bs4 import BeautifulSoup
import re

class ExampleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):
        self.setMinimumSize(QSize(440, 240))    
        self.setWindowTitle("PyQt5 Clipboard example") 
        self.layout = QVBoxLayout(self)
        
        # # Add text field 
        self.b = QTextEdit()
 

        self.button = QPushButton('Get Full Html')
        # self.button.clicked.connect(self.getfullhtml)
        self.b.textChanged.connect(self.getfullhtml)
 
        document = QTextDocument()
        self.b.setDocument(document)
        self.cursor = QTextCursor(document)
        root = document.rootFrame()
        self.cursor.setPosition(root.lastPosition())

        self.layout.addWidget(self.b)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
    # Get the system clipboard contents
    def getfullhtml(self):
        html = self.b.toHtml()
        html_list = re.split('<img[^<>]*>', html)
         
        soup = BeautifulSoup(html,'html.parser')
        img_list = soup.find_all('img')
      
        html_num = 0
        self.b.clear()
        for img in img_list:
            imageFromWeb = urllib.request.urlopen(img.attrs['src']).read()
            qPixmapVar = QImage() 
            qPixmapVar.loadFromData(imageFromWeb)
            self.cursor.insertHtml(html_list[html_num])
            self.cursor.insertImage(qPixmapVar)
            html_num += 1 

         
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )