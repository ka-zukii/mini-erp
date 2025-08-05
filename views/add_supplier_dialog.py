from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from database.db import db
from modules.inventory.services import BarangService, SupplierService
from modules.inventory.schemas import SupplierCreate, BarangUpdate

class AddSupplierDialog(QDialog):
    def __init__(self, parent=None, warehouse_id=None):
        super(AddSupplierDialog, self).__init__(parent)
        uic.loadUi("ui/addSupplierDialog.ui", self)
        
        self.warehouse_id = warehouse_id
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.closeBtn.clicked.connect(self.close)
        self.addBtn.clicked.connect(self.add_supplier)
        self.cancelBtn.clicked.connect(self.reject)
        
    def add_supplier(self):
        kode_barang = self.addItemCode.text()
        nama = self.addSupplierName.text()
        telepon = self.addPhoneNumber.text()
        alamat = self.addAddress.text()
        
        # logic here
        exist_barang = BarangService.get_all(db)
        
        found_item = 0
        for barang in exist_barang:
            if kode_barang == barang.kd_barang:
                found_item =+ 1
        
        if(found_item <= 0):
            self.addItemCode.setText("")
            self.addItemCode.setPlaceholderText("Barang tidak ditemukan")
            return
        
        payload = SupplierCreate(
            nama=nama,
            telepon=telepon,
            alamat=alamat,
            id_gudang=self.warehouse_id
        )
        
        supplier = SupplierService.store(db, payload)
        
        for barang in exist_barang:
            if barang.kd_barang == kode_barang:
                payload_barang = BarangUpdate(
                    id_supplier= supplier.id,
                )
                BarangService.update(db, barang.id, payload_barang)
        self.accept()
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()