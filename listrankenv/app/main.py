from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from button_widget import ButtonWidget
from List import List
import sys

class MainWindow(QMainWindow):
    def __init__(self, listname):
        super().__init__()
        self.setWindowTitle(f"List Rank: {listname}")
        self.setGeometry(100, 100, 300, 200)
        self.list = List(listname)
        self.items = []
        self.initUI()
        self.refresh_items_and_buttons()

    def initUI(self):
        # Create a central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Horizontal layout for side-by-side buttons
        self.buttons_layout = QHBoxLayout()
        
        # Initialize buttons without text; they will be set in refresh_items_and_buttons
        self.button1 = ButtonWidget("", None, lambda: self.update_scores_and_refresh(self.items[0], self.items[1]))
        self.button2 = ButtonWidget("", None, lambda: self.update_scores_and_refresh(self.items[1], self.items[0]))
        
        # Add buttons to the horizontal layout
        self.buttons_layout.addWidget(self.button1)
        self.buttons_layout.addWidget(self.button2)

        # Add the horizontal layout to the main vertical layout
        main_layout.addLayout(self.buttons_layout)

        # New button to print the sorted list
        self.print_button = QPushButton("Print Sorted List")
        self.print_button.clicked.connect(self.print_sorted_list)
        
        # Add the print button at the bottom
        main_layout.addWidget(self.print_button)

    def refresh_items_and_buttons(self):
        # Get two distinct items
        try:
            self.items = self.list.get_two_distinct_items()
        except ValueError as e:
            print(e)
            return

        # Update button texts and associated items
        self.button1.update_text_and_item(self.items[0].name, self.items[0])
        self.button2.update_text_and_item(self.items[1].name, self.items[1])

    def update_scores_and_refresh(self, winner, loser):
        # Update scores
        self.list.update_score(winner, loser)
        
        # Refresh the items displayed on the buttons
        self.refresh_items_and_buttons()

    def print_sorted_list(self):
        # Sort the items and print to console
        sorted_items = sorted(self.list.items)
        for item in sorted_items:
            print(item)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 main.py listname")
        sys.exit(1)

    listname = sys.argv[1]
    app = QApplication(sys.argv)
    main_window = MainWindow(listname)
    main_window.show()
    sys.exit(app.exec())
