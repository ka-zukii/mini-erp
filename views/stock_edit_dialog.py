from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from database.db import db
from modules.inventory.services import BarangService
from modules.inventory.schemas import BarangUpdate

class StockEditDialog(QDialog):
    def __init__(self, table, row):
        super(StockEditDialog, self).__init__()
        uic.loadUi("ui/stockEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        item_name = table.item(row, 2).text()
        units_of_quantity = table.item(row, 3).text()
        purchase_price = table.item(row, 4).text()
        selling_price = table.item(row, 5).text()
        stock = table.item(row, 6).text()
        description = table.item(row, 7).text()
        
        self.editItemName.setText(item_name)
        self.editUnitsOfQuantity.setText(units_of_quantity)
        self.editPurchasePrice.setText(purchase_price)
        self.editSellingPrice.setText(selling_price)
        self.editStock.setText(stock)
        self.editDescription.setText(description)
        
        # Make window frameless from default window frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
    
    @staticmethod
    def _parse_rupiah(value: str) -> int:
        if not value or str(value).strip().lower() == 'none':
            return 0
        try:
            cleaned = value.replace("Rp", "").replace(".", "").strip()
            return int(cleaned)
        except ValueError:
            return 0
    
    def save_edited_data(self):
        # take data from input
        item_name = self.editItemName.text()
        units_of_quantity = self.editUnitsOfQuantity.text()
        purchase_price = self.editPurchasePrice.text()
        selling_price = self.editSellingPrice.text()
        stock = self.editStock.text()
        description = self.editDescription.text()
        
        # update the table data
        payload = BarangUpdate(
            nama=item_name,
            satuan=units_of_quantity,
            harga_beli=self._parse_rupiah(purchase_price),
            harga_jual=self._parse_rupiah(selling_price),
            stock=int(stock),
            deskripsi=description
        )
        
        BarangService.update(db, self.table.item(self.row, 0).text(), payload)
        
        self.accept() # to close dialog
    
    # to always create a new QTableWidgetItem
    def __new__item(self, value):
        from PyQt5.QtWidgets import QTableWidgetItem
        return QTableWidgetItem(value)
                
    # Function for dragable dialog window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()