# standard
import sys

# internal
from src.ui import UI
from src import utils

# pyqt
from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # check for single-instance
    if utils.is_single_instance():
        main()
