from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QToolButton, QFileDialog, QWidget, QHBoxLayout, QPushButton, QHeaderView, QTableWidget, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import resources_rc
import data_dummy
from .stock_edit_dialog import StockEditDialog
from .supplier_edit_dialog import SupplierEditDialog
from .transaction_edit_dialog import TransactionEditDialog
from .category_edit_dialog import CategoryEditDialog
from .warehouse_edit_dialog import WarehouseEditDialog
from .delete_data_dialog import DeleteDataDialog
from .warehouse_selection import WarehouseSelection
from .add_stock_dialog import AddStockDialog
from .add_supplier_dialog import AddSupplierDialog
from .add_transaction_dialog import AddTransactionDialog
from .add_category_dialog import AddCategoryDialog
# from .user_edit_dialog import UserEditDialog
# from .history_edit_dialog import HistoryEditDialog
from modules.inventory.services.scanner_service import ScannerService

from database.db import db
from modules.inventory.services import BarangService, KategoriService, SupplierService, TransaksiService

class MainWindow(QMainWindow):
    def __init__(self, warehouse_id = None):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/minierp_cool.ui", self)
        
        # Side menu
        # Hide icon only sidebar when app start
        self.icon_only_widget.hide()
        
        # automatically open main page when app started
        self.stackedWidget.setCurrentIndex(0)
        
        self.overviewBtn1.setChecked(True)
        self.overviewBtn2.setChecked(True)
        
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
        
        # Back to select warehouse dialog
        self.warehouseBtn1.clicked.connect(self.return_select_warehouse)
        self.warehouseBtn2.clicked.connect(self.return_select_warehouse)
        
        self.addStockBtn.clicked.connect(self.add_data)
        self.addSupplierBtn.clicked.connect(self.add_data)
        self.addTransactionBtn.clicked.connect(self.add_data)
        self.addCategoryBtn.clicked.connect(self.add_data)
        
        # Searchbar
        self.searchBtnStock.clicked.connect(
            lambda: self.search_data_table(self.stockTableWidget, self.inputSearchStock)
        )
        
        self.searchBtnSupplier.clicked.connect(
            lambda: self.search_data_table(self.supplierTableWidget, self.inputSearchSupplier)
        )
        
        self.searchBtnTransaction.clicked.connect(
            lambda: self.search_data_table(self.transactionTableWidget, self.inputSearchTransaction)
        )
        
        self.searchBtnCategory.clicked.connect(
            lambda: self.search_data_table(self.categoryTableWidget, self.inputSearchCategory)
        )
        
        # automatically search data table without pressing the search button
        self.inputSearchStock.textChanged.connect(
            lambda: self.search_data_table(self.stockTableWidget, self.inputSearchStock)
        )
        
        self.inputSearchSupplier.textChanged.connect(
            lambda: self.search_data_table(self.supplierTableWidget, self.inputSearchSupplier)
        )
        
        self.inputSearchTransaction.textChanged.connect(
            lambda: self.search_data_table(self.transactionTableWidget, self.inputSearchTransaction)
        )
        
        self.inputSearchCategory.textChanged.connect(
            lambda: self.search_data_table(self.categoryTableWidget, self.inputSearchCategory)
        )
        
        # Choose file
        self.chooseFileBtn.clicked.connect(self.open_file)
        
        prev_btn = self.calendarWidget.findChild(QToolButton, "qt_calendar_prevmonth")
        next_btn = self.calendarWidget.findChild(QToolButton, "qt_calendar_nextmonth")
        
        prev_btn.setText("<")
        next_btn.setText(">")
        
        self.warehouse_id = warehouse_id
        
        # Data di dalam gudang
        self.data_barang = BarangService.get_all(db)
        self.data_kategori = KategoriService.get_all(db)
        self.data_supplier = SupplierService.get_all(db)
        self.data_transaksi = TransaksiService.get_all(db)
        
        # load data dummy
        self.load_data(self.warehouse_id)

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
            ScannerService.scan_invoice(file_path, self.warehouse_id)
            self.load_data(self.warehouse_id)

    def load_data(self, warehouse_id=None):
        self.data_barang = BarangService.get_all(db)
        self.data_kategori = KategoriService.get_all(db)
        self.data_supplier = SupplierService.get_all(db)
        self.data_transaksi = TransaksiService.get_all(db)

        tables = [
            {
                "table": self.stockTableWidget,
                "headers": ["ID", "Kode Barang", "Nama Barang", "Satuan", "Harga Beli", "Harga Jual", "Stock", "Deskripsi", ""],
                "fields": ["id", "kd_barang", "nama", "satuan", "harga_beli", "harga_jual", "stock", "deskripsi"],
                "data": self.data_barang,
                "filter_by_warehouse": True
            },
            {
                "table": self.supplierTableWidget,
                "headers": ["ID", "Nama", "Telepon", "Alamat", ""],
                "fields": ["id", "nama", "telepon", "alamat"],
                "data": self.data_supplier,
                "filter_by_warehouse": True
            },
            {
                "table": self.transactionTableWidget,
                "headers": ["ID", "Kode Barang", "Nama Barang", "Tanggal", "Jenis", "Jumlah", "Keterangan", ""],
                "fields": ["id", "barang.kd_barang", "barang.nama", "tanggal", "jenis", "jumlah", "keterangan"],
                "data": self.data_transaksi,
                "filter_by_warehouse": True
            },
            {
                "table": self.categoryTableWidget,
                "headers": ["ID", "Nama", "Deskripsi", "Total Barang", ""],
                "fields": ["id", "nama", "deskripsi", "barang_list|count"],
                "data": self.data_kategori,
                "filter_by_warehouse": True
            },
        ]

        for info in tables:
            table = info["table"]
            headers = info["headers"]
            data_dict = info["data"]
            filter_by_warehouse = info.get("filter_by_warehouse", False)

            if warehouse_id and filter_by_warehouse:
                filtered_data = [item for item in data_dict if getattr(item, "id_gudang", None) == warehouse_id]
            else:
                filtered_data = data_dict

            table.setRowCount(len(filtered_data))
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers + [""])

            self.adjust_table_columns(table, len(headers))

            for row_num, item in enumerate(filtered_data):
                fields = info.get("fields")
                for col_num, field in enumerate(fields):
                    # Deteksi apakah field mengandung operator seperti |count
                    if "|" in field:
                        base_field, op = field.split("|")
                    else:
                        base_field, op = field, None

                    # Tangani relasi nested seperti barang.kd_barang
                    if "." in base_field:
                        value = item
                        for attr in base_field.split("."):
                            value = getattr(value, attr, None)
                            if value is None:
                                break
                    else:
                        value = getattr(item, base_field, None)

                    # Jalankan operator khusus (misalnya count)
                    if op == "count" and value is not None:
                        value = len(value)
                    elif value is None:
                        value = ""

                    table.setItem(row_num, col_num, QTableWidgetItem(str(value)))

                self.add_action_buttons(table, row_num)
    
    def return_select_warehouse(self):
        self.close()
        
        self.warehouse_selection = WarehouseSelection()
        self.warehouse_selection.exec_()
        
        try:
            selected_warehouse_id = self.warehouse_selection.get_selected_warehouse_id()
            self.__init__(warehouse_id=selected_warehouse_id)  # reinit ulang MainWindow
            self.show()
        except AttributeError:
            pass  # tidak memilih gudang
                
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
                
    def adjust_table_columns(self, table, action_column_index):
        header = table.horizontalHeader()
        header.setStretchLastSection(False)
        for col in range(table.columnCount()):
            if col == action_column_index:
                header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(col, QHeaderView.Stretch)
            
    def add_action_buttons(self, table, row):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignCenter)

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
        
        btn_edit.clicked.connect(lambda _, b=btn_edit: self.edit_row(table, b))
        btn_delete.clicked.connect(lambda _, b=btn_delete: self.delete_row(table, b))

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
        
    def add_data(self):
        current_index = self.stackedWidget.currentIndex()
        current_page = self.stackedWidget.widget(current_index)
        page_name = current_page.objectName()
        
        dialog_map = {
            "page_2": lambda: AddStockDialog(self, warehouse_id=self.warehouse_id),
            "page_3": lambda: AddSupplierDialog(self, warehouse_id=self.warehouse_id),
            "page_4": lambda: AddTransactionDialog(self, warehouse_id=self.warehouse_id),
            "page_5": lambda: AddCategoryDialog(self, warehouse_id=self.warehouse_id),
        }
        
        dialog_class = dialog_map.get(page_name)
        
        if dialog_class:
            dialog = dialog_class()
            dialog.exec_()
            self.load_data(self.warehouse_id)
        else:
            print(f"Tidak ada dialog untuk page: {page_name}")
        
    def edit_row(self, table, button):
        index = table.indexAt(button.parent().pos())
        row = index.row()
        table_name = table.objectName()
        
        if table_name == "stockTableWidget":
            dialog = StockEditDialog(table, row)
        elif table_name == "supplierTableWidget":
            dialog = SupplierEditDialog(table, row)
        elif table_name == "transactionTableWidget":
            dialog = TransactionEditDialog(table, row)
        elif table_name == "categoryTableWidget":
            dialog = CategoryEditDialog(table, row)
        else:
            print(f"Table {table} not found")
        
        dialog.exec_()
        self.load_data(self.warehouse_id)

    def delete_row(self, table, button):
        # find real-time row
        current_index = self.stackedWidget.currentIndex()
        current_page = self.stackedWidget.widget(current_index)
        page_name = current_page.objectName()
        
        index = table.indexAt(button.parent().pos())
        row = index.row()
        
        dialog_map = {
            "page_2": lambda: DeleteDataDialog(table, row, "Barang"),
            "page_3": lambda: DeleteDataDialog(table, row, "Supplier"),
            "page_4": lambda: DeleteDataDialog(table, row, "Transaksi"),
            "page_5": lambda: DeleteDataDialog(table, row, "Kategori"),
        }
        
        dialog_class = dialog_map.get(page_name)
        
        if dialog_class:
            dialog = dialog_class()
            dialog.exec_()
            self.load_data(self.warehouse_id)
        
        self.load_data(self.warehouse_id)

    def toggleSidebar(self):
        if self.icon_text_widget.isVisible():
            self.icon_text_widget.hide()
            self.icon_only_widget.show()
        else:
            self.icon_text_widget.show()
            self.icon_only_widget.hide()