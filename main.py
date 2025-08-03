from views.window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

from database.db import local_session
from modules.inventory.services.excel_service import ExcelService
from modules.inventory.services.scanner_service import ScannerService

def app():
    # app = QApplication(sys.argv)
    
    # window = MainWindow()
    # window.show()
    # app.exec()
    # ExcelService.export_barang(local_session())
    ScannerService.scan_invoice(path="assets/invo.jpeg")

if __name__ == "__main__":
    app()