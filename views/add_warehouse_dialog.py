from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from modules.inventory.services.gudang_service import GudangService
from modules.inventory.schemas.gudang_schema import GudangCreate

from database.db import db

class AddWarehouseDialog(QDialog):
    def __init__(self, parent=None):
        super(AddWarehouseDialog, self).__init__(parent)
        uic.loadUi("ui/addWarehouseDialog.ui", self)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.closeBtn.clicked.connect(self.close)
        self.cancelBtn.clicked.connect(self.reject)
        self.addBtn.clicked.connect(self.add_warehouse)
        
    # Menambahkan data gudang baru
    def add_warehouse(self):
        # Mengambil nilai dari input field
        nama_gudang = self.addWarehouseName.text()
        keterangan_gudang = self.addDescription.text()
        lokasi_gudang = self.addLocation.text()
        
        # Validasi input
        payload_gudang = GudangCreate(
            nama=nama_gudang,
            lokasi=lokasi_gudang,
            keterangan=keterangan_gudang
        )
        
        # Menyimpan data gudang baru ke database
        GudangService.store(db, payload_gudang)
        
        self.accept()
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        