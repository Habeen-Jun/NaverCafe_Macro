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
import urllib.request
from bs4 import BeautifulSoup

class ExampleWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(440, 240))    
        self.setWindowTitle("PyQt5 Clipboard example") 

        # # Add text field
        self.b = QTextEdit(self)
        # self.b.move(10,10)
        self.b.resize(400,200)
        document = QTextDocument()
        self.b.setDocument(document)
        # document.setPageSize(QSizeF(self.doc_width, self.doc_height))
        self.cursor = QTextCursor(document)
        root = document.rootFrame()
        self.cursor.setPosition(root.lastPosition())

        # self.b = QTextDocument(self)
        QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

    # Get the system clipboard contents
    def clipboardChanged(self):
        # html = QApplication.clipboard().to
        # print(img)

        # icon = QPixmap.fromImage(img)
        
        html = self.b.toHtml()
        soup = BeautifulSoup(html,'html.parser')
        img_list = soup.find_all('img')
        print(img_list)
        for img in img_list:
            print(img)
         
        urlString =  'https://lh3.googleusercontent.com/ogw/ADGmqu9OqMeqRnFRHCj1a4BJd0wbZqIxwRgwap6VVMuT=s32-c-mo'
        imageFromWeb = urllib.request.urlopen(urlString).read()
        qPixmapVar = QImage() 
        qPixmapVar.loadFromData(imageFromWeb)
        
        self.cursor.insertImage(qPixmapVar)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )