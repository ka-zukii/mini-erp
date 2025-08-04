from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
import resources_rc

class HistoryEditDialog(QDialog):
    def __init__(self, table, row):
        super(HistoryEditDialog, self).__init__()
        uic.loadUi("ui/historyEditDialog.ui", self)
        
        self.table = table
        self.row = row
        
        time = table.item(row, 4).text()
        action = table.item(row, 5).text()
        entity = table.item(row, 6).text()
        description = table.item(row, 9).text()
        
        self.editTime.setText(time)
        self.editAction.setText(action)
        self.editEntity.setText(entity)
        self.editDescription.setText(description)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.saveBtn.clicked.connect(self.save_edited_data)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.closeBtn.clicked.connect(self.close)
        
    def save_edited_data(self):
        
        time = self.editTime.text()
        action = self.editTime.text()
        entity = self.editEntity.text()
        description = self.editDescription.text()
        
        self.table.setItem(self.row, 4, self.__new__item(time))
        self.table.setItem(self.row, 5, self.__new__item(action))
        self.table.setItem(self.row, 6, self.__new__item(entity))
        self.table.setItem(self.row, 9, self.__new__item(description))
        
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