import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from button_widget import ButtonWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Multi-Button Example")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()
    
    def initUI(self):
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        vbox = QVBoxLayout()

        # Create two instances of ButtonWidget with identifiers
        button1 = ButtonWidget("Button 1", "Button1")
        button2 = ButtonWidget("Button 2", "Button2")

        # Add buttons to the layout
        vbox.addWidget(button1)
        vbox.addWidget(button2)

        # Set the layout on the central widget
        central_widget.setLayout(vbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
