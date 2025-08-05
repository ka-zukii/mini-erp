from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

from database.db import db
from modules.inventory.services import KategoriService
from modules.inventory.schemas import KategoriUpdate

class CategoryEditDialog(QDialog):
    def __init__(self, table, row):
        super(CategoryEditDialog, self).__init__()
        uic.loadUi("ui/categoryEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        self.id_kategori = table.item(row, 0).text()
        category_name = table.item(row, 1).text()
        description = table.item(row, 2).text()
        
        self.editCategoryName.setText(category_name)
        self.editDescription.setText(description)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
        
    def save_edited_data(self):
        category_name = self.editCategoryName.text()
        description = self.editDescription.text()
        
        payload = KategoriUpdate(
            nama=category_name,
            deskripsi=description
        )
        
        KategoriService.update(db, self.id_kategori, payload)
        self.accept() # close dialog after saving
        
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