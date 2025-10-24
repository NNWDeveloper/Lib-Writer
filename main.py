import sys, os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox,
    QToolBar, QFontDialog, QColorDialog
)
from PySide6.QtGui import QAction, QKeySequence, QTextCursor, QTextTableFormat, QTextCharFormat, QFont, QColor, QIcon, QImage, QTextDocumentFragment
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtCore import QTimer, Qt
from odf.opendocument import OpenDocumentText
from odf.text import P
from odf import teletype

AUTOSAVE_FILE = "autosave.odt"

class NNWLibWriter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NNW Lib-Writer 1.0")
        self.setGeometry(100, 100, 1100, 750)
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)
        self.current_file = None

        self.create_toolbar()
        self.create_menu()
        self.start_autosave()

    # --------------------
    # MENU
    # --------------------
    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("Soubor")
        open_action = QAction("Otevřít", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Uložit", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        export_action = QAction("Export do PDF", self)
        export_action.triggered.connect(self.export_pdf)
        file_menu.addAction(export_action)

        file_menu.addSeparator()
        exit_action = QAction("Ukončit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        format_menu = menu.addMenu("Formát")
        font_action = QAction("Písmo…", self)
        font_action.triggered.connect(self.select_font)
        format_menu.addAction(font_action)
        color_action = QAction("Barva textu…", self)
        color_action.triggered.connect(self.select_color)
        format_menu.addAction(color_action)

        align_menu = menu.addMenu("Zarovnání")
        for text, method in [("Vlevo", self.align_left),
                             ("Na střed", self.align_center),
                             ("Vpravo", self.align_right),
                             ("Do bloku", self.align_justify)]:
            a = QAction(text, self)
            a.triggered.connect(method)
            align_menu.addAction(a)

        insert_menu = menu.addMenu("Vložit")
        img_action = QAction("Obrázek…", self)
        img_action.triggered.connect(self.insert_image)
        insert_menu.addAction(img_action)
        table_action = QAction("Tabulku…", self)
        table_action.triggered.connect(self.insert_table)
        insert_menu.addAction(table_action)

    # --------------------
    # TOOLBAR
    # --------------------
    def create_toolbar(self):
        toolbar = QToolBar("Hlavní")
        self.addToolBar(toolbar)

        bold_action = QAction("B", self)
        bold_action.setShortcut(QKeySequence.Bold)
        bold_action.triggered.connect(self.toggle_bold)
        toolbar.addAction(bold_action)

        italic_action = QAction("I", self)
        italic_action.setShortcut(QKeySequence.Italic)
        italic_action.triggered.connect(self.toggle_italic)
        toolbar.addAction(italic_action)

        underline_action = QAction("U", self)
        underline_action.setShortcut(QKeySequence.Underline)
        underline_action.triggered.connect(self.toggle_underline)
        toolbar.addAction(underline_action)

        toolbar.addSeparator()
        font_action = QAction("Písmo", self)
        font_action.triggered.connect(self.select_font)
        toolbar.addAction(font_action)

        color_action = QAction("Barva", self)
        color_action.triggered.connect(self.select_color)
        toolbar.addAction(color_action)

    # --------------------
    # Formátování
    # --------------------
    def toggle_bold(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontWeight(700 if fmt.fontWeight() != 700 else 400)
        self.editor.setCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.editor.setCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = self.editor.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.editor.setCurrentCharFormat(fmt)

    def select_font(self):
        ok, font = QFontDialog.getFont()
        if ok: self.editor.setCurrentFont(font)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = self.editor.currentCharFormat()
            fmt.setForeground(color)
            self.editor.setCurrentCharFormat(fmt)

    def align_left(self): self.editor.setAlignment(Qt.AlignLeft)
    def align_center(self): self.editor.setAlignment(Qt.AlignCenter)
    def align_right(self): self.editor.setAlignment(Qt.AlignRight)
    def align_justify(self): self.editor.setAlignment(Qt.AlignJustify)

    # --------------------
    # Vkládání
    # --------------------
    def insert_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Vyber obrázek", "", "Obrázky (*.png *.jpg *.jpeg)")
        if path:
            cursor = self.editor.textCursor()
            cursor.insertImage(QImage(path))

    def insert_table(self):
        cursor = self.editor.textCursor()
        cursor.insertTable(2, 2)

    # --------------------
    # SOUBORY
    # --------------------
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Otevřít", "", "ODT (*.odt);;TXT (*.txt)")
        if path:
            try:
                if path.endswith(".txt"):
                    with open(path, "r", encoding="utf-8") as f:
                        self.editor.setPlainText(f.read())
                elif path.endswith(".odt"):
                    doc = OpenDocumentText(filename=path)
                    text = ""
                    for p in doc.getElementsByType(P):
                        text += teletype.extractText(p) + "\n"
                    self.editor.setPlainText(text.strip())
                self.current_file = path
            except Exception as e:
                QMessageBox.critical(self, "Chyba", str(e))

    def save_file(self):
        if not self.current_file:
            path, _ = QFileDialog.getSaveFileName(self, "Uložit jako", "", "ODT (*.odt)")
            if not path: return
            if not path.endswith(".odt"): path += ".odt"
            self.current_file = path
        try:
            doc = OpenDocumentText()
            for line in self.editor.toPlainText().split("\n"):
                doc.text.addElement(P(text=line))
            doc.save(self.current_file)
        except Exception as e:
            QMessageBox.critical(self, "Chyba", str(e))

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export do PDF", "", "PDF (*.pdf)")
        if not path: return
        if not path.endswith(".pdf"): path += ".pdf"
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(path)
        self.editor.document().print_(printer)

    # --------------------
    # Autosave
    # --------------------
    def start_autosave(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.autosave)
        self.timer.start(60000)  # každých 60s

    def autosave(self):
        try:
            doc = OpenDocumentText()
            for line in self.editor.toPlainText().split("\n"):
                doc.text.addElement(P(text=line))
            doc.save(AUTOSAVE_FILE)
        except: pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NNWLibWriter()
    win.show()
    sys.exit(app.exec())
