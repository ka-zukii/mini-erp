from views.window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from views.warehouse_selection import WarehouseSelection

def app():
    
    app = QApplication(sys.argv)
    selection = WarehouseSelection()
    selection.exec_()
    
    try:
        selected_warehouse_id = selection.get_selected_warehouse_id()
    except AttributeError:
        sys.exit()
    
    window = MainWindow(warehouse_id=selected_warehouse_id)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    app()