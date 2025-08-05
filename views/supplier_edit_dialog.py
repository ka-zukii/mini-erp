from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from database.db import db
from modules.inventory.services import BarangService, SupplierService
from modules.inventory.schemas import SupplierUpdate, BarangUpdate

class SupplierEditDialog(QDialog):
    def __init__(self, table, row):
        super(SupplierEditDialog, self).__init__()
        uic.loadUi("ui/supplierEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        # item_code = table.item(row, 1).text()
        supplier_name = table.item(row, 1).text()
        phone_number = table.item(row, 2).text()
        address = table.item(row, 3).text()
        
        self.kd_brng = ""
        barangexits = BarangService.get_all(db)
        
        for brg in barangexits:
            if brg.id_supplier == table.item(row, 0).text():
                self.kd_brng = brg.kd_barang
                break
        
        self.supp_id = table.item(row, 0).text()
        self.editItemCode.setText(self.kd_brng)
        self.editSupplierName.setText(supplier_name)
        self.editPhoneNumber.setText(phone_number)
        self.editAddress.setText(address)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
    
    def save_edited_data(self):
        # take data from input
        item_code = self.editItemCode.text()
        supplier_name = self.editSupplierName.text()
        phone_number = self.editPhoneNumber.text()
        address = self.editAddress.text()
        
        # logic here
        exist_barang = BarangService.get_all(db)
        
        found_item = 0
        for barang in exist_barang:
            if item_code == barang.kd_barang:
                found_item =+ 1
        
        if(found_item <= 0):
            self.editItemCode.setText("")
            self.editItemCode.setPlaceholderText("Barang tidak ditemukan")
            return
        
        payload = SupplierUpdate(
            nama=supplier_name,
            telepon=phone_number,
            alamat=address,
        )
        
        supplier = SupplierService.update(db, self.supp_id, payload)
        
        for barang in exist_barang:
            if barang.kd_barang == item_code:
                payload_barang = BarangUpdate(
                    id_supplier= supplier.id,
                )
                BarangService.update(db, barang.id, payload_barang)
        
        self.accept() # close dialog
        
    def __new__item(self, value):
        from PyQt5.QtWidgets import QTableWidgetItem
        return QTableWidgetItem(value)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()