import sys
import qdarktheme
from PySide6.QtWidgets import QApplication

from src.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    main_window = MainWindow()
    main_window.show()
    app.exec()
