from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

class SupplierEditDialog(QDialog):
    def __init__(self, table, row):
        super(SupplierEditDialog, self).__init__()
        uic.loadUi("ui/supplierEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        item_code = table.item(row, 1).text()
        supplier_name = table.item(row, 2).text()
        phone_number = table.item(row, 3).text()
        address = table.item(row, 4).text()
        
        self.editItemCode.setText(item_code)
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
        
        # update the table data
        self.table.setItem(self.row, 1, self.__new__item(item_code))
        self.table.setItem(self.row, 2, self.__new__item(supplier_name))
        self.table.setItem(self.row, 3, self.__new__item(phone_number))
        self.table.setItem(self.row, 4, self.__new__item(address))
        
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