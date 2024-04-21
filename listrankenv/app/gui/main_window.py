from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QAction  # Corrected import for QAction
from gui.button_widget import ButtonWidget
from models.list.List import List

class MainWindow(QMainWindow):
    def __init__(self, listname):
        super().__init__()
        self.listname = listname
        self.setWindowTitle(f"List Rank: {listname}")
        self.setGeometry(100, 100, 300, 200)
        # self.embeddings = self.load_embeddings()
        self.list = List(listname)
        self.items = []
        self.initUI()
        self.refresh_items_and_buttons()

    def initUI(self):
        menu_bar = self.menuBar()
        menu = menu_bar.addMenu("&Menu")  # The ampersand indicates a keyboard shortcut

        # Create an action for printing the sorted list
        print_action = QAction("&Print Sorted List", self)
        print_action.triggered.connect(self.print_sorted_list)
        menu.addAction(print_action)

        print_clusters_action = QAction("&Print Clusters", self)
        print_clusters_action.triggered.connect(self.print_clusters)
        menu.addAction(print_clusters_action)

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

        # Horizontal layout for input and add word button
        self.input_layout = QHBoxLayout()
        self.new_word_input = QLineEdit()
        self.new_word_input.setPlaceholderText("Enter a new word...")
        self.input_layout.addWidget(self.new_word_input)

        self.add_word_button = QPushButton("Add Word")
        self.add_word_button.clicked.connect(self.add_new_word)
        self.input_layout.addWidget(self.add_word_button)

        # Add the input layout to the main vertical layout
        main_layout.addLayout(self.input_layout)

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
        print(f"Sorted list of {self.listname}\n")
        sorted_items = sorted(self.list.items, reverse=True)

        # Find the maximum width of each field to align the columns properly
        max_name_length = max(len(item.name) for item in sorted_items)
        max_score_length = max(len(str(item.score)) for item in sorted_items)
        max_frequency_length = max(len(str(item.frequency)) for item in sorted_items)

        # Create a format string that aligns each column
        format_string = "{:<{name_width}}: {:>{score_width}}: {:>{freq_width}} times appeared"

        # Print each item using the format string
        for item in sorted_items:
            print(format_string.format(
                item.name, item.score, item.frequency,
                name_width=max_name_length,
                score_width=max_score_length,
                freq_width=max_frequency_length
            ))

        print('\n')

    def print_clusters(self):
        self.list.print_clusters(4)
        print('\n')
    
    def add_new_word(self):
        new_word = self.new_word_input.text().strip()
        if new_word:
            # Add new word to the list and update files
            self.list.add_item(new_word, 1000)  # Assuming default score of 1000
            self.refresh_items_and_buttons()
            self.new_word_input.clear()  # Clear the input box after adding