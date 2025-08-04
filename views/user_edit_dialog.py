from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

class UserEditDialog(QDialog):
    def __init__(self, table, row):
        super(UserEditDialog, self).__init__()
        uic.loadUi("ui/userEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        full_name = table.item(row, 1).text()
        username = table.item(row, 2).text()
        password = table.item(row, 3).text()
        role = table.item(row, 4).text()
        
        self.editFullName.setText(full_name)
        self.editUsername.setText(username)
        self.editPassword.setText(password)
        self.editRole.setText(role)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
        
    def save_edited_data(self):
        
        full_name = self.editFullName.text()
        username = self.editUsername.text()
        password = self.editPassword.text()
        role = self.editRole.text()
        
        self.table.setItem(self.row, 1, self.__new__item(full_name))
        self.table.setItem(self.row, 2, self.__new__item(username))
        self.table.setItem(self.row, 3, self.__new__item(password))
        self.table.setItem(self.row, 4, self.__new__item(role))
        
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