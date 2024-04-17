from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout
from data_processor import process_data

class ButtonWidget(QWidget):
    def __init__(self, button_text, button_id):
        super().__init__()
        self.button_id = button_id
        self.initUI(button_text)

    def initUI(self, button_text):
        # Create layout
        vbox = QVBoxLayout()

        # Create button and add to layout
        self.button = QPushButton(button_text)
        self.button.clicked.connect(self.on_click)  # Connect button click to handler
        vbox.addWidget(self.button)

        # Set the layout
        self.setLayout(vbox)

    def on_click(self):
        # Trigger data processing when the button is clicked
        process_data(self.button_id)
