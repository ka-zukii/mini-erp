from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

class TransactionEditDialog(QDialog):
    def __init__(self, table, row):
        super(TransactionEditDialog, self).__init__()
        uic.loadUi("ui/transactionEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        item_code = table.item(row, 1).text()
        warehouse_code = table.item(row, 2).text()
        date = table.item(row, 3).text()
        type = table.item(row, 4).text()
        amount = table.item(row, 5).text()
        description = table.item(row, 6).text()
        
        self.editItemCode.setText(item_code)
        self.editWarehouseCode.setText(warehouse_code)
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
        warehouse_code = self.editWarehouseCode.text()
        date = self.editDate.text()
        type = self.editType.text()
        amount = self.editAmount.text()
        description = self.editDescription.text()
        
        self.table.setItem(self.row, 1, self.__new__item(item_code))
        self.table.setItem(self.row, 2, self.__new__item(warehouse_code))
        self.table.setItem(self.row, 3, self.__new__item(date))
        self.table.setItem(self.row, 4, self.__new__item(type))
        self.table.setItem(self.row, 5, self.__new__item(amount))
        self.table.setItem(self.row, 6, self.__new__item(description))
        
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