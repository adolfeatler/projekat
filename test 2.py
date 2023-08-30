import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QTextCursor
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtCore import Qt, QUrl

class RichTextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        self.initMenuBar()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Rich Text Editor')
        self.show()

    def initMenuBar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        edit_menu = menubar.addMenu('Edit')
        link_action = QAction('Insert Link', self)
        link_action.triggered.connect(self.insertLink)
        edit_menu.addAction(link_action)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_path:
            with open(file_path, 'r') as file:
                self.textEdit.setPlainText(file.read())

    def insertLink(self):
        selected_text = self.textEdit.textCursor().selectedText()

        if selected_text:
            link, ok = QInputDialog.getText(self, "Insert Link", "Enter URL:")

            if ok and link:
                cursor = self.textEdit.textCursor()
                cursor.insertHtml(f'<a href="{link}">{selected_text}</a>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = RichTextEditor()
    sys.exit(app.exec_())