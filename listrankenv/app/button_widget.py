from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout

class ButtonWidget(QWidget):
    def __init__(self, button_text, item, callback):
        super().__init__()
        self.callback = callback
        self.initUI(button_text, item)

    def initUI(self, button_text, item):
        self.vbox = QVBoxLayout()
        self.button = QPushButton(button_text)
        self.button.clicked.connect(self.on_click)
        self.item = item
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)

    def update_text_and_item(self, text, item):
        self.button.setText(text)
        self.item = item

    def on_click(self):
        if self.callback and callable(self.callback):
            self.callback()
