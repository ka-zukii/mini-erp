from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from modules.inventory.services import TransaksiService, BarangService
from modules.inventory.schemas import TransaksiUpdate, BarangResponse, BarangUpdate
from database.db import db

class TransactionEditDialog(QDialog):
    def __init__(self, table, row):
        super(TransactionEditDialog, self).__init__()
        uic.loadUi("ui/transactionEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        item_code = table.item(row, 1).text()
        date = table.item(row, 3).text()
        type = table.item(row, 4).text()
        amount = table.item(row, 5).text()
        description = table.item(row, 6).text()
        
        self.transaksi_id = table.item(row, 0).text()
        self.editItemCode.setText(item_code)
        self.editDate.setText(date)
        self.editType.setText(type)
        self.editAmount.setText(amount)
        self.editDescription.setText(description)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
        
    def save_edited_data(self):
        item_code = self.editItemCode.text()
        date = self.editDate.text()
        type = self.editType.text()
        amount = self.editAmount.text()
        description = self.editDescription.text()
        
        if type not in ["masuk", "keluar"]:
            self.editType.setText("")
            self.editType.setPlaceholderText("Jenis transaksi harus 'masuk' atau 'keluar'")
            return
        
        exist_barang = BarangService.get_all(db)
        self.barang_data: BarangResponse = None
        
        for barang in exist_barang:
            if item_code == barang.kd_barang:
                self.barang_data = barang
                break
        
        payload = TransaksiUpdate(
            tanggal=date,
            jenis=type,
            jumlah=int(amount),
            keterangan=description,
            id_barang=self.barang_data.id,
        )
        
        TransaksiService.update(db, self.transaksi_id, payload)
        
        if type == "masuk":
            self.barang_data.stock += int(amount)
        elif type == "keluar":
            self.barang_data.stock -= int(amount)
        
        payload_barang = BarangUpdate(
            stock=self.barang_data.stock,
        )
        
        BarangService.update(db, self.barang_data.id, payload_barang)
        
        self.accept()
    
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