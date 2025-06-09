from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from ui.command_line_window import CommandLineWindow
from ui.variables_window import VariablesWindow
import input_parser_main as parser

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hedge Fund CLI")
        self.setGeometry(100, 100, 1200, 600)

        self.command_line = CommandLineWindow()
        self.variables_window = VariablesWindow()

        self.command_line.run_button.clicked.connect(self.run_command)

        layout = QHBoxLayout()
        layout.addWidget(self.command_line)
        layout.addWidget(self.variables_window)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.update_variables()

    def run_command(self):
        user_input = self.command_line.text_edit.toPlainText()
        output = parser.parse_input(user_input)
        print(output)
        self.update_variables()

    def update_variables(self):
        self.variables_window.update_variables(parser.get_registry())
