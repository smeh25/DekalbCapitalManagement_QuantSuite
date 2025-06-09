from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout

class VariablesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_widget = QListWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def update_variables(self, registry):
        self.list_widget.clear()
        for name in registry:
            self.list_widget.addItem(name)
