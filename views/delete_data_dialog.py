from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from modules.inventory.services import GudangService, BarangService, KategoriService, SupplierService, TransaksiService
from database.db import db

class DeleteDataDialog(QDialog):
    def __init__(self, table, row, table_name):
        super(DeleteDataDialog, self).__init__()
        uic.loadUi("ui/deleteDialog.ui", self)
        
        self.table = table
        self.row = row
        self.table_name = table_name
        
        # Make window frameless from default window frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.confirmDeleteBtn.clicked.connect(self.confirm_delete)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
    
    # Function for delete data when the confirmDeleteBtn clicked
    def confirm_delete(self):
        # self.table.removeRow(self.row)
        
        if self.table_name == "Gudang":
            warehouse_id = self.table.item(self.row, 0).text()
            GudangService.destroy(db, warehouse_id)
        elif self.table_name == "Barang":
            item_id = self.table.item(self.row, 0).text()
            BarangService.destroy(db, item_id)
        elif self.table_name == "Kategori":
            category_id = self.table.item(self.row, 0).text()
            KategoriService.destroy(db, category_id)
        elif self.table_name == "Supplier":
            supplier_id = self.table.item(self.row, 0).text()
            SupplierService.destroy(db, supplier_id)
        elif self.table_name == "Transaksi":
            transaction_id = self.table.item(self.row, 0).text()
            TransaksiService.destroy(db, transaction_id)
        self.accept()
    
    # Function for dragable dialog window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()