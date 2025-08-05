from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from database.db import db
from modules.inventory.services import BarangService
from modules.inventory.schemas import BarangCreate

class AddStockDialog(QDialog):
    def __init__(self, parent=None, warehouse_id=None):
        super(AddStockDialog, self).__init__(parent)
        uic.loadUi("ui/addStockDialog.ui", self)
        
        self.warehouse_id = warehouse_id
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.closeBtn.clicked.connect(self.close)
        self.addBtn.clicked.connect(self.add_stock)
        self.cancelBtn.clicked.connect(self.reject)
        
    def add_stock(self):
        nama_barang = self.addItemName.text()
        stock_barang = self.addStockAmount.text()
        satuan_barang = self.addUnitsOfQuantity.text()
        
        hr_bl: str = self.addPurchasePrice.text()
        hr_jl: str = self.addSellingPrice.text()
        
        harga_beli = int(hr_bl.replace("Rp", "").replace(".", "").strip())
        harga_jual = int(hr_jl.replace("Rp", "").replace(".", "").strip())
        deskripsi = self.addDescription.text()
        
        print(self.warehouse_id)
        
        payload = BarangCreate(
            nama=nama_barang,
            stock=stock_barang,
            satuan=satuan_barang,
            harga_beli=harga_beli,
            harga_jual=harga_jual,
            deskripsi=deskripsi,
            id_kategori=None,
            id_supplier=None,
            id_gudang=self.warehouse_id
        )
        BarangService.store(db, payload)
        self.accept()
    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        