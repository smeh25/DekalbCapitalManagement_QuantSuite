from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget

class VariablesPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def update_variables(self, variables_dict):
        self.list_widget.clear()
        for var_name in variables_dict:
            self.list_widget.addItem(var_name)
