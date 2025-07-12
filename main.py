from views.window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

def app():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    app()