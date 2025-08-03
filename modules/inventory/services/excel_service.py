from sqlalchemy.orm import Session
from modules.inventory.models import *
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import pandas as pd

# Service untuk mengelola ekspor data ke Excel

class ExcelService:
    # Metode statis untuk mengekspor data barang ke file Excel
    @staticmethod
    def export_barang(db: Session):
        # Dialog pilih lokasi file
        root = Tk()
        root.withdraw()
        file_path = asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Simpan File Excel",
            initialfile="laporan_gudang.xlsx"
        )
        root.destroy()

        if not file_path:
            print("⚠️ Export dibatalkan.")
            return

        try:
            # Menggunakan Pandas untuk menulis data ke Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Sheet 1: Daftar Gudang
                ExcelService.get_data_gudang(db, writer)
                # Sheet 2+: Barang per Gudang
                ExcelService.get_data_barang_per_gudang(db, writer)

            print("✅ Berhasil mengekspor data barang ke Excel.")
        except Exception as e:
            print(f"❌ Terjadi kesalahan saat mengekspor data: {e}")
        finally:
            db.close()

    # Metode statis untuk mengambil data gudang untuk di ekspor
    @staticmethod
    def get_data_gudang(db: Session, writer: pd.ExcelWriter):
        # Mengambil data gudang dari database
        gudang_list = db.query(Gudang).all()
        # Membuat list of dictionaries untuk setiap gudang
        data_gudang = [{
            "ID Gudang": g.id,
            "Nama Gudang": g.nama,
            "Alamat Gudang": g.alamat,
            "Keterangan": g.keterangan
        } for g in gudang_list]

        # Membuat DataFrame dari data gudang
        df_gudang = pd.DataFrame(data_gudang)
        if df_gudang.empty:
            df_gudang = pd.DataFrame(columns=["ID Gudang", "Nama Gudang", "Alamat Gudang", "Keterangan"])

        # Menulis DataFrame ke sheet Excel
        df_gudang.to_excel(writer, index=False, sheet_name='Daftar Gudang')

    # Metode statis untuk mengambil data barang per gudang untuk di ekspor
    @staticmethod
    def get_data_barang_per_gudang(db: Session, writer: pd.ExcelWriter):
        # Mengambil data gudang dari database
        gudang_list = db.query(Gudang).all()
        
        # Iterasi setiap gudang untuk mengambil data barang
        for gudang in gudang_list:
            data_barang = db.query(Barang).filter(Barang.gudang_id == gudang.id).all()
            
            # Membuat list of dictionaries untuk setiap barang
            data_barang_list = [{
                "ID Barang": b.id,
                "Nama Barang": b.nama,
                "Harga Satuan": b.harga_satuan,
                "Stok": b.stok,
                "Satuan": b.satuan,
                "Deskripsi": b.deskripsi,
                "Kategori": b.kategori.nama if b.kategori else None
            } for b in data_barang]
            
            # Membuat DataFrame dari data barang
            df_barang = pd.DataFrame(data_barang_list)
            if df_barang.empty:
                df_barang = pd.DataFrame(columns=["ID Barang", "Nama Barang", "Harga Satuan", "Stok", "Satuan", "Deskripsi", "Kategori"])
            
            # Menulis DataFrame ke sheet Excel dengan nama gudang
            sheet_name = gudang.nama[:31] if gudang.nama else f"Gudang {gudang.id}"
            df_barang.to_excel(writer, index=False, sheet_name=sheet_name)