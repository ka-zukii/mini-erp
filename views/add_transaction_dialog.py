from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc
import datetime

from modules.inventory.services import TransaksiService, BarangService
from modules.inventory.schemas import TransaksiCreate, BarangResponse, BarangUpdate
from database.db import db

class AddTransactionDialog(QDialog):
    def __init__(self, parent=None, warehouse_id=None):
        super(AddTransactionDialog, self).__init__(parent)
        uic.loadUi("ui/addTransactionDialog.ui", self)
        
        datenow = datetime.datetime.now().date()
        self.addDate.setText(str(datenow))
        
        self.warehouse_id = warehouse_id
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.closeBtn.clicked.connect(self.close)
        self.addBtn.clicked.connect(self.add_transaction)
        self.cancelBtn.clicked.connect(self.reject)
        
    def add_transaction(self):
        kd_brg = self.addItemCode.text()
        jumlah = self.addAmount.text()
        tanggal = self.addDate.text()
        jenis = self.addType.text()
        deskripsi = self.addDescription.text()
        
        if jenis not in ["masuk", "keluar"]:
            self.addType.setText("")
            self.addType.setPlaceholderText("Jenis transaksi harus 'masuk' atau 'keluar'")
            return
        
        exist_barang = BarangService.get_all(db)
        
        # self.barang_id = ""
        self.barang_data: BarangResponse = None
        for barang in exist_barang:
            if kd_brg == barang.kd_barang:
                self.barang_data = barang
                break
        
        payload = TransaksiCreate(
            tanggal= tanggal,
            jenis= jenis,
            jumlah= int(jumlah),
            keterangan= deskripsi,
            id_barang=self.barang_data.id,
            id_gudang=self.warehouse_id
        )
        
        TransaksiService.store(db, payload)
        
        if jenis == "masuk":
            self.barang_data.stock += int(jumlah)
        elif jenis == "keluar":
            self.barang_data.stock -= int(jumlah)
        
        payload_barang = BarangUpdate(
            stock=self.barang_data.stock,
        )
        BarangService.update(db, self.barang_data.id, payload_barang)
        
        self.accept()
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()