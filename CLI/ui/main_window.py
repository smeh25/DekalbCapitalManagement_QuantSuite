from PyQt5.QtWidgets import QMainWindow, QDockWidget
from ui.variables_panel import VariablesPanel
from ui.command_line_panel import CommandLinePanel
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quant Workspace")
        self.resize(1200, 800)

        # Create panels
        self.variables_panel = VariablesPanel()
        self.command_line_panel = CommandLinePanel()

        # Wrap panels in dock widgets
        self.variables_dock = QDockWidget("Variables", self)
        self.variables_dock.setWidget(self.variables_panel)

        self.command_line_dock = QDockWidget("Command Line", self)
        self.command_line_dock.setWidget(self.command_line_panel)

        # Add dock widgets to the main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.variables_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.command_line_dock)

        # Allow them to be moved/floated
        self.variables_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.command_line_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
