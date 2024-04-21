from PyQt6.QtWidgets import QApplication
import sys
from gui.main_window import MainWindow
# try:
#     from gui.main_window import MainWindow
# except ImportError as e:
#     print(f"Failed to import modules: {e}")
#     sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 main.py listname")
        sys.exit(1)

    listname = sys.argv[1]
    app = QApplication(sys.argv)
    main_window = MainWindow(listname)
    main_window.show()
    sys.exit(app.exec())