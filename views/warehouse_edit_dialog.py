from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from database.db import db
from modules.inventory.services import GudangService
from modules.inventory.schemas import GudangUpdate

class WarehouseEditDialog(QDialog):
    def __init__(self, table, row):
        super(WarehouseEditDialog, self).__init__()
        uic.loadUi("ui/warehouseEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        warehouse_name = table.item(row, 1).text()
        description = table.item(row, 2).text()
        location = table.item(row, 3).text()
        
        self.warehouse_id = table.item(row, 0).text()
        self.editWarehouseName.setText(warehouse_name)
        self.editDescription.setText(description)
        self.editLocation.setText(location)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
        
    def save_edited_data(self):
        
        warehouse_name = self.editWarehouseName.text()
        description = self.editDescription.text()
        location = self.editLocation.text()
        
        payload = GudangUpdate(
            nama=warehouse_name,
            keterangan=description,
            lokasi=location
        )
        
        GudangService.update(db, self.warehouse_id, payload)
        
        self.accept()
        
    def __new__item(self, value):
        from PyQt5.QtWidgets import QTableWidgetItem
        return QTableWidgetItem(value)
    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()