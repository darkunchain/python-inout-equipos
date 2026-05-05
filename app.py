import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from database.schema import create_tables
from ui.main_window import MainWindow


def load_styles(app: QApplication):
    style_path = Path(__file__).resolve().parent / "styles" / "main.qss"

    if style_path.exists():
        with open(style_path, "r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())


def main():
    create_tables()

    app = QApplication(sys.argv)
    load_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()