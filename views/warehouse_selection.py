from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton, QHeaderView, QTableWidget, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from .add_warehouse_dialog import AddWarehouseDialog
from .warehouse_edit_dialog import WarehouseEditDialog
from .delete_data_dialog import DeleteDataDialog
import data_dummy
import resources_rc

from database.db import db
from modules.inventory.services.gudang_service import GudangService

class WarehouseSelection(QDialog):
    def __init__(self):
        super(WarehouseSelection, self).__init__()
        uic.loadUi("ui/warehouse.ui", self)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.closeBtn.clicked.connect(self.reject)
        
        self.addWarehouseBtn.clicked.connect(self.add_warehouse)
        
        self.inputSearchWarehouse.textChanged.connect(
            lambda: self.search_data_table(self.warehouseTableWidget, self.inputSearchWarehouse)
        )
        
        self.load_data_warehouse()
    
    def get_selected_warehouse_id(self):
        return self.selected_warehouse_id
        
    def load_data_warehouse(self):
        # Menampilkan data gudang di tabel
        warehouse_tables = [
            {
                "table": self.warehouseTableWidget,
                "headers": ["ID", "Nama Warehouse", "Keterangan", "Lokasi", ""],
                "data": GudangService.get_all(db)
            },
        ]
        
        # Mengeluarkan data ke tabel
        for info in warehouse_tables:
            table = info["table"]
            headers = info["headers"]
            data  = info["data"]
            
            row_count = len(data)
            column_count = len(headers)
            
            table.setRowCount(row_count)
            table.setColumnCount(column_count)
            table.setHorizontalHeaderLabels(headers)
            
            self.adjust_table_columns(table, len(headers) - 1)

            for row_num, row_data in enumerate(data):
                
                table.setItem(row_num, 0, QTableWidgetItem(row_data.id))
                table.setItem(row_num, 1, QTableWidgetItem(row_data.nama))
                table.setItem(row_num, 2, QTableWidgetItem(row_data.keterangan))
                table.setItem(row_num, 3, QTableWidgetItem(row_data.lokasi))
                
                warehouse_id = row_data.id    
                self.add_action_buttons(table, row_num, warehouse_id)
                
    def add_action_buttons(self, table, row, warehouse_id):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

        # Open Warehouse Button
        btn_warehouse = QPushButton()
        btn_warehouse.setIcon(QIcon(":/icons/total-warehouse-blue.svg"))
        btn_warehouse.setIconSize(QSize(16, 16))
        btn_warehouse.setStyleSheet(
            """
                QPushButton{
                    border: none;
                    background: transparent;
                    border-radius: 5px;
                    padding:5px;
                }
                QPushButton:hover{
                    background-color: #D9D9D9;
                }
            """)

        # Edit Button
        btn_edit = QPushButton()
        btn_edit.setIcon(QIcon(":/icons/edit-blue.svg"))
        btn_edit.setIconSize(QSize(16, 16))
        btn_edit.setStyleSheet(
            """
                QPushButton{
                    border: none;
                    background: transparent;
                    border-radius: 5px;
                    padding:5px;
                }
                QPushButton:hover{
                    background-color: #D9D9D9;
                }
            """)
        
        # Delete Button
        btn_delete = QPushButton()
        btn_delete.setIcon(QIcon(":/icons/delete-blue.svg"))
        btn_delete.setIconSize(QSize(16, 16))
        btn_delete.setStyleSheet(
            """
                QPushButton{
                    border: none;
                    background: transparent;
                    border-radius: 5px;
                    padding:5px;
                }
                QPushButton:hover{
                    background-color: #D9D9D9;
                }
            """)
        
        btn_warehouse.clicked.connect(lambda _, wid=warehouse_id: self.open_main_window(wid))
        btn_edit.clicked.connect(lambda _, b=btn_edit: self.edit_row(table, b))
        btn_delete.clicked.connect(lambda _, b=btn_delete: self.delete_row(table, b))

        layout.addWidget(btn_warehouse)
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        col_index = table.columnCount() - 1

        # add widget to cell
        table.setCellWidget(row, col_index, widget)

        # Biar cell Action tidak bisa di-select
        dummy_item = QTableWidgetItem()
        dummy_item.setFlags(Qt.NoItemFlags)
        table.setItem(row, col_index, dummy_item)

        # Resize kolom Action agar pas
        header = table.horizontalHeader()
        header.setSectionResizeMode(col_index, QHeaderView.ResizeToContents)
    
    def search_data_table(self, table: QTableWidget, input_search: QLineEdit):
        query = input_search.text().lower()
        
        for row in range(table.rowCount()):
            match = False
            for column in range(table.columnCount() - 1): # to skip last col (action button "edit" and "delete")
                item = table.item(row, column)
                if item and query in item.text().lower():
                    match = True
                    break
            table.setRowHidden(row, not match)
            
    def open_main_window(self, warehouse_id):
        self.selected_warehouse_id = warehouse_id
        self.accept()

    def adjust_table_columns(self, table, action_column_index):
        header = table.horizontalHeader()
        header.setStretchLastSection(False)
        for col in range(table.columnCount()):
            if col == action_column_index:
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(col, QHeaderView.Stretch)
                
    def add_warehouse(self):
        dialog = AddWarehouseDialog(self)
        dialog.exec_()
        self.load_data_warehouse()
    
    def edit_row(self, table, button):
        index = table.indexAt(button.parent().pos())
        row = index.row()
        dialog = WarehouseEditDialog(table, row)
        dialog.exec_()
        self.load_data_warehouse()

    def delete_row(self, table, button):
        # find real-time row
        index = table.indexAt(button.parent().pos())
        row = index.row()
        
        dialog = DeleteDataDialog(table, row, "Gudang")
        dialog.exec_()
        self.load_data_warehouse()

    # Function for dragable dialog window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()