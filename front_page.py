from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QToolButton, QFileDialog, QWidget, QHBoxLayout, QPushButton, QHeaderView
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import resources_rc
import data_dummy

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/minierp_cool.ui", self)
        
        # Hide icon only sidebar when app start
        self.icon_only_widget.hide()
        
        # Connect hamburgerButton clicked
        self.hamburgerBtn1.clicked.connect(self.toggleSidebar)
        self.hamburgerBtn2.clicked.connect(self.toggleSidebar)

        # Switch Page
        
        # Switch to overview
        self.overviewBtn1.clicked.connect(lambda: self.switch_page(0))
        self.overviewBtn2.clicked.connect(lambda: self.switch_page(0))

        # Switch to stock
        self.stockBtn1.clicked.connect(lambda: self.switch_page(1))
        self.stockBtn2.clicked.connect(lambda: self.switch_page(1))

        # Switch to supplier
        self.supplierBtn1.clicked.connect(lambda: self.switch_page(2))
        self.supplierBtn2.clicked.connect(lambda: self.switch_page(2))

        # Swtich to transaction
        self.transactionBtn1.clicked.connect(lambda: self.switch_page(3))
        self.transactionBtn2.clicked.connect(lambda: self.switch_page(3))
        
        # Switch to category
        self.categoryBtn1.clicked.connect(lambda: self.switch_page(4))
        self.categoryBtn2.clicked.connect(lambda: self.switch_page(4))
        
        # Switch to warehouse
        self.warehouseBtn1.clicked.connect(lambda: self.switch_page(5))
        self.warehouseBtn2.clicked.connect(lambda: self.switch_page(5))
        
        # Switch to user
        self.userBtn1.clicked.connect(lambda: self.switch_page(6))
        self.userBtn2.clicked.connect(lambda: self.switch_page(6))
        
        # Swtich to history
        self.historyBtn1.clicked.connect(lambda: self.switch_page(7))
        self.historyBtn2.clicked.connect(lambda: self.switch_page(7))
        
        # Choose file
        self.chooseFileBtn.clicked.connect(self.open_file)
        
        prev_btn = self.calendarWidget.findChild(QToolButton, "qt_calendar_prevmonth")
        next_btn = self.calendarWidget.findChild(QToolButton, "qt_calendar_nextmonth")
        
        prev_btn.setText("<")
        next_btn.setText(">")
        
        # Make vertical header table hidden
        # self.stockTableWidget.verticalHeader().setVisible(False)
        
        # load data dummy
        self.load_data()

    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
    
    # Choose file function
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Pilih File",
            "",
            "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg)"
        )
        if file_path:
            print("File dipilih:", file_path)

    # Function for load dummy data from data_dummy.py
    def load_data(self):
        data = data_dummy.dummy_data

        row_count = len(data)
        column_count = len(data[0]) + 1  # Tambah 1 kolom Action

        self.stockTableWidget.setRowCount(row_count)
        self.stockTableWidget.setColumnCount(column_count)

        headers = ["ID", "Kode Barang", "Nama Barang", "Deskripsi",
                "Satuan", "Harga Beli", "Harga Jual", "Stock", ""]
        self.stockTableWidget.setHorizontalHeaderLabels(headers)

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.stockTableWidget.setItem(row_num, col_num, item)
                
            self.add_crud_buttons(self.stockTableWidget, row_num)
            # self.add_crud_buttons(self.supplierTableWidget, row_num)
            # self.add_crud_buttons(self.transactionTableWidget, row_num)
            # self.add_crud_buttons(self.categoryTableWidget, row_num)
            # self.add_crud_buttons(self.warehouseTableWidget, row_num)
            # self.add_crud_buttons(self.userTableWidget, row_num)
            
    def add_crud_buttons(self, table, row):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(50)
        layout.setAlignment(Qt.AlignCenter)

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
        btn_edit.clicked.connect(lambda _, r=row, t=table: self.edit_row(t, r))

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
        btn_delete.clicked.connect(lambda _, r=row, t=table: self.delete_row(t, r))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        widget.setLayout(layout)

        col_index = table.columnCount() - 1

        # Tambahkan widget ke cell
        table.setCellWidget(row, col_index, widget)

        # Biar cell Action tidak bisa di-select
        dummy_item = QTableWidgetItem()
        dummy_item.setFlags(Qt.NoItemFlags)
        table.setItem(row, col_index, dummy_item)

        # Resize kolom Action agar pas
        header = table.horizontalHeader()
        header.setSectionResizeMode(col_index, QHeaderView.ResizeToContents)
        
    def edit_row(self, table, row):
        print(f"Edit row {row} di tabel: {table.objectName()}")

    def delete_row(self, table, row):
        print(f"Delete row {row} di tabel: {table.objectName()}")

    def toggleSidebar(self):
        if self.icon_text_widget.isVisible():
            self.icon_text_widget.hide()
            self.icon_only_widget.show()
        else:
            self.icon_text_widget.show()
            self.icon_only_widget.hide()