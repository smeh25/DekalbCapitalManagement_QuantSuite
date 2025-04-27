from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit
from app.command_executor import execute_command

class CommandLinePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.command_input = QLineEdit()
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        self.command_input.returnPressed.connect(self.run_command)

        layout.addWidget(self.command_input)
        layout.addWidget(self.output_display)
        self.setLayout(layout)

    def run_command(self):
        command = self.command_input.text()
        result = execute_command(command)
        self.output_display.append(f"> {command}")
        self.output_display.append(str(result))
        self.command_input.clear()
