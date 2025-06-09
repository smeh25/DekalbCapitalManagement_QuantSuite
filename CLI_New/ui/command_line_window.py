from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QVBoxLayout

class CommandLineWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_edit = QTextEdit(self)
        self.run_button = QPushButton("Run Command", self)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
