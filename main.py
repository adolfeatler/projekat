import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtCore import Qt, QUrl

#hyperlink
class hyperlinkwindow(QDialog):
    def __init__ (self, text_edit):
        super().__init__()
        self.textedit = text_edit
        self.setWindowTitle("Link")
        layout = QVBoxLayout()
        self.address_input = QLineEdit()
        layout.addWidget(self.address_input)
        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.add_hyperlink)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
    def add_hyperlink(self):
        address = self.address_input.text()
        selected_text = self.textedit.textCursor().selectedText()
        hyperlink = f'<a href="{address}">{selected_text}</a>'
        self.textedit.insertHtml(hyperlink) 
        print ( self.textedit.toHtml())        
        self.close()

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Open File"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()

        self.btn1 = QPushButton("Open Image")
        self.btn1.clicked.connect(self.getImage)

        vbox.addWidget(self.btn1)

        self.label = QLabel("Hello")
        vbox.addWidget(self.label)

        self.setLayout(vbox)


    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())



#pozivanje 
class RTE(QMainWindow):
    def __init__(self):
        super(RTE, self).__init__()
        self.editor = QTextEdit()
        self.fontSizeBox = QSpinBox()

        font = QFont("Times", 24)
        self.editor.setFont(font)
        self.path = ""
        self.setCentralWidget(self.editor)
        self.setWindowTitle("Rich Text Editor")
        self.showMaximized()
        self.create_tool_bar()
        self.editor.setFontPointSize(24)

    def create_tool_bar(self):
        toolbar = QToolBar()


        save_action = QAction(QIcon("save.png"), "Save", self) 
        save_action.triggered.connect(self.saveFile) 
        toolbar.addAction(save_action)

        undoBtn = QAction(QIcon("undo.png"), "undo", self) 
        undoBtn.triggered.connect(self.editor.undo)
        toolbar.addAction(undoBtn)

        redoBtn = QAction(QIcon("redo.png"), "redo", self)
        redoBtn.triggered.connect(self.editor.redo)
        toolbar.addAction(redoBtn)


        copyBtn = QAction(QIcon("copy.png"), "copy", self)
        copyBtn.triggered.connect(self.editor.copy)
        toolbar.addAction(copyBtn)

        cutBtn = QAction(QIcon("cut.png"), "cut", self)
        cutBtn.triggered.connect(self.editor.cut)
        toolbar.addAction(cutBtn)

        pasteBtn = QAction(QIcon("paste.png"), "paste", self)
        pasteBtn.triggered.connect(self.editor.paste)
        toolbar.addAction(pasteBtn)


        self.fontBox = QComboBox(self)
        list = QFontDatabase().families()
        self.fontBox.addItems(list)
        self.fontBox.activated.connect(self.setFont)
        toolbar.addWidget(self.fontBox)

        self.fontSizeBox.setValue(24)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar.addWidget(self.fontSizeBox)

        rightAllign = QAction(QIcon("right-allign.png"), "Right Allign", self)
        rightAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignRight))
        toolbar.addAction(rightAllign)
        
        centerAllign = QAction(QIcon("center-allign.png"), "Center Allign", self)
        centerAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignCenter))
        toolbar.addAction(centerAllign)

        leftAllign = QAction(QIcon("left-allign.png"), "Left Allign", self)
        leftAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignLeft))
        toolbar.addAction(leftAllign)

        toolbar.addSeparator()

        boldBtn = QAction(QIcon("bold.png"), "bold", self)
        boldBtn.triggered.connect(self.boldText) 
        toolbar.addAction(boldBtn)

        italicBtn = QAction(QIcon("italic.png"), "italic", self)
        italicBtn.triggered.connect(self.italicText)
        toolbar.addAction(italicBtn)

        underlineBtn = QAction(QIcon("underline.png"), "underline", self)
        underlineBtn.triggered.connect(self.underlineText)
        toolbar.addAction(underlineBtn)

        #colorset
        colorbtn = QAction(QIcon("paint.png"), "colorset", self)
        colorbtn.triggered.connect(self.setFontColor)
        toolbar.addAction(colorbtn)

        linkbtn = QAction(QIcon("link.png"), "linkset", self)
        linkbtn.triggered.connect(self.open_hyperlink_window)
        toolbar.addAction(linkbtn)
        

        self.addToolBar(toolbar)

    def open_hyperlink_window(self):
        self.selected_text = self.editor.textCursor().selectedText()
        if(self.selected_text):
            self.hyperlink_window = hyperlinkwindow(self.editor)
            self.hyperlink_window.exec_()


    def setFontSize(self):
        value = self.fontSizeBox.value()
        self.editor.setFontPointSize(value)

    def setFont(self):
        print(1)
        font = self.fontBox.currentText()
        print(font)
        font = QFont(font)
        print(font.toString())
        self.editor.setCurrentFont(QFont(font))
    
    # font color

    def setFontColor(self):
        color = QColorDialog.getColor()
        self.editor.setTextColor(color)

    #podvlacenje
    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not(state))

    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not(state))

    def boldText(self):
        if  self.editor.fontWeight != QFont.Bold:
              self.editor.setFontWeight(QFont.Bold)
              return
        self.editor.setFontWeight(QFont.Normal)

    def saveFile(self):
        print(self.path)
        if self.path == "":
            self.file_saveas()
        text = self.editor.toHtml()
        try:
            with open(self.path, "w") as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)

    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text documents (*.text);Text documents (*.txt);All files (*.*)")
        if self.path == '':
            return   
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
                self.update_title() 
        except Exception as e:
            print(e)
            
app = QApplication(sys.argv)
window = RTE()
window.show()
sys.exit(app.exec_())